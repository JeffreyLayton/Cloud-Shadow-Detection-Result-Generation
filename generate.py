import os, subprocess, json


def Quote(string):
    return ("\"" + string + "\"").replace("\\", "\\\\")

print("Starting results script...")

current_path    = os.getcwd()

settings_file = open('generate_settings.json')
settings = json.load(settings_file)
settings_file.close()

executable_dir  = settings['Executable Directory Path']
executable_name = settings['Executable Name']
height_variation_executable_name = settings['Height Variation Executable Name']
executable_path = os.path.join(executable_dir, executable_name)
height_variation_executable_path = os.path.join(executable_dir, height_variation_executable_name)

print("Executable Path: " + executable_path)

dat_eval_root_dir = os.path.join(current_path, 'data\\evaluation')
dat_addi_root_dir = os.path.join(current_path, 'data\\additional')
res_eval_root_dir = os.path.join(current_path, 'results\\evaluation')
res_addi_root_dir = os.path.join(current_path, 'results\\additional')

if not os.path.exists(res_eval_root_dir):
   os.makedirs(res_eval_root_dir)

input_eval_dirs = []
output_eval_dirs = []

input_addi_dirs = []
output_addi_dirs = []

print("Compiling inputs...")
for sub_dir in os.listdir(dat_eval_root_dir):
    data_dir = os.path.join(dat_eval_root_dir, sub_dir)
    if os.path.isdir(data_dir):
        results_dir = os.path.join(res_eval_root_dir, sub_dir)
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        print("----Adding evaluation set to inputs: " + sub_dir)
        input_eval_dirs.append(data_dir)
        output_eval_dirs.append(results_dir)

for sub_dir in os.listdir(dat_addi_root_dir):
    data_dir = os.path.join(dat_addi_root_dir, sub_dir)
    if os.path.isdir(data_dir):
        results_dir = os.path.join(res_addi_root_dir, sub_dir)
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        print("----Adding additional set to inputs: " + sub_dir)
        input_addi_dirs.append(data_dir)
        output_addi_dirs.append(results_dir)

print("Executing shadow detection...")
for i in range(len(input_eval_dirs)):
    print("----Executing input: " + Quote(input_eval_dirs[i]) + " and outputing to: " + Quote(output_eval_dirs[i]))
    subprocess.run([executable_path, "-e", "-f", "--input_dir=" + Quote(input_eval_dirs[i]), "--output_dir=" + Quote(output_eval_dirs[i])], cwd=executable_dir)
    subprocess.run([height_variation_executable_path, "--input_dir=" + Quote(input_eval_dirs[i]), "--output_dir=" + Quote(output_eval_dirs[i])], cwd=executable_dir)
for i in range(len(input_addi_dirs)):
    print("----Executing input: " + Quote(input_addi_dirs[i]) + " and outputing to: " + Quote(output_addi_dirs[i]))
    subprocess.run([executable_path, "-f", "--input_dir=" + Quote(input_addi_dirs[i]), "--output_dir=" + Quote(output_addi_dirs[i])], cwd=executable_dir)
    subprocess.run([height_variation_executable_path, "--input_dir=" + Quote(input_addi_dirs[i]), "--output_dir=" + Quote(input_addi_dirs[i])], cwd=executable_dir)

