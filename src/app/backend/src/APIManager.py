from src.shared.image_transfer_converter import ImageTransferConverter
from src.shared.network_models import DetectFacesRequest,DetectFacesResponse,RecognizeFaceRequest,RecognizeFaceResponse
from src.shared.models import BoundingBox

from PIL.PngImagePlugin import PngImageFile
from typing import List,Optional,Type
from uuid import UUID
import aiohttp
from aiohttp import HTTPError, ClientResponseError,  ClientConnectorError
from asyncio import TimeoutError
from pydantic import BaseModel
from enum import Enum

DEFAULT_API_URL = ""
HTTP_TIMEOUT = 2


class RequestMethod(str, Enum):
    GET = "GET"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class APICommunicationError(Exception):
    """Raised when an HTTP API call fails."""
    def __init__(self, message: str = "API Call failed."):
        super().__init__(message)


class APIManager:
    """Class that responsible for API communication."""

    def __init__(self, api_url:str=DEFAULT_API_URL):
        self.__api_url = api_url
        self.__is_api_online = False
        self.__session = aiohttp.ClientSession()

    async def __do_communication(
            self,
            api_endpoint: str,
            request_model_object: Optional[BaseModel] = None,
            response_model_class: Optional[Type[BaseModel]] = None,
            method: Optional[RequestMethod] = RequestMethod.POST
        ):
        """Executes a http request.

        This method is used by all API call methods to uniformly handle requests.

        Args:
            api_endpoint (str): API endpoint name. Appended to API base url.
            request_model_object (BaseModel, optional): Model object to be sent to API Server.
            response_model_class (type[BaseModel], optional): Model class into which the
                response should be parsed. None if no response should be parsed.

        Returns:
            A model object instance derived from response_model_class on success.

        Raises:
            ValidationError if response cannot be parsed into response_model_class.
            APICommunicationError if the communication with server failed.
        """
        try:
            target_url = f"{self.__api_url}/{api_endpoint}"
            request_params = {
                "method": method.value,
                "url": target_url,
                "timeout": HTTP_TIMEOUT
            }
            
            if request_model_object:
                request_params["data"] = request_model_object.json()
                request_params["headers"] = {"Content-Type": "application/json"}
                
            resp = await self.__session.request(**request_params)
            resp_text = await resp.text()
            resp.raise_for_status() # raise after reading response text to get error messages.
        
        except (HTTPError, ClientResponseError) as http_err:
            raise APICommunicationError(message = resp_text) from http_err
        
        except (TimeoutError, ClientConnectorError) as error:
            self.__is_api_online = False
            print(f"API server is offline. {error}")
            raise APICommunicationError from error

        self.__is_api_online = True
        if (response_model_class):
            return response_model_class.parse_raw(resp_text)

    def get_is_api_online(self):
        """Returns: the status of the API server. 
                -True: online
                -False: offline
        """
        return self.__is_api_online
    
    def detect_faces(self,img: PngImageFile)->List[BoundingBox]:
        encoded_img_bytes = ImageTransferConverter().encode_img(img)
        req = DetectFacesRequest(encoded_img_bytes=encoded_img_bytes)

        res: DetectFacesResponse = self.__do_communication(api_endpoint="detect_faces",request_model_object=req,response_model_class=DetectFacesResponse)
        return res.face_bounding_boxes

    def recognize_face(self,img: PngImageFile)->UUID:
        encoded_img_bytes = ImageTransferConverter().encode_img(img)
        req = RecognizeFaceRequest(encoded_img_bytes=encoded_img_bytes)

        res: RecognizeFaceResponse = self.__do_communication(api_endpoint="recognize_face",request_model_object=req,response_model_class=RecognizeFaceResponse)
        return res.face_uuid