import cv2   #include opencv library functions in python
from app.Application import Application



vidcap = cv2.VideoCapture(0)
app = Application()

while(vidcap.isOpened()):
    ret, frame = vidcap.read() 

    if ret:
            app.process_frame(frame)
            cv2.imshow("Frame",frame) 
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("Unable to open frame")
else:
    print("Cannot open camera")