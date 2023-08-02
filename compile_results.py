
import json
import os
from helpers import *


def complile_results():
    current_path = os.getcwd()
    output_path = os.path.join(current_path, "output")

    eval_json = {}
    for set_dir in os.listdir(output_path):
        with open(os.path.join(output_path, set_dir, "EvaluationMetric.json"), 'r') as f_i:
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
    with open(os.path.join(output_path, "EvaluationMetric_compiled.json"), 'w') as f_o:
        json.dump(eval_json, f_o)

if __name__ == "__main__":
    print("Running Setup...")
    complile_results()
    print("Complete Setup...")