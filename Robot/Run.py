from Camera import Camera
from Classified import Classified
import imutils
from collections import deque
import serial

cmr = Camera()

camera = cmr.camera
cv2 = cmr.ccv2
args = cmr.args

clsf = Classified()
clf1 = clsf.clf1
clf2 = clsf.clf2
#teensy = serial.Serial ("/dev/ttyACM0", 9600)

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (94, 80, 2)
colorUpper = (126, 255, 255)
pts = deque(maxlen=args["buffer"])

def calculateClassification():
	rects = [cv2.boundingRect(cnts) for cnt in cnts]
	print(rects)
	while cnts:
		rect = cv2.boundingRect(list(cnts))
		mode1=clf1.predict([rect[0], rect[1]])
		print (mode1)
		cnts = cnts.h_next()
		size = (rect[2]*rect[3])
		if size > 100:
                    pt1 = (rect[0],rect[1])
                    pt2 = (rect[0]+rect[2],rect[1]+rect[3])
                    cv2.Rectangle(img,pt1,pt2,(38,160,60))
	
def track():
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
	
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

def calculateRound():
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
	
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		#teensy.write("50M".encode())
		
		 
		# only proceed if the radius meets a minimum size
		if radius > 20:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), 1)
			#teensy.write("50M".encode())

while True:
	(grabbed, frame) = camera.read()
	frame = cv2.flip(frame, 1)

	if args.get("video") and not grabbed:
		break
	
	# resize the frame, inverted ("vertical flip" w/ 180degrees),
	# blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	frame = imutils.rotate(frame, angle=360)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
	
	
	center = None

	calculateClassification()


	calculateRound()

	pts.appendleft(center)

	track()

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