eval_json = {}
#Information Regarding Sun and View Position
eval_json["SUN"]  = {"Mean": 0.0, "Values": {}}
eval_json["VIEW"] = {"Mean": 0.0, "Values": {}}
#Information Regarding at each stage
eval_json["PSM"]  = {
    "FP-R": {"Mean": 0.0, "Values": {}}
    , "FN-R": {"Mean": 0.0, "Values": {}}
    , "F-R": {"Mean": 0.0, "Values": {}}
    , "FP-T": {"Mean": 0.0, "Values": {}}
    , "FN-T": {"Mean": 0.0, "Values": {}}
    , "F-T": {"Mean": 0.0, "Values": {}}
    , "U": {"Mean": 0.0, "Values": {}}
    , "P": {"Mean": 0.0, "Values": {}}
}
eval_json["OSM"]  = {
    "FP-R": {"Mean": 0.0, "Values": {}}
    , "FN-R": {"Mean": 0.0, "Values": {}}
    , "F-R": {"Mean": 0.0, "Values": {}}
    , "FP-T": {"Mean": 0.0, "Values": {}}
    , "FN-T": {"Mean": 0.0, "Values": {}}
    , "F-T": {"Mean": 0.0, "Values": {}}
    , "U": {"Mean": 0.0, "Values": {}}
    , "P": {"Mean": 0.0, "Values": {}}
}
eval_json["FSM"]  = {
    "FP-R": {"Mean": 0.0, "Values": {}}
    , "FN-R": {"Mean": 0.0, "Values": {}}
    , "F-R": {"Mean": 0.0, "Values": {}}
    , "FP-T": {"Mean": 0.0, "Values": {}}
    , "FN-T": {"Mean": 0.0, "Values": {}}
    , "F-T": {"Mean": 0.0, "Values": {}}
    , "U": {"Mean": 0.0, "Values": {}}
    , "P": {"Mean": 0.0, "Values": {}}
}
#Information Regarding change between stage
eval_json["D-M-PSM-OSM"] = {
      "FP-R":  0.0
    , "FN-R":  0.0
    , "F-R":  0.0
    , "FP-T":  0.0
    , "FN-T":  0.0
    , "F-T":  0.0
    , "U":  0.0
    , "P":  0.0
}
eval_json["D-M-OSM-FSM"] = {
      "FP-R":  0.0
    , "FN-R":  0.0
    , "F-R":  0.0
    , "FP-T":  0.0
    , "FN-T":  0.0
    , "F-T":  0.0
    , "U":  0.0
    , "P":  0.0
}
eval_json["D-M-PSM-FSM"] = {
      "FP-R":  0.0
    , "FN-R":  0.0
    , "F-R":  0.0
    , "FP-T":  0.0
    , "FN-T":  0.0
    , "F-T":  0.0
    , "U":  0.0
    , "P":  0.0
}

def delta(original,new):
    return (new / original) - 1.0

def mean(json):
    acc = 0.0
    count = 0
    for key, value in json.items():
        count = count + 1
        acc = acc + value
    return acc / count

