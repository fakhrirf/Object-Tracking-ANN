'''
Object detection ("Ball tracking") with OpenCV
    Adapted from the original code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

# import the necessary packages
#from collections import deque
import numpy as np
import argparse
#import imutils
import cv2
import serial

class Camera:

	camera = None
	ccv2 = cv2
	args = None
	

	def __init__(self):
		#teensy = serial.Serial ("/dev/ttyACM0", 9600)

		# construct the argument parse and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-v", "--video",
			help="path to the (optional) video file")
		ap.add_argument("-b", "--buffer", type=int, default=64,
			help="max buffer size")
		args = vars(ap.parse_args())
		self.args = args
		 
		# if a video path was not supplied, grab the reference
		# to the webcam
		if not args.get("video", False):
			camera = cv2.VideoCapture(0)
		 
		# otherwise, grab a reference to the video file
		else:
			camera = cv2.VideoCapture(args["video"])
		
		self.camera = camera
	 
