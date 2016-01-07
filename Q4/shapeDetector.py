# Necessary modules imported
import numpy as np
import sys
import cv2

# Ensuring correct arguments
if not len(sys.argv) == 2:
	print "Usage : %s <input image>" % sys.argv[0]
	sys.exit()

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (5, 5), 0)

ret, thresh = cv2.threshold(gray, 127, 255, 1)
if np.mean(thresh) > 127:
	thresh = 255 - thresh

# OpenCV 3.0.0				: _, contours, h
# OpenCV 2.4.11 and before	: contours, h
_, contours, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)

count = [0] * 20

for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
	count[len(approx)] += 1
	color = np.random.randint(0, 255, 3)
	cv2.drawContours(img, [cnt], 0, color, -1)

for idx in range(0, len(count)):
	if count[idx] == 0:
		continue
	print str(idx) + " - " + str(count[idx])

# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
