

# importing libararies
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import numpy as np
import argparse
import cv2 
from gtts import gTTS
import os
import speech_recognition as sr
from playsound import playsound
import ctypes
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
'''outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
#
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")
# Labels of Network.
classNames = { 'background':0,
    'aeroplane':1, 'bicycle':2 , 'bird': 3, 'boat':4,
    'bottle':5, 'bus':6, 'car':7, 'cat':8, 'chair':9,
    'cow':10, 'diningtable':11,  'dog':12,  'horse':13,
    'motorbike':14, 'person':15, 'pottedplant':16,
    'sheep':17, 'sofa':18, 'train':19,  'tvmonitor':20 }

def detect_image():
	find='bottle'   # or find = talk()
	find_id=classNames[find]
	vStream = VideoStream(src=0).start()
	global lock,classNames
	left=True
	down= True
	up=True
	right=True

	while True:

		# device screen
		user32 = ctypes.windll.user32
		height, width = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		
		# frames for a camera
		frame= vStream.read()
@app.route("/vidoe_stream")
def video_stream():
	return Response(genarate(), 
	mimetype='multipart/x-mixed-replace; boundary=frame')
'''

vStream = VideoStream(src=0).start()
outputFrame = None
lock = threading.Lock()

# Labels of Network.
classNames = { 'background':0,
    'aeroplane':1, 'bicycle':2 , 'bird': 3, 'boat':4,
    'bottle':5, 'bus':6, 'car':7, 'cat':8, 'chair':9,
    'cow':10, 'diningtable':11,  'dog':12,  'horse':13,
    'motorbike':14, 'person':15, 'pottedplant':16,
    'sheep':17, 'sofa':18, 'train':19,  'tvmonitor':20 }

net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt', 'MobileNetSSD_deploy.caffemodel')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def find():
	global vStream, outputFrame, lock , classNames
	user32 = ctypes.windll.user32
	left=True
	down= True
	up=True
	right=True
	find='bottle'   # or find = talk()
	find_id=classNames[find]
	while True:
		# window height and width
		# and resize camera
		width ,height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		frame= vStream.read()
		
		# resize frame for prediction
		frame_resized = cv2.resize(frame,(300,300)) 
		
		blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
		#Set to network the input blob 
		net.setInput(blob)
		#Prediction of network
		detections = net.forward()

		frame_resized = cv2.resize(frame,(600,600))
		cols = frame_resized.shape[1]
		rows = frame_resized.shape[0]

		cv2.putText(frame_resized, find, (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		for i in range(detections.shape[2]):
			confidence = detections[0, 0, i, 2] #Confidence of prediction

			if confidence > 0.75: #Filter prediction 
				class_id = int(detections[0, 0, i, 1]) #Class label
				if  class_id == find_id:

					# Object location 
					xLeftBottom = int(detections[0, 0, i, 3] * cols) 
					yLeftBottom = int(detections[0, 0, i, 4] * rows)
					xRightTop   = int(detections[0, 0, i, 5] * cols)
					yRightTop   = int(detections[0, 0, i, 6] * rows)

					# Centre
					xcentre=int((xRightTop+xLeftBottom)/2) 
					ycentre=int((yRightTop+yLeftBottom)/2)

					# Draw location of central square
					x_b= int((cols/2)-40) 
					x_t= int((cols/2)+40)
					#print(x_b>x_t)
					#print(xLeftBottom>xRightTop)
					y_r= int((rows/2)+40)
					y_l= int((rows/2)-40)

					frame_resized= cv2.rectangle(frame_resized, (x_t, y_l), (x_b, y_r),(0, 255, 0))

					# Draw location of object
					frame_resized= cv2.rectangle(frame_resized, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),(0, 255, 0))

					# Direction
					if xcentre > x_t or xcentre < x_b:
						if xcentre > x_t and right: 

							right= False
							left=True
							up=True
							down=True
							print('go right')
							file = "right.mp3"
							os.system("mpg123 " + file)
							playsound(file)
							break
		
						if xcentre < x_b and left:
							left= False
							right=True
							up=True
							down=True
							print('go left')
							file = "left.mp3"
							os.system("mpg123 " + file)
							playsound(file)
							break
						break

					if ycentre > y_r or ycentre < y_l:
						if ycentre < y_l and up:
							up= False
							left=True
							right=True
							down=True
							file = "up.mp3"
							os.system("mpg123 " + file)
							playsound(file)
							print('go up')
							break
			
						if ycentre > y_r and down:
							down= False
							up=True
							left=True
							right=True
					
							file = "down.mp3"
							os.system("mpg123 " + file)
							playsound(file)
				
							print('go down')
							break
						break

					if ycentre < y_r and ycentre > y_l and  xcentre < x_t and xcentre > x_b:
						#reset
						left=True
						right=True
						up=True
						down=True
						file = "stop.mp3"
						os.system("mpg123 " + file)
						playsound(file)

						print('stop')
					
					break
		frame=frame_resized
		with lock:
			outputFrame = frame.copy()

def gen():
	global outputFrame, lock
	while True:
		with lock: #check if frame is available
			if outputFrame is None:
				continue
			(flag,ecnImage)= cv2.imencode('.jpg',outputFrame) # image extension format
			if not flag:
				continue

		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +bytearray(ecnImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
	# start a thread that will perform motion detection
	t = threading.Thread(target=find)
	t.daemon = True
	t.start()
	app.run(host='127.0.0.7', port='8000', debug=True,
		threaded=True, use_reloader=False)
		
