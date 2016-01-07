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

rows, cols = gray.shape
gray = cv2.GaussianBlur(gray, (5, 5), 0)

circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)

if circles is not None:
	circles = np.round(circles[0, :]).astype("int")

	for (x, y, r) in circles:
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

	cv2.imshow("output", np.hstack([image, output]))
	cv2.waitKey(0)
