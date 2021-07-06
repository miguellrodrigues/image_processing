import cv2
import numpy as np

window = cv2.namedWindow("output", cv2.WINDOW_NORMAL)
img = cv2.imread("../images/white_dots.png")

blurred = cv2.GaussianBlur(img, (11, 11), 0)
thresh = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)

k = np.ones(shape=(3, 3))

thresh = cv2.erode(thresh, k, (-1, -1), iterations=2)
thresh = cv2.dilate(thresh, k, (-1, -1), iterations=4)

mask = cv2.inRange(thresh, np.array([0, 0, 200]), np.array([180, 255, 255]))

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

i = 0
for contour in contours:
    center_moment = cv2.moments(contour)

    center_x = int(center_moment['m10'] / center_moment['m00'])
    center_y = int(center_moment['m01'] / center_moment['m00'])

    # (x, y, w, h) = cv2.boundingRect(contour)
    # ((cX, cY), radius) = cv2.minEnclosingCircle(contour)
    #
    # cv2.circle(img, (int(cX), int(cY)), int(radius),
    #            (0, 0, 255), 3)
    # cv2.putText(img, "{}".format(i + 1), (x, y - 15),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    #
    # i += 1

    cv2.line(img, (center_x, center_y + 5), (center_x, center_y - 5), (0, 0, 255), 2)
    cv2.line(img, (center_x + 5, center_y), (center_x - 5, center_y), (0, 0, 255), 2)

cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

# def draw_circle(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img, (x, y), 10, (255, 255, 255), -1)
#
#
# cv2.setMouseCallback("output", draw_circle)
#
# while(1):
#     cv2.imshow('output',img)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 27:
#         break

cv2.imshow("output", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
