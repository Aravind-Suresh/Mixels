# Necessary modules imported
import numpy as np
import sys
import cv2

# Ensuring correct arguments
if not len(sys.argv) == 3:
	print "Usage : %s <input image> <output image>" % sys.argv[0]
	sys.exit()

class justaclass(object):
	pass

def getArea(item):
	return item.area

def distance(p0, p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

img = cv2.imread(sys.argv[1], 0)
arr = []

ret, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img1 = cv2.bitwise_and(img, otsu)
img2 = img1

# OpenCV 3.0.0				: _, contours, h
# OpenCV 2.4.11 and before	: contours, h
_, contours,hierarchy = cv2.findContours(otsu, 1, 2)

for cnt in contours:
	obj = justaclass()
	obj.area = cv2.contourArea(cnt)
	obj.rect = cv2.minAreaRect(cnt)
	obj.contour = cnt
	box = cv2.boxPoints(obj.rect)
	obj.box = np.int0(box)
	arr.append(obj)

sorted(arr, key=getArea)
ele = arr[len(arr)-1]
box = ele.box

#reduce epsilon till size is 4 or approx.size == 8
epsilon = 0.01

while(1):
	approx = cv2.approxPolyDP(ele.contour, epsilon, bool('true'))
	if approx.size == 8:
		break
	else:
		epsilon = epsilon*2

bdry = np.array([[approx[2][0][0], approx[2][0][1]], [approx[1][0][0], approx[1][0][1]], [approx[0][0][0], approx[0][0][1]], [approx[3][0][0], approx[3][0][1]]], dtype="int0")
# print bdry

cv2.drawContours(img1,[bdry],0,(255,255,255),2)

pts1 = np.float32(bdry)
pts = np.int32(bdry)
cv2.fillPoly(otsu, [pts], (255,255,255))
img1 = cv2.bitwise_and(img, otsu)
fx = distance(bdry[0],bdry[1])
fy = distance(bdry[1], bdry[2])
dimx = 600
dimy = (dimx*fy)/fx
pts2 = np.float32([[0,dimx-1],[0,0],[dimy-1,0],[dimy-1,dimx-1]])

M = cv2.getPerspectiveTransform(pts1,pts2)
img3 = cv2.warpPerspective(img1, M, (int(dimy),int(dimx)))

cv2.imwrite(sys.argv[2], img3)
