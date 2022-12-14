import cv2   #include opencv library functions in python
from app.Application import Application



vidcap = cv2.VideoCapture(0)
app = Application()

while(vidcap.isOpened()):
    ret, frame = vidcap.read() 

    if ret:
            app.update_frame(frame)
            cv2.imshow("Frame",frame) 
            # fps = vidcap.get(cv2.CAP_PROP_FPS)
            # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # exiting gracefully :3
                app.close_processing_thread()
                break
    else:
        print("Unable to open frame")
else:
    print("Cannot open camera")