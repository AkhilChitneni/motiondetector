import cv2, time, pandas
from datetime import datetime


first_frame = None
status_list = [None,None]
times = []
df = pandas.DataFrame(columns=["Start","End"])

video = cv2.VideoCapture(0)
while True:
    check,frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta,None,iterations=2)

    (_,ctns,_)=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in ctns:
        if cv2.contourArea(contour)<1000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),((x+w),(y+h)),(0,0,200),3)
    status_list.append(status)
    status_list=status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Color",frame)
    cv2.imshow("Delta frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_delta)

    key = cv2.waitKey(1)
    if 0<key<256:
        if(status==1):
            times.append(datetime.now())
        break
print(times)
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("akhil.csv" ,sep='\t', encoding='utf-8')
video.release()
cv2.destroyAllWindows()
