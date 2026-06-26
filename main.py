import cv2
import numpy as np
import requests
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import serial
import time

url = '' #put your esp32-cam url

lower_blue = np.array([100, 100, 50])
upper_blue = np.array([130, 255, 255])

data = np.loadtxt('arm_data.txt', delimiter=',')

X = data[:, :2]
y = data[:, 2:]

model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X, y)

def predict_angles(cx, cy):
    pred = model.predict([[cx, cy]])[0]
    return tuple(int(round(v)) for v in pred)

def send_angles(s1, s2, s3):
    msg = f'{s1},{s2},{s3}\n'
    arduino.write(msg.encode())
    print(f'Sent: {msg.strip()}')

arduino = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)

while True:
    resp = requests.get(url, timeout=5)
    frame = cv2.imdecode(np.frombuffer(resp.content, dtype=np.uint8), cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 100:
            (x, y), radius = cv2.minEnclosingCircle(c)
            cx, cy = int(x), int(y)
            print(f'cx: {cx}, cy: {cy}')

            s1, s2, s3 = predict_angles(cx, cy)
            print(f's1: {s1}, s2: {s2}, s3: {s3}')

            send_angles(s1, s2, s3)

            time.sleep(15);
    else:
        break


arduino.close()
cv2.destroyAllWindows()
