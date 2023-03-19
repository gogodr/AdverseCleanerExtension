import numpy as np
import cv2

from cv2.ximgproc import guidedFilter

img = cv2.imread('input.png').astype(np.float32)

y = img.copy()
for _ in range(64):
    y = cv2.bilateralFilter(y, 5, 8, 8)
for _ in range(4):
    y = guidedFilter(img, y, 5, 16)

img = y.clip(0, 255).astype(np.uint8)
cv2.imwrite('output.png', img)
