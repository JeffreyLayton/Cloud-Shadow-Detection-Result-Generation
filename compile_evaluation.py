
import json
import os
from helpers import *


def compile_evaluation():
    current_path = os.getcwd()
    data_path = os.path.join(current_path, "data") 
    output_path = os.path.join(current_path, "output")

    eval_json = {}
    eval_json["Permutation Counts"] = {
        "F - FFT": 0.0, 
        "F - FTF": 0.0,
        "F - FTT": 0.0,
        "F - TFF": 0.0,
        "F - TFT": 0.0,
        "F - TTF": 0.0,
        "F - TTT": 0.0,
        "T - FFF": 0.0,
        "T - FFT": 0.0,
        "T - FTF": 0.0,
        "T - FTT": 0.0,
        "T - TFF": 0.0,
        "T - TFT": 0.0,
        "T - TTF": 0.0,
        "T - TTT": 0.0
    } 
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
    ave_perm = np.zeros((0,0))
    i = 0
    for set_dir in os.listdir(output_path):
        data_set_path = os.path.join(data_path, set_dir)
        output_set_path = os.path.join(output_path, set_dir)
        if not os.path.isdir(output_set_path):
            continue

        with open(os.path.join(output_set_path, "EvaluationMetric.json"), 'r') as f_i:
            f_i_data = json.load(f_i)

        _id = f_i_data["ID"]

        if f_i_data["Baselined"] :
            CM_image = load_binary_image(os.path.join(output_set_path, "CM.tif"))
            PSM_image = load_binary_image(os.path.join(output_set_path, "PSM.tif"))
            OSM_image = load_binary_image(os.path.join(output_set_path, "OSM.tif"))
            FSM_image = load_binary_image(os.path.join(output_set_path, "FSM.tif"))
            SB_image = load_baseline_image(os.path.join(data_set_path, "shadowBaseline.tif"))

            permutations = np.zeros((16,), dtype=float)
            cloud_image_inv = CM_image == False
            npixels = np.sum(cloud_image_inv)
            for tru_i in range(2):
                for pot_i in range(2):
                    for obj_i in range(2):
                        for fin_i in range(2):
                            is_part =           (SB_image      == bool(tru_i))
                            is_part = is_part & (PSM_image == bool(pot_i))
                            is_part = is_part & (OSM_image == bool(obj_i))
                            is_part = is_part & (FSM_image == bool(fin_i))
                            is_part = is_part & cloud_image_inv
                            count = np.sum(is_part)
                            index = tru_i * 8 + pot_i * 4 + obj_i * 2 + fin_i
                            permutations[index] = count / npixels
            if i == 0:
                ave_perm = np.array([permutations])
            else :
                ave_perm = np.append(ave_perm, [permutations], axis=0)

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
            i = i + 1

    ave_perm = np.mean(ave_perm, axis=0)

    eval_json["Permutation Counts"]["F - FFF"] = ave_perm[0]
    eval_json["Permutation Counts"]["F - FFT"] = ave_perm[1]
    eval_json["Permutation Counts"]["F - FTF"] = ave_perm[2]
    eval_json["Permutation Counts"]["F - FTT"] = ave_perm[3]
    eval_json["Permutation Counts"]["F - TFF"] = ave_perm[4]
    eval_json["Permutation Counts"]["F - TFT"] = ave_perm[5]
    eval_json["Permutation Counts"]["F - TTF"] = ave_perm[6]
    eval_json["Permutation Counts"]["F - TTT"] = ave_perm[7]

    eval_json["Permutation Counts"]["T - FFF"] = ave_perm[8]
    eval_json["Permutation Counts"]["T - FFT"] = ave_perm[9]
    eval_json["Permutation Counts"]["T - FTF"] = ave_perm[10]
    eval_json["Permutation Counts"]["T - FTT"] = ave_perm[11]
    eval_json["Permutation Counts"]["T - TFF"] = ave_perm[12]
    eval_json["Permutation Counts"]["T - TFT"] = ave_perm[13]
    eval_json["Permutation Counts"]["T - TTF"] = ave_perm[14]
    eval_json["Permutation Counts"]["T - TTT"] = ave_perm[15]

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
    with open(os.path.join(output_path, "EvaluationMetric_compiled.json"), 'w') as f_o:
        json.dump(eval_json, f_o)

if __name__ == "__main__":
    print("Runing compiling results...")
    compile_evaluation()
    print("Complete compiling results...")