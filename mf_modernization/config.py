# import os
# from dotenv import load_dotenv

# def load_config():
#     load_dotenv()
#     return {
#         "source_path": {
#             # "base_dir_parent": "C:/KanagWS/PythonWS1/code-conversion-wc/mainframe_code",
#             # "base_dir": "",
#             # "base_dir_default": "C:/KanagWS/PythonWS1/code-conversion-wc/mainframe_code/LTCHPPSPricerMFApp2021",
#             # "proj_name_default": "LTCHPPSPricerMFApp2021",
#             # "fs_consolidation_config_default": "C:/KanagWS/PythonWS1/code-conversion-wc/mf_modernization/processing_data/functional_specification_consolidation_config.yaml"
#             "base_dir_parent": r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications",
#             "base_dir": "",
#             "base_dir_default": r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021",
#             "proj_name_default": "LTCHPPSPricerMFApp2021",
#             "fs_consolidation_config_default": r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\config\functional_specification_consolidation_config.yaml"
  
#         }
#     }




# config.py
import os
from dotenv import load_dotenv
from pathlib import Path


def load_config():
    load_dotenv()
    
    config = {
        "source_path": {
            "base_dir_parent": r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications",
            "base_dir": "",
            "base_dir_default": r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021",
            "proj_name_default": "LTCHPPSPricerMFApp2021",
            "fs_consolidation_config_default": r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\config\functional_specification_consolidation_config.yaml"
            # "base_dir_parent": r"C:\Users\2786986\Documents\codespectre_backend\MainframeApplications",
            # "base_dir": "",
            # "base_dir_default": r"C:\Users\2786986\Documents\codeSpectre_backend\MainframeApplications\LTCHPPSPricerMFApp2021",
            # "proj_name_default": "LTCHPPSPricerMFApp2021",
            # "fs_consolidation_config_default": r"C:\Users\2786986\Documents\codeSpectre_backend\MainframeApplications\LTCHPPSPricerMFApp2021\config\functional_specification_consolidation_config.yaml"

        },
        
        # ✅ Platform-specific configurations
        "platforms": {
            "mainframe": {
                "display_name": "Mainframe",
                "output_dir": "mainframe_specifications",
                "source_extensions": [".cbl", ".jcl", ".cpy", ""],
                "source_subdir": "source_code"
            },
            "sas": {
                "display_name": "SAS",
                "output_dir": "sas_specifications",
                "source_extensions": [".sas", ""],
                "source_subdir": "sas_programs"
            },
            "java": {
                "display_name": "Java",
                "output_dir": "java_specifications",
                "source_extensions": [".java", ""],
                "source_subdir": "java_src"
            }
        }
    }
    
    # ✅ DYNAMIC helper functions (access base_dir_default from config)
    def get_output_dir(platform):
        platform_cfg = config["platforms"].get(platform)
        if not platform_cfg:
            raise ValueError(f"Unsupported platform: {platform}")
        base_dir = config["source_path"]["base_dir_default"]
        return str(Path(base_dir) / "output" / platform_cfg["output_dir"])
    
    def get_pdf_dir(platform):
        platform_cfg = config["platforms"].get(platform)
        if not platform_cfg:
            raise ValueError(f"Unsupported platform: {platform}")
        base_dir = config["source_path"]["base_dir_default"]
        return str(Path(base_dir) / "output" / platform_cfg["output_dir"] / "pdfs")
    
    def get_source_dir(platform):
        platform_cfg = config["platforms"].get(platform)
        if not platform_cfg:
            raise ValueError(f"Unsupported platform: {platform}")
        base_dir = config["source_path"]["base_dir_default"]
        return str(Path(base_dir) / platform_cfg["source_subdir"])
    
    # Add helper functions to config
    config["get_output_dir"] = get_output_dir
    config["get_pdf_dir"] = get_pdf_dir
    config["get_source_dir"] = get_source_dir
    
    return config
