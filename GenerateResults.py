import os, subprocess, json

print("Starting results script...")

current_path    = os.getcwd()
executable_dir  = current_path + "\\out\\build\\x64-Release"
executable_path = executable_dir + "\\Cloud-Shadow-Detection.exe"

input_root_dir  = os.getcwd() + "\\Tests"
output_root_dir = os.getcwd() + "\\Tests-Results"

input_dirs = []
output_dirs = []

def Quote(string):
    return ("\"" + string + "\"").replace("\\", "\\\\")

print("Compiling inputs...")
for dir in os.listdir(input_root_dir):
    if os.path.isdir(input_root_dir + "\\" + dir):
        print("Adding test in path: " + input_root_dir + "\\" + dir)
        input_dirs.append(input_root_dir + "\\" + dir)
        output_dirs.append(output_root_dir + "\\" + dir)

print("Executing Shadow detection...")
for i in range(len(input_dirs)):
    print("Executing test: " + Quote(input_dirs[i]) + " and outputing to: " + Quote(output_dirs[i]))
    subprocess.run([executable_path, "-e", "-f", "--input_dir=" + Quote(input_dirs[i]), "--output_dir=" + Quote(output_dirs[i])], cwd=executable_dir)

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
eval_json["D-PSM-OSM"] = {
    "FP-R": {"Mean": 0.0, "Values": {}}
    , "FN-R": {"Mean": 0.0, "Values": {}}
    , "F-R": {"Mean": 0.0, "Values": {}}
    , "FP-T": {"Mean": 0.0, "Values": {}}
    , "FN-T": {"Mean": 0.0, "Values": {}}
    , "F-T": {"Mean": 0.0, "Values": {}}
    , "U": {"Mean": 0.0, "Values": {}}
    , "P": {"Mean": 0.0, "Values": {}}
}
eval_json["D-OSM-FSM"] = {
    "FP-R": {"Mean": 0.0, "Values": {}}
    , "FN-R": {"Mean": 0.0, "Values": {}}
    , "F-R": {"Mean": 0.0, "Values": {}}
    , "FP-T": {"Mean": 0.0, "Values": {}}
    , "FN-T": {"Mean": 0.0, "Values": {}}
    , "F-T": {"Mean": 0.0, "Values": {}}
    , "U": {"Mean": 0.0, "Values": {}}
    , "P": {"Mean": 0.0, "Values": {}}
}
eval_json["D-PSM-FSM"] = {
    "FP-R": {"Mean": 0.0, "Values": {}}
    , "FN-R": {"Mean": 0.0, "Values": {}}
    , "F-R": {"Mean": 0.0, "Values": {}}
    , "FP-T": {"Mean": 0.0, "Values": {}}
    , "FN-T": {"Mean": 0.0, "Values": {}}
    , "F-T": {"Mean": 0.0, "Values": {}}
    , "U": {"Mean": 0.0, "Values": {}}
    , "P": {"Mean": 0.0, "Values": {}}
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

print("Evaluating and Compiling Shadow Detection results...")
for i in range(len(output_dirs)):
    print("Opening Evaluation: " + output_dirs[i] + "...")
    with open(output_dirs[i] + "\\" + "evaluation.json", 'r') as f_i:
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

        eval_json["D-PSM-OSM"]["FP-R"]["Values"][_id] = delta(eval_json["PSM"]["FP-R"]["Values"][_id], eval_json["OSM"]["FP-R"]["Values"][_id])
        eval_json["D-PSM-OSM"]["FN-R"]["Values"][_id] = delta(eval_json["PSM"]["FN-R"]["Values"][_id], eval_json["OSM"]["FN-R"]["Values"][_id])
        eval_json["D-PSM-OSM"]["F-R"]["Values"][_id] = delta(eval_json["PSM"]["F-R"]["Values"][_id], eval_json["OSM"]["F-R"]["Values"][_id])
        eval_json["D-PSM-OSM"]["FP-T"]["Values"][_id] = delta(eval_json["PSM"]["FP-T"]["Values"][_id], eval_json["OSM"]["FP-T"]["Values"][_id])
        eval_json["D-PSM-OSM"]["FN-T"]["Values"][_id] = delta(eval_json["PSM"]["FN-T"]["Values"][_id], eval_json["OSM"]["FN-T"]["Values"][_id])
        eval_json["D-PSM-OSM"]["F-T"]["Values"][_id] = delta(eval_json["PSM"]["F-T"]["Values"][_id], eval_json["OSM"]["F-T"]["Values"][_id])
        eval_json["D-PSM-OSM"]["U"]["Values"][_id] = delta(eval_json["PSM"]["U"]["Values"][_id], eval_json["OSM"]["U"]["Values"][_id])
        eval_json["D-PSM-OSM"]["P"]["Values"][_id] = delta(eval_json["PSM"]["P"]["Values"][_id], eval_json["OSM"]["P"]["Values"][_id])

        eval_json["D-OSM-FSM"]["FP-R"]["Values"][_id] = delta(eval_json["OSM"]["FP-R"]["Values"][_id], eval_json["FSM"]["FP-R"]["Values"][_id])
        eval_json["D-OSM-FSM"]["FN-R"]["Values"][_id] = delta(eval_json["OSM"]["FN-R"]["Values"][_id], eval_json["FSM"]["FN-R"]["Values"][_id])
        eval_json["D-OSM-FSM"]["F-R"]["Values"][_id] = delta(eval_json["OSM"]["F-R"]["Values"][_id], eval_json["FSM"]["F-R"]["Values"][_id])
        eval_json["D-OSM-FSM"]["FP-T"]["Values"][_id] = delta(eval_json["OSM"]["FP-T"]["Values"][_id], eval_json["FSM"]["FP-T"]["Values"][_id])
        eval_json["D-OSM-FSM"]["FN-T"]["Values"][_id] = delta(eval_json["OSM"]["FN-T"]["Values"][_id], eval_json["FSM"]["FN-T"]["Values"][_id])
        eval_json["D-OSM-FSM"]["F-T"]["Values"][_id] = delta(eval_json["OSM"]["F-T"]["Values"][_id], eval_json["FSM"]["F-T"]["Values"][_id])
        eval_json["D-OSM-FSM"]["U"]["Values"][_id] = delta(eval_json["OSM"]["U"]["Values"][_id], eval_json["FSM"]["U"]["Values"][_id])
        eval_json["D-OSM-FSM"]["P"]["Values"][_id] = delta(eval_json["OSM"]["P"]["Values"][_id], eval_json["FSM"]["P"]["Values"][_id])

        eval_json["D-PSM-FSM"]["FP-R"]["Values"][_id] = delta(eval_json["PSM"]["FP-R"]["Values"][_id], eval_json["FSM"]["FP-R"]["Values"][_id])
        eval_json["D-PSM-FSM"]["FN-R"]["Values"][_id] = delta(eval_json["PSM"]["FN-R"]["Values"][_id], eval_json["FSM"]["FN-R"]["Values"][_id])
        eval_json["D-PSM-FSM"]["F-R"]["Values"][_id] = delta(eval_json["PSM"]["F-R"]["Values"][_id], eval_json["FSM"]["F-R"]["Values"][_id])
        eval_json["D-PSM-FSM"]["FP-T"]["Values"][_id] = delta(eval_json["PSM"]["FP-T"]["Values"][_id], eval_json["FSM"]["FP-T"]["Values"][_id])
        eval_json["D-PSM-FSM"]["FN-T"]["Values"][_id] = delta(eval_json["PSM"]["FN-T"]["Values"][_id], eval_json["FSM"]["FN-T"]["Values"][_id])
        eval_json["D-PSM-FSM"]["F-T"]["Values"][_id] = delta(eval_json["PSM"]["F-T"]["Values"][_id], eval_json["FSM"]["F-T"]["Values"][_id])
        eval_json["D-PSM-FSM"]["U"]["Values"][_id] = delta(eval_json["PSM"]["U"]["Values"][_id], eval_json["FSM"]["U"]["Values"][_id])
        eval_json["D-PSM-FSM"]["P"]["Values"][_id] = delta(eval_json["PSM"]["P"]["Values"][_id], eval_json["FSM"]["P"]["Values"][_id])

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

eval_json["D-PSM-OSM"]["FP-R"]["Mean"] = mean(eval_json["D-PSM-OSM"]["FP-R"]["Values"])
eval_json["D-PSM-OSM"]["FN-R"]["Mean"] = mean(eval_json["D-PSM-OSM"]["FN-R"]["Values"])
eval_json["D-PSM-OSM"]["F-R"]["Mean"] = mean(eval_json["D-PSM-OSM"]["F-R"]["Values"])
eval_json["D-PSM-OSM"]["FP-T"]["Mean"] = mean(eval_json["D-PSM-OSM"]["FP-T"]["Values"])
eval_json["D-PSM-OSM"]["FN-T"]["Mean"] = mean(eval_json["D-PSM-OSM"]["FN-T"]["Values"])
eval_json["D-PSM-OSM"]["F-T"]["Mean"] = mean(eval_json["D-PSM-OSM"]["F-T"]["Values"])
eval_json["D-PSM-OSM"]["U"]["Mean"] = mean(eval_json["D-PSM-OSM"]["U"]["Values"])
eval_json["D-PSM-OSM"]["P"]["Mean"] = mean(eval_json["D-PSM-OSM"]["P"]["Values"])

eval_json["D-OSM-FSM"]["FP-R"]["Mean"] = mean(eval_json["D-OSM-FSM"]["FP-R"]["Values"])
eval_json["D-OSM-FSM"]["FN-R"]["Mean"] = mean(eval_json["D-OSM-FSM"]["FN-R"]["Values"])
eval_json["D-OSM-FSM"]["F-R"]["Mean"] = mean(eval_json["D-OSM-FSM"]["F-R"]["Values"])
eval_json["D-OSM-FSM"]["FP-T"]["Mean"] = mean(eval_json["D-OSM-FSM"]["FP-T"]["Values"])
eval_json["D-OSM-FSM"]["FN-T"]["Mean"] = mean(eval_json["D-OSM-FSM"]["FN-T"]["Values"])
eval_json["D-OSM-FSM"]["F-T"]["Mean"] = mean(eval_json["D-OSM-FSM"]["F-T"]["Values"])
eval_json["D-OSM-FSM"]["U"]["Mean"] = mean(eval_json["D-OSM-FSM"]["U"]["Values"])
eval_json["D-OSM-FSM"]["P"]["Mean"] = mean(eval_json["D-OSM-FSM"]["P"]["Values"])

eval_json["D-PSM-FSM"]["FP-R"]["Mean"] = mean(eval_json["D-PSM-FSM"]["FP-R"]["Values"])
eval_json["D-PSM-FSM"]["FN-R"]["Mean"] = mean(eval_json["D-PSM-FSM"]["FN-R"]["Values"])
eval_json["D-PSM-FSM"]["F-R"]["Mean"] = mean(eval_json["D-PSM-FSM"]["F-R"]["Values"])
eval_json["D-PSM-FSM"]["FP-T"]["Mean"] = mean(eval_json["D-PSM-FSM"]["FP-T"]["Values"])
eval_json["D-PSM-FSM"]["FN-T"]["Mean"] = mean(eval_json["D-PSM-FSM"]["FN-T"]["Values"])
eval_json["D-PSM-FSM"]["F-T"]["Mean"] = mean(eval_json["D-PSM-FSM"]["F-T"]["Values"])
eval_json["D-PSM-FSM"]["U"]["Mean"] = mean(eval_json["D-PSM-FSM"]["U"]["Values"])
eval_json["D-PSM-FSM"]["P"]["Mean"] = mean(eval_json["D-PSM-FSM"]["P"]["Values"])

print("Saving compiled results")
with open(output_root_dir + "\\" + "evaluation_compilation.json", 'w') as f_o:
    json.dump(eval_json, f_o)
    
