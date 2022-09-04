import numpy as np
import cv2
import utils

img_height, img_width = utils.HEIGHT, utils.WIDTH
n_channels = 4
transparent_img = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)
transparent_img[round(img_height/2), round(img_width/2)] = (0, 0, 0, 1)

# Save the image for visualization
cv2.imwrite(utils.TRANSPARENT_PATH + 'transparent.png', transparent_img)