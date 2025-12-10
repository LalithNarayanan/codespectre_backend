import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "source_path": {
            # "base_dir_parent": "C:/KanagWS/PythonWS1/code-conversion-wc/mainframe_code",
            # "base_dir": "",
            # "base_dir_default": "C:/KanagWS/PythonWS1/code-conversion-wc/mainframe_code/LTCHPPSPricerMFApp2021",
            # "proj_name_default": "LTCHPPSPricerMFApp2021",
            # "fs_consolidation_config_default": "C:/KanagWS/PythonWS1/code-conversion-wc/mf_modernization/processing_data/functional_specification_consolidation_config.yaml"
            "base_dir_parent": r"C:\SeenuWS\CodeSpectre\JavaSpringApplications",
            "base_dir": "",
            "base_dir_default": r"C:\SeenuWS\CodeSpectre\JavaSpringApplications",
            "proj_name_default": "LTCHPPSPricerMFApp2021",
            # "fs_consolidation_config_default": "C:/MainframeApplications/LTCHPPSPricerMFApp2021/config/functional_specification_consolidation_config.yaml"
  
        }
    }