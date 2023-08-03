import json
import os

import numpy as np
from helpers import *


def compile_height_variation():
    current_path = os.getcwd()
    output_path = os.path.join(current_path, "output")

    heights = np.zeros(0)
    dots = np.zeros((0,0))
    i = 0
    for set_dir in os.listdir(output_path):
        output_set_path = os.path.join(output_path, set_dir)
        if not os.path.isdir(output_set_path):
            continue
        json_file_path = os.path.join(output_set_path, "HeightVariationMetric.json")
        with open(json_file_path, 'r') as f:
            series_data = json.load(f)['m_ave_dot_series']
        if i == 0:
            heights = np.array([item["Height"] for item in series_data])
            dots = np.array([[item["Average Dot Product"] for item in series_data]])
        else :
            dots = np.append(dots, [[item["Average Dot Product"] for item in series_data]], axis=0)
        i = i + 1
    ave_dot = np.mean(dots, axis=0)

    eval_json = {}
    eval_json["m_ave_dot_series"] = [{"Height" : heights[i], "Average Dot Product" : ave_dot[i]} for i in range(len(heights))]
    with open(os.path.join(output_path, "HeightVariationMetric_compiled.json"), 'w') as f_o:
        json.dump(eval_json, f_o)


if __name__ == "__main__":
    print("Runing compiling height variation...")
    compile_height_variation()
    print("Complete compiling height variation...")