import json
import os
import tomlkit

def setup():
    current_path = os.getcwd()
    data_path = os.path.join(current_path, "data")
    setting_path = os.path.join(current_path, "settings")
    output_path = os.path.join(current_path, "output")
    
    #Generate the environment
    if not os.path.exists(data_path):
        raise FileNotFoundError("No data folder present")
    
    if not os.path.exists(setting_path):
        os.makedirs(setting_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for set_dir in os.listdir(data_path):
        data_set_path = os.path.join(data_path, set_dir)
        setting_set_path = os.path.join(setting_path, set_dir)
        output_set_path = os.path.join(output_path, set_dir)

        request_json = os.path.join(data_set_path, "request.json")
        if not os.path.exists(request_json):
            raise FileNotFoundError("No request file found")
        with open(request_json, 'r') as json_file:
            request = json.load(json_file)
        bbox_data = request["payload"]["input"]["bounds"]["bbox"]

        if not os.path.exists(setting_set_path):
            os.makedirs(setting_set_path)
        if not os.path.exists(output_set_path):
            os.makedirs(output_set_path)

        data_toml = tomlkit.document()

        data_table = tomlkit.table()
        data_table.add("ID", "test_data_" + set_dir)
        data_table.add("bbox", bbox_data)

        NIR_path = os.path.join(data_set_path, "B08.tif")
        if not os.path.exists(NIR_path):
            raise FileNotFoundError("No file found")
        data_table.add("NIR_path", NIR_path)

        CLP_path = os.path.join(data_set_path, "CLP.tif")
        if not os.path.exists(CLP_path):
            raise FileNotFoundError("No file found")
        data_table.add("CLP_path", CLP_path)

        CLD_path = os.path.join(data_set_path, "CLD.tif")
        if not os.path.exists(CLD_path):
            raise FileNotFoundError("No file found")
        data_table.add("CLD_path", CLD_path)

        ViewZenith_path = os.path.join(data_set_path, "viewZenithMean.tif")
        if not os.path.exists(ViewZenith_path):
            raise FileNotFoundError("No file found")
        data_table.add("ViewZenith_path", ViewZenith_path)

        ViewAzimuth_path = os.path.join(data_set_path, "viewAzimuthMean.tif")
        if not os.path.exists(ViewAzimuth_path):
            raise FileNotFoundError("No file found")
        data_table.add("ViewAzimuth_path", ViewAzimuth_path)

        SunZenith_path = os.path.join(data_set_path, "sunZenithAngles.tif")
        if not os.path.exists(SunZenith_path):
            raise FileNotFoundError("No file found")
        data_table.add("SunZenith_path", SunZenith_path)

        SunAzimuth_path = os.path.join(data_set_path, "sunAzimuthAngles.tif")
        if not os.path.exists(SunAzimuth_path):
            raise FileNotFoundError("No file found")
        data_table.add("SunAzimuth_path", SunAzimuth_path)

        SCL_path = os.path.join(data_set_path, "SCL.tif")
        if not os.path.exists(SCL_path):
            raise FileNotFoundError("No file found")
        data_table.add("SCL_path", SCL_path)

        RBGA_path = os.path.join(data_set_path, "RGB.tif")
        if not os.path.exists(RBGA_path):
            raise FileNotFoundError("No file found")
        data_table.add("RBGA_path", RBGA_path)

        ShadowBaseline_path = os.path.join(data_set_path, "shadowBaseline.tif")
        if os.path.exists(ShadowBaseline_path):
            data_table.add("ShadowBaseline_path", ShadowBaseline_path)

        data_toml["Data"] = data_table
        tomlkit.dumps(data_toml)
        data_toml_path = os.path.join(setting_set_path ,"data.toml")
        with open(data_toml_path, "w+") as f:
            f.write(data_toml.as_string())
            f.flush()
            os.fsync(f.fileno())   

        full_output_toml = tomlkit.document()
        full_output_table = tomlkit.table()

        CM_path = os.path.join(output_set_path, "CM.tif")
        full_output_table.add("CM_path", CM_path)
        
        PSM_path = os.path.join(output_set_path, "PSM.tif")
        full_output_table.add("PSM_path", PSM_path)
        
        OSM_path = os.path.join(output_set_path, "OSM.tif")
        full_output_table.add("OSM_path", OSM_path)

        FSM_path = os.path.join(output_set_path, "FSM.tif")
        full_output_table.add("FSM_path", FSM_path)

        Alpha_path = os.path.join(output_set_path, "Alpha.tif")
        full_output_table.add("Alpha_path", Alpha_path)

        Beta_path = os.path.join(output_set_path, "Beta.tif")
        full_output_table.add("Beta_path", Beta_path)

        PSME_path = os.path.join(output_set_path, "PSME.tif")
        full_output_table.add("PSME_path", PSME_path)

        OSME_path = os.path.join(output_set_path, "OSME.tif")
        full_output_table.add("OSME_path", OSME_path)

        FSME_path = os.path.join(output_set_path, "FSME.tif")
        full_output_table.add("FSME_path", FSME_path)

        EvaluationMetric_path = os.path.join(output_set_path, "EvaluationMetric.json")
        full_output_table.add("EvaluationMetric_path", EvaluationMetric_path)

        HeightVariationMetric_path = os.path.join(output_set_path, "HeightVariationMetric.json")
        full_output_table.add("HeightVariationMetric_path", HeightVariationMetric_path)

        full_output_toml["Output"] = full_output_table
        tomlkit.dumps(full_output_toml)
        full_output_toml_path = os.path.join(setting_set_path, "full_output.toml")
        with open(full_output_toml_path, "w+") as f:
            f.write(full_output_toml.as_string())
            f.flush()
            os.fsync(f.fileno())           
        
if __name__ == "__main__":
    print("Running Setup...")
    setup()
    print("Complete Setup...")