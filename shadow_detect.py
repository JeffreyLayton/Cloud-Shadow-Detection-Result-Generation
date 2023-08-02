
import json
import os
import subprocess
from helpers import *


def shadow_detect(root_path, executable_name):
    executable_path = os.path.join(root_path, executable_name)

    current_path = os.getcwd()
    data_path = os.path.join(current_path, "data")
    setting_path = os.path.join(current_path, "settings")
    output_path = os.path.join(current_path, "output")

    for set_dir in os.listdir(data_path):
        setting_set_toml_path = os.path.join(setting_path, set_dir, "data.toml")
        output_set_toml_path = os.path.join(output_path, set_dir, "full_output.toml")
        subprocess.run([executable_path, "--data_path=" + Quote(setting_set_toml_path), "--output_path=" + Quote(output_set_toml_path)], cwd=root_path)

if __name__ == "__main__":
    print("Running shadow detection...")

    current_path = os.getcwd()
    generate_settings_path = os.path.join(current_path, "generate_settings.json")
    with open(generate_settings_path, 'r') as f:
        settings = json.load(f)
    executable_dir  = settings['Executable Directory Path']
    executable_name = settings['Executable Name']
    shadow_detect(executable_dir, executable_name)
    print("Complete shadow detection...")