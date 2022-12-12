import { Component,ViewChild,ElementRef,OnInit } from '@angular/core';
import { NgxSpinnerService } from "ngx-spinner";

@Component({
  selector: 'app-web-cam',
  templateUrl: './web-cam.component.html',
  styleUrls: ['./web-cam.component.scss']
})
export class WebCamComponent implements OnInit{
  pc?: RTCPeerConnection
  videoElement?: HTMLVideoElement | null
  isLoading: boolean = false
  isPlaying: boolean = false
  errorMessage?: string //if an error occured displaying it!

  constructor(private spinner: NgxSpinnerService) {}

  ngOnInit() {
    /** spinner starts on init */
  }
  createPeerConnection(): void {
      this.pc = new RTCPeerConnection();
      const self = this;

      // connect audio / video
      this.pc.addEventListener('track',function(evt) {
        self.isPlaying = true;
        self.videoElement = <HTMLVideoElement>document.getElementById("videobox")
        self.videoElement.srcObject = evt.streams[0];
        self.isLoading = false;
      })
  }

  errorHappened(msg: string): void {
    this.isPlaying = false;
    this.isLoading = false;
    this.spinner.hide()
    this.errorMessage = msg;
  }

  negotiate(pc?: RTCPeerConnection) {
      return pc?.createOffer().then(function(offer) {
          return pc?.setLocalDescription(offer);
      }).then(function() {
          // wait for ICE gathering to complete
          return new Promise(function(resolve) {
              if (pc?.iceGatheringState === 'complete') {
                resolve("dummy");
              } else {
                  function checkState() {
                      if (pc?.iceGatheringState === 'complete') {
                          pc?.removeEventListener('icegatheringstatechange', checkState);
                          resolve("dummy");
                      }
                  }
                  pc?.addEventListener('icegatheringstatechange', checkState);
              }
          });
      }).then(function() {
          var offer = pc?.localDescription;
          //console.log(offer)
          return fetch('http://localhost:8080/offer', {
              body: JSON.stringify({
                  sdp: offer?.sdp,
                  type: offer?.type,
                  video_transform: 'none'
              }),
              headers: {
                  'Content-Type': 'application/json'
              },
              method: 'POST'
          });
      }).then(function(response) {
          return response.json();
      }).then(function(answer) {
          return pc?.setRemoteDescription(answer);
      }).catch(function(e) {
          alert(e);
      });
  }

  start(): void {
      this.isLoading = true
      this.spinner.show()
      this.errorMessage = undefined
      this.createPeerConnection()

      var negotiate = this.negotiate
      var pc = this.pc

      var constraints = {
          video : {
              width: 500,
              height: 500,
          }
      }
      navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
          stream.getTracks().forEach(function(track) {
              pc?.addTrack(track, stream);
          });
          return negotiate(pc);
      }, function(err) {
          alert('Could not acquire media: ' + err);
      });
    }

    stop() {
      this.isPlaying = false
      // loading-ot itt is bebillenteni, ha nem pillanatszerű a kikapcs!
      const pc = this.pc
      // close transceivers
      if (pc?.getTransceivers) {
          pc?.getTransceivers().forEach(function(transceiver) {
              if (transceiver.stop) {
                  transceiver.stop();
              }
          });
      }
      // close local audio / video
      pc?.getSenders().forEach(function(sender) {
          sender?.track?.stop();
      });
      // close peer connection
      setTimeout(function() {
         pc?.close();
      }, 500);
  }
}

