
import streamlit as st
from pathlib import Path
import os
# Assuming config and utils are available in your project structure
from config import load_config
from utils.logger import logger
from agents import ReverseEngineeringAgentManager
from utils.file_util import save_to_file
import yaml
import re
import base64

config = load_config()
logger = logger # Use your actual logger instance
agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
fs_agent = agent_manager.get_agent("generate_functional_spec")
base_dir=config['source_path']['base_dir_default']

def generate_functional_spec(source_code, section_type,filename_only):
    """Placeholder for generating functional specifications."""
    functional_spec_content = fs_agent.execute(
                                       code=source_code,
                                       section_type=section_type)
    
    print(f"base_dir: {base_dir}")
    target_file_path = str(Path(base_dir) / "output" / f"{filename_only}_{section_type}_FunctionalSpecification.md")
    save_to_file(target_file_path, functional_spec_content)


def read_files_in_directory(folder_path):
    """
    Lists all files in the given folder path and reads their content one by one.
    Args:
        folder_path (str): The path to the directory.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: The provided path '{folder_path}' is not a valid directory.")
        return

    print(f"Reading files from: {folder_path}\n")

    file_list = os.listdir(folder_path)
    return file_list
    

if __name__ == "__main__":
    #read code from a file
    source_code="""

    """
    section_type="extract_program_overview"
    folder_path=r"C:\KanagWS\CodeSpectreWS\code_extractor\controller_wise_code_snippets"
    file_list=read_files_in_directory(folder_path)
    if not file_list:
        print("No files found in the directory.")
    else:
        no_files=1
      
        for filename in file_list:
            #TODO TESTING
            # if no_files>1:
            #     break
            no_files+=1
            file_path = os.path.join(folder_path, filename)
            filename_only, _ = os.path.splitext(filename)
            # Check if it's a file (not a subdirectory)
            if os.path.isfile(file_path):
                print(f"--- Reading content of: {filename} ---")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"read file...")
                        # print(content)
                        output_file_path=generate_functional_spec(source_code=content,section_type=section_type,filename_only=filename_only)
                    print(f"--- End of {filename} ---\n")
                except Exception as e:
                    print(f"Error reading file {filename}: {e}\n")


    
    

