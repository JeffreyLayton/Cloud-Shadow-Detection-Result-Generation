from PIL import Image
import numpy as np

def Quote(string):
    return ("\"" + string + "\"").replace("\\", "\\\\")

def delta(original,new):
    return (new / original) - 1.0

def mean(json):
    acc = 0.0
    count = 0
    for key, value in json.items():
        if(value is not None):
            count = count + 1
            acc = acc + value
    if count > 0:
        return acc / count
    return None

def load_binary_image(file_path):
    # Load binary image as grayscale with values >0 being True and 0 otherwise
    img = Image.open(file_path).convert("L")
    return np.array(img) > 0

def load_baseline_image(file_path):
    # Load RGBA image and set RGB values (0, 255, 0) as True and others as False
    img = Image.open(file_path).convert("RGBA")
    return np.all(np.array(img) == [0, 255, 0, 255], axis=-1)