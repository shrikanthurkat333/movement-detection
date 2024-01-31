import cv2
import imutils
import threading
import winsound
#set camera
camera_capture=cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH,720)
camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
'''a
start frame and caluclate difffrence of other frame
'''
_, start_frame=camera_capture.read()#_ beacuse we wont use that
start_frame=imutils.resize(start_frame,width=500)
start_frame=cv2.cvtColor(start_frame,cv2.COLOR_BGR2GRAY)
start_frame=cv2.GaussianBlur(start_frame,(25,25),0)

alarm=False
alarm_mode=False
alarm_counter=0
def activate_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("Intrusion Detected")
        winsound.Beep(3000,500)#frequency and time
    alarm=False

while True:
    _,frame=camera_capture.read()
    frame=imutils.resize(frame,width=500)
    if alarm_mode:
        frame_bw=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_bw=cv2.GaussianBlur(frame_bw,(5,5),0)

        frame_diffrence=cv2.absdiff(frame_bw,start_frame)
        threshold=cv2.threshold(frame_diffrence,25,255,cv2.THRESH_BINARY)[1]
        start_frame=frame_bw

        if threshold.sum()>300:#sensitiveity
            alarm_counter+=1
        else:
            if alarm_counter>0:
                alarm_counter-=1
        
        cv2.imshow("Cam",threshold)
    else:
        cv2.imshow("Cam",frame)
    if alarm_counter>20:
        if not alarm:
            alarm=True
            threading.Thread(target=activate_alarm).start()
    key_pressed=cv2.waitKey(20)
    if key_pressed==ord('a'):
        alarm_mode=not alarm_mode
        alarm_counter=0
    if key_pressed==ord('e'):
        alarm_mode=False
        break

camera_capture.release()
cv2.destroyAllWindows()

