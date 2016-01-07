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
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

totalArea = cols*rows

if np.mean(thresh) > 127:
	thresh = 255 - thresh

dt = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dt,0.1*dt.max(),255,0)
dt = np.uint8(dt)
sure_fg = np.uint8(sure_fg)

# cv2.imshow("thresh", thresh)
# cv2.imshow("fg", sure_fg)
# cv2.imshow("dt", dt)

_, contours, h = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, 2)

count = 0

for cnt in contours:
	area = cv2.contourArea(cnt)
	(x,y), radius = cv2.minEnclosingCircle(cnt)
	areaC = np.pi*radius*radius
	dev = np.abs(area - areaC)/areaC
	if dev > 0.3:
		continue
	count += 1
	# print area, areaC
	color = np.random.randint(0, 255, 3)
	cv2.drawContours(img, [cnt], 0, color, -1)

print count
# cv2.waitKey(0)
# cv2.destroyAllWindows()
