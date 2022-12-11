import cv2
import numpy as np

def convert_to_gray(image: np.ndarray):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
