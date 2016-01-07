# Necessary modules imported
import numpy as np
import sys
import cv2

# Ensuring correct arguments
if not len(sys.argv) == 2:
	print "Usage : %s <input image>" % sys.argv[0]
	sys.exit()

img = cv2.imread(sys.argv[1])
imgC = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

rows, cols = gray.shape
gray = cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.equalizeHist(gray)

edge = cv2.Canny(gray, 40, 40)
cv2.imshow("edge", edge)

circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1.4, 50, minRadius = 10, maxRadius = 500)

if circles is not None:
	circles = np.uint8(circles[0, :])

	for (x, y, r) in circles:
		cv2.circle(img, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

	cv2.imshow("output", img)
	cv2.waitKey(0)

cv2.destroyAllWindows()
