import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
from pathlib import Path
from uuid import UUID

import cv2
from aiohttp import web
import aiohttp_cors
from av import VideoFrame
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from VideoTransformer import VideoTransformer
from app.Application import Application
from app.PersonManager import PersonNotFoundException

from network_models import GetPersonsResponse

routes = web.RouteTableDef()

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()
relay = MediaRelay()

core = Application();

async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

@routes.get('/get-image/{person_id}')
async def serve_img(request):
    """Dummy endpoint that shows how to serve images"""
    _id = UUID(request.match_info['person_id'])
    person = Application().person_manager.get_person(_id)
    file_dir=Application().images_manager.get_images_dir(person.faces[0].id)
    file_names = os.listdir(file_dir)
    path = os.path.join(file_dir,file_names[0])
    data = Path(path).read_bytes()
    return web.Response(body=data, content_type="image/png")

async def offer(request):
    print("called offer")
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    recorder = MediaBlackhole()
    
    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)
        pc.addTrack(VideoTransformer(relay.subscribe(track),core))
        if args.record_to:
            recorder.addTrack(relay.subscribe(track))

    # handle offer
    await pc.setRemoteDescription(offer)
    # await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

# dummy endpoint for debugging purposes
async def dummy(request):
    return web.Response(
        content_type="application/json",
        text=json.dumps({"text": "Hello!"})
    )

async def get_persons(request):
    persons = list(Application().person_manager.get_all_persons().values())
    resp = GetPersonsResponse(persons=persons)

    return web.Response(
        content_type="application/json",
        text=resp.json()
    )

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

async def delete_person(request):
    params = await request.json()
    print(f"id to delete:{params['id']}")
    try:
        Application().person_manager.delete_person(params["id"]);
    except PersonNotFoundException as e:
        print(f"Person with id {params['id']} not found")

async def rename_person(request):
    params = await request.json()
    print(f"id to rename: {params['id']}")
    print(f"new name: {params['new_name']}")
    Application().person_manager.rename_person(params['id'],params['new_name'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--record-to", help="Write received media to a file."),
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    app.router.add_get("/dummy",dummy)
    app.router.add_get("/get-persons",get_persons)
    app.router.add_post('/rename-person',rename_person)
    app.router.add_post('/delete-person',delete_person)
    app.router.add_get('/get-image/{person_id}',serve_img)
    
    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )
