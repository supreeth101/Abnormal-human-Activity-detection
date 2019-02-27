import numpy as np
import cv2
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

Sec = 0
Min = 0
Check = 1
Counter = 1

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #if ret is True:
     #           gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #else:
    #    continue
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)     

    if len(faces) > 0:  

        Sec += 1
        print(str(Min) + " Mins " + str(Sec) + " Sec ")

        cv2.putText(img, "Time: " + str(Min) + " Mins " + str(Sec) + " Sec ", (0,img.shape[0] -30), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)
        cv2.putText(img, "Number of faces detected: " + str(faces.shape[0]), (0,img.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)    

        time.sleep(1)
        if Sec == 60:
            Sec = 0
            Min += 1
            print(str(Min) + " Minute")

        if Min == 2:
            print("Alert")
            if Check == 1:
                import http.client
                conn = http.client.HTTPConnection("api.msg91.com")
                payload = "{ \"sender\": \"ATMAUT\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Suspicious activity detected inside ATM.\", \"to\": [ \"9677104366\"] } ] }"
                headers = {'authkey': "209349Aqh8iTXUN1Of5accca05",'content-type': "application/json"}
                conn.request("POST", "/api/v2/sendsms", payload, headers)
                res = conn.getresponse()
                data = res.read()
                print(data.decode("utf-8"))
                Check += 1   

    if len(faces) > 2 and Counter == 1:
        import http.client
        conn = http.client.HTTPConnection("api.msg91.com")
        payload = "{ \"sender\": \"SRMVDP\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Suspicious activity detected inside SRM VDP ATM.\", \"to\": [ \"9551631252\"] } ] }"
        headers = {'authkey': "209349Aqh8iTXUN1Of5accca05",'content-type': "application/json"}
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        Counter += 1

                   
    if len(faces) == 0:

        print('No face detected')
        cv2.putText(img, "No face detected ", (0,img.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)        
        Sec = 0
        Min = 0

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break    

cap.release()
cv2.destroyAllWindows()
