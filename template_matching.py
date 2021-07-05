import cv2
import numpy as np

ultrasound_image = cv2.imread("images/template_matching.png", cv2.IMREAD_UNCHANGED)
pattern_image = cv2.imread("images/pattern.png")

h = pattern_image.shape[0]
w = pattern_image.shape[1]

# Template Matching
# TM_CCOEFF
# TM_CCOEFF_NORMED
# TM_CCORR
# TM_CCORR_NORMED
# TM_SQDIFF
# TM_SQDIFF_NORMED
# https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html

result = cv2.matchTemplate(
    ultrasound_image,
    pattern_image,
    cv2.TM_CCOEFF_NORMED
)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(min_val, max_val, min_loc, max_loc)

threshold = .8
y_loc, x_loc = np.where(result >= threshold)

for (x, y) in zip(x_loc, y_loc):
    cv2.rectangle(ultrasound_image, (x, y), (x + w, y + h), (0, 255, 255), 2)

cv2.imshow("output", ultrasound_image)
cv2.waitKey(0)

# rectangles = []
# for (x, y) in zip(x_loc, y_loc):
#     rectangles.append([int(x), int(y), int(w), int(h)])
#     rectangles.append([int(x), int(y), int(w), int(h)])
#
# rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