print("Compiling results...")
for i in range(len(output_eval_dirs)):
    print("----Opening Evaluation: " + output_eval_dirs[i] + "...")
    with open(os.path.join(output_eval_dirs[i], 'evaluation.json'), 'r') as f_i:
        f_i_data = json.load(f_i)
        _id = f_i_data["ID"]

        eval_json["SUN"]["Values"][_id] = f_i_data["Sun"]["Average Dot Product"]
        eval_json["VIEW"]["Values"][_id] = f_i_data["View"]["Average Dot Product"]

        eval_json["PSM"]["FP-R"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["False Positives Relative to Shadow Pixels"]
        eval_json["PSM"]["FN-R"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["False Negatives Relative to Shadow Pixels"]
        eval_json["PSM"]["F-R"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["False Pixels Relative to Shadow Pixels"]
        eval_json["PSM"]["FP-T"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["False Positives Relative to Total Pixels"]
        eval_json["PSM"]["FN-T"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["False Negatives Relative to Total Pixels"]
        eval_json["PSM"]["F-T"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["False Pixels Relative to Total Pixels"]
        eval_json["PSM"]["U"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["Users Accuracy"]
        eval_json["PSM"]["P"]["Values"][_id] = f_i_data["Potential Shadow Mask"]["Producers Accuracy"]

        eval_json["OSM"]["FP-R"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["False Positives Relative to Shadow Pixels"]
        eval_json["OSM"]["FN-R"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["False Negatives Relative to Shadow Pixels"]
        eval_json["OSM"]["F-R"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["False Pixels Relative to Shadow Pixels"]
        eval_json["OSM"]["FP-T"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["False Positives Relative to Total Pixels"]
        eval_json["OSM"]["FN-T"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["False Negatives Relative to Total Pixels"]
        eval_json["OSM"]["F-T"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["False Pixels Relative to Total Pixels"]
        eval_json["OSM"]["U"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["Users Accuracy"]
        eval_json["OSM"]["P"]["Values"][_id] = f_i_data["Object-based Shadow Mask"]["Producers Accuracy"]

        eval_json["FSM"]["FP-R"]["Values"][_id] = f_i_data["Final Shadow Mask"]["False Positives Relative to Shadow Pixels"]
        eval_json["FSM"]["FN-R"]["Values"][_id] = f_i_data["Final Shadow Mask"]["False Negatives Relative to Shadow Pixels"]
        eval_json["FSM"]["F-R"]["Values"][_id] = f_i_data["Final Shadow Mask"]["False Pixels Relative to Shadow Pixels"]
        eval_json["FSM"]["FP-T"]["Values"][_id] = f_i_data["Final Shadow Mask"]["False Positives Relative to Total Pixels"]
        eval_json["FSM"]["FN-T"]["Values"][_id] = f_i_data["Final Shadow Mask"]["False Negatives Relative to Total Pixels"]
        eval_json["FSM"]["F-T"]["Values"][_id] = f_i_data["Final Shadow Mask"]["False Pixels Relative to Total Pixels"]
        eval_json["FSM"]["U"]["Values"][_id] = f_i_data["Final Shadow Mask"]["Users Accuracy"]
        eval_json["FSM"]["P"]["Values"][_id] = f_i_data["Final Shadow Mask"]["Producers Accuracy"]

eval_json["SUN"]["Mean"] = mean(eval_json["SUN"]["Values"])
eval_json["VIEW"]["Mean"] = mean(eval_json["VIEW"]["Values"])

eval_json["PSM"]["FP-R"]["Mean"] = mean(eval_json["PSM"]["FP-R"]["Values"])
eval_json["PSM"]["FN-R"]["Mean"] = mean(eval_json["PSM"]["FN-R"]["Values"])
eval_json["PSM"]["F-R"]["Mean"] = mean(eval_json["PSM"]["F-R"]["Values"])
eval_json["PSM"]["FP-T"]["Mean"] = mean(eval_json["PSM"]["FP-T"]["Values"])
eval_json["PSM"]["FN-T"]["Mean"] = mean(eval_json["PSM"]["FN-T"]["Values"])
eval_json["PSM"]["F-T"]["Mean"] = mean(eval_json["PSM"]["F-T"]["Values"])
eval_json["PSM"]["U"]["Mean"] = mean(eval_json["PSM"]["U"]["Values"])
eval_json["PSM"]["P"]["Mean"] = mean(eval_json["PSM"]["P"]["Values"])

eval_json["OSM"]["FP-R"]["Mean"] = mean(eval_json["OSM"]["FP-R"]["Values"])
eval_json["OSM"]["FN-R"]["Mean"] = mean(eval_json["OSM"]["FN-R"]["Values"])
eval_json["OSM"]["F-R"]["Mean"] = mean(eval_json["OSM"]["F-R"]["Values"])
eval_json["OSM"]["FP-T"]["Mean"] = mean(eval_json["OSM"]["FP-T"]["Values"])
eval_json["OSM"]["FN-T"]["Mean"] = mean(eval_json["OSM"]["FN-T"]["Values"])
eval_json["OSM"]["F-T"]["Mean"] = mean(eval_json["OSM"]["F-T"]["Values"])
eval_json["OSM"]["U"]["Mean"] = mean(eval_json["OSM"]["U"]["Values"])
eval_json["OSM"]["P"]["Mean"] = mean(eval_json["OSM"]["P"]["Values"])

eval_json["FSM"]["FP-R"]["Mean"] = mean(eval_json["FSM"]["FP-R"]["Values"])
eval_json["FSM"]["FN-R"]["Mean"] = mean(eval_json["FSM"]["FN-R"]["Values"])
eval_json["FSM"]["F-R"]["Mean"] = mean(eval_json["FSM"]["F-R"]["Values"])
eval_json["FSM"]["FP-T"]["Mean"] = mean(eval_json["FSM"]["FP-T"]["Values"])
eval_json["FSM"]["FN-T"]["Mean"] = mean(eval_json["FSM"]["FN-T"]["Values"])
eval_json["FSM"]["F-T"]["Mean"] = mean(eval_json["FSM"]["F-T"]["Values"])
eval_json["FSM"]["U"]["Mean"] = mean(eval_json["FSM"]["U"]["Values"])
eval_json["FSM"]["P"]["Mean"] = mean(eval_json["FSM"]["P"]["Values"])

eval_json["D-M-PSM-OSM"]["FP-R"] = delta(eval_json["PSM"]["FP-R"]["Mean"], eval_json["OSM"]["FP-R"]["Mean"])
eval_json["D-M-PSM-OSM"]["FN-R"] = delta(eval_json["PSM"]["FN-R"]["Mean"], eval_json["OSM"]["FN-R"]["Mean"])
eval_json["D-M-PSM-OSM"]["F-R"] = delta(eval_json["PSM"]["F-R"]["Mean"], eval_json["OSM"]["F-R"]["Mean"])
eval_json["D-M-PSM-OSM"]["FP-T"] = delta(eval_json["PSM"]["FP-T"]["Mean"], eval_json["OSM"]["FP-T"]["Mean"])
eval_json["D-M-PSM-OSM"]["FN-T"] = delta(eval_json["PSM"]["FN-T"]["Mean"], eval_json["OSM"]["FN-T"]["Mean"])
eval_json["D-M-PSM-OSM"]["F-T"] = delta(eval_json["PSM"]["F-T"]["Mean"], eval_json["OSM"]["F-T"]["Mean"])
eval_json["D-M-PSM-OSM"]["U"] = delta(eval_json["PSM"]["U"]["Mean"], eval_json["OSM"]["U"]["Mean"])
eval_json["D-M-PSM-OSM"]["P"] = delta(eval_json["PSM"]["P"]["Mean"], eval_json["OSM"]["P"]["Mean"])

eval_json["D-M-OSM-FSM"]["FP-R"] = delta(eval_json["OSM"]["FP-R"]["Mean"], eval_json["FSM"]["FP-R"]["Mean"])
eval_json["D-M-OSM-FSM"]["FN-R"] = delta(eval_json["OSM"]["FN-R"]["Mean"], eval_json["FSM"]["FN-R"]["Mean"])
eval_json["D-M-OSM-FSM"]["F-R"] = delta(eval_json["OSM"]["F-R"]["Mean"], eval_json["FSM"]["F-R"]["Mean"])
eval_json["D-M-OSM-FSM"]["FP-T"] = delta(eval_json["OSM"]["FP-T"]["Mean"], eval_json["FSM"]["FP-T"]["Mean"])
eval_json["D-M-OSM-FSM"]["FN-T"] = delta(eval_json["OSM"]["FN-T"]["Mean"], eval_json["FSM"]["FN-T"]["Mean"])
eval_json["D-M-OSM-FSM"]["F-T"] = delta(eval_json["OSM"]["F-T"]["Mean"], eval_json["FSM"]["F-T"]["Mean"])
eval_json["D-M-OSM-FSM"]["U"] = delta(eval_json["OSM"]["U"]["Mean"], eval_json["FSM"]["U"]["Mean"])
eval_json["D-M-OSM-FSM"]["P"] = delta(eval_json["OSM"]["P"]["Mean"], eval_json["FSM"]["P"]["Mean"])

eval_json["D-M-PSM-FSM"]["FP-R"] = delta(eval_json["PSM"]["FP-R"]["Mean"], eval_json["FSM"]["FP-R"]["Mean"])
eval_json["D-M-PSM-FSM"]["FN-R"] = delta(eval_json["PSM"]["FN-R"]["Mean"], eval_json["FSM"]["FN-R"]["Mean"])
eval_json["D-M-PSM-FSM"]["F-R"] = delta(eval_json["PSM"]["F-R"]["Mean"], eval_json["FSM"]["F-R"]["Mean"])
eval_json["D-M-PSM-FSM"]["FP-T"] = delta(eval_json["PSM"]["FP-T"]["Mean"], eval_json["FSM"]["FP-T"]["Mean"])
eval_json["D-M-PSM-FSM"]["FN-T"] = delta(eval_json["PSM"]["FN-T"]["Mean"], eval_json["FSM"]["FN-T"]["Mean"])
eval_json["D-M-PSM-FSM"]["F-T"] = delta(eval_json["PSM"]["F-T"]["Mean"], eval_json["FSM"]["F-T"]["Mean"])
eval_json["D-M-PSM-FSM"]["U"] = delta(eval_json["PSM"]["U"]["Mean"], eval_json["FSM"]["U"]["Mean"])
eval_json["D-M-PSM-FSM"]["P"] = delta(eval_json["PSM"]["P"]["Mean"], eval_json["FSM"]["P"]["Mean"])
                                                     
print("Saving compiled results...")
with open(os.path.join(res_eval_root_dir, 'evaluation_compilation.json'), 'w') as f_o:
    json.dump(eval_json, f_o)
    
print("Finished...")