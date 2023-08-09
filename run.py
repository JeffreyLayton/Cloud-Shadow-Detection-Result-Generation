import json
import os
import subprocess


def run(data_set_dir_name):
    current_path = os.getcwd()

    generate_settings_path = os.path.join(current_path, "generate_settings.json")
    with open(generate_settings_path, 'r') as f:
        settings = json.load(f)
    executable_dir  = settings['Executable Directory Path']
    executable_name = settings['Executable Name']
    executable_path = os.path.join(executable_dir, executable_name)

    setting_set_toml_path = os.path.join(current_path, "settings", data_set_dir_name, "data.toml")
    subprocess.run([executable_path, "-g" ,"--data_path=" + setting_set_toml_path], cwd=executable_dir)