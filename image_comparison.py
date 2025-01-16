import cv2
import numpy as np

def load_images(directory):
    images = {}
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            longitude, latitude = map(float, filename.rstrip('.png').split('_')[1:])
            images[(longitude, latitude)] = image
    return images

def find_best_match(input_image_path, images):
    input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    best_score = float('inf')
    best_coords = None
    for coords, image in images.items():
        result = cv2.matchTemplate(input_image, image, cv2.TM_SQDIFF)
        _, score, _, _ = cv2.minMaxLoc(result)
        if score < best_score:
            best_score = score
            best_coords = coords
    return best_coords, best_score
