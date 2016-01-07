# Necessary modules imported
import numpy as np
import sys
import cv2

# Ensuring correct arguments
if not len(sys.argv) == 2:
	print "Usage : %s <input image>" % sys.argv[0]
	sys.exit()

def dist(pt1, pt2):
	return np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

def process(pts):
	midPt = np.uint8(np.mean(pts, 0))

	ptsS = pts[1:, :]
	np.append(ptsS, pts[0])

	distM = [ dist(pts[:], ptsS[:]) ]
	idx = np.argmax(distM)
	pt1 = np.float32(pts[idx])
	pt2 = np.float32(ptsS[idx])

	return midPt, np.uint8(np.degrees(np.arctan((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))))


img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

rows, cols = gray.shape

gray = cv2.GaussianBlur(gray, (5, 5), 0)

ret, thresh = cv2.threshold(gray,127,255,1)

# OpenCV 3.0.0				: _, contours, h
# OpenCV 2.4.11 and before	: contours, h
_, contours, h = cv2.findContours(thresh,1,2)

totalArea = cols*rows

log = ""
ctr = 0

for cnt in contours:
	if cv2.contourArea(cnt) > 0.9*totalArea:
		continue

	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

	if len(approx)==4:
		ctr += 1
		midPt, theta = process(np.array(approx).reshape(-1, 2))
		log = log + str(midPt[0]) + ", " + str(midPt[1]) + ", " + str(theta) + '\n'
		color = np.random.randint(0, 255, 3)
		cv2.drawContours(img, [cnt], 0, color, -1)

print log.strip()

cv2.imshow('gray', gray)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
