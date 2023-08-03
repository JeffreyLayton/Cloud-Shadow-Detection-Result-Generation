import json
import shutil
import os

from setup import setup
from shadow_detect import shadow_detect
from height_variation import height_variation
from compile_evaluation import compile_evaluation
from compile_height_variation import compile_height_variation


#Script to run
current_path = os.getcwd()
data_path = os.path.join(current_path, "data")
setting_path = os.path.join(current_path, "settings")
output_path = os.path.join(current_path, "output")

if os.path.exists(setting_path):
    shutil.rmtree(setting_path)

if os.path.exists(output_path):
    shutil.rmtree(output_path)

generate_settings_path = os.path.join(current_path, "generate_settings.json")
with open(generate_settings_path, 'r') as f:
    settings = json.load(f)
executable_dir  = settings['Executable Directory Path']
shadow_detection_name = settings['Executable Name']
height_variation_name = settings['Height Variation Executable Name']

setup()
shadow_detect(executable_dir, shadow_detection_name)
height_variation(executable_dir, height_variation_name)
compile_evaluation()
compile_height_variation()