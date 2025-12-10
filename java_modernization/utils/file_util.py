import os
import csv
from pathlib import Path
import shutil
import re
import pandas as pd
from datetime import datetime
from loguru import logger

def increment_copy_existing(target_file_path):
    if not os.path.exists(target_file_path):
        print(f"File not found: {target_file_path}")
        return

    base_dir, filename = os.path.split(target_file_path)
    filename_without_ext, ext = os.path.splitext(filename)
    # Find existing files with incremented suffixes
    existing_files = [f for f in os.listdir(base_dir) if f.startswith(filename_without_ext) and f != filename]
    max_number = 0
    for existing_file in existing_files:
        match = re.search(rf"{filename_without_ext}_(\d+){ext}", existing_file)
        if match:
            max_number = max(max_number, int(match.group(1)))

    new_number = max_number + 1
    while True:
        new_filename = f"{filename_without_ext}_{new_number}{ext}"
        new_file_path = os.path.join(base_dir, new_filename)

        if not os.path.exists(new_file_path):
            try:
                shutil.copy2(target_file_path, new_file_path)
                print(f"File copied to: {new_file_path}")
                break
            except Exception as e:
                print(f"Error copying file: {e}")
                break
        new_number += 1



#Save a file
def save_to_file(file_name,response):
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory and any necessary parents
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response)
        print(f"saved file_name:{file_name}")
 

#Read the file content for the given file
def read_program(base_dir, file_name):
    source_code=""
    file_name=f"{base_dir}\{file_name}"
    print(f"file_name:{file_name}")
    with open (file_name, "r") as file:
        source_code+f"## Content of the file :{file_name}" +"\n"
        source_code=file.read()
        source_code+="********************"
    return source_code

#File that contains the list of files to processed
def combine_files_at_directory(base_dir, file_name):
    combined_content = ""
    try:
        # file_name=r"C:\KanagWS\PythonWS\project\CBS-GenAI\cobol_pseudocode_details.csv"
        file_list=[]
        with open(file_name, mode="r", encoding='utf-8') as file:
            csv_reader=csv.DictReader(file)
            for row in csv_reader:
                if row['Action']=="PROCESS":
                    # print(f"Going to process this file:> {row["FileName"]}") 
                    file_list.append(row["FileName"])
                    # print(f"Processed:> {row["FileName"]}") 

            print(f"File List: {file_list}")
        for file in file_list:
            file_path = os.path.join(base_dir, file)
            # print(f"dependent file> {file_path}")

            with open(file_path, 'r') as f:
                combined_content += f"\n ## content of the file: {file_path} \n"
                combined_content += f.read() + "\n"
                combined_content += f"## End of the file: {file_path}\n"

    except FileNotFoundError:
        print(f"Error: Directory {base_dir} not found.")
    except IOError as e:
        print(f"Error: Couldn't read a file: {e}")
    except OSError as e:
        print(f"Error: OS error occured: {e}")
    return combined_content

# Combine all files content for the given base directory level.
def combine_files(base_dir, file_list):
    print(f"Combine: {base_dir} {file_list}")
    combined_content=""
    for file in file_list:
        try:
            file=f"{base_dir}\{file}"
            print(f"dependent file>{file}")
            with open(file,'r') as f:
                combined_content+= f"\n ## content of the file: {file} \n"
                combined_content+= f.read()+ "\n"
                combined_content+= f"## End of the file: {file}\n"
        except FileNotFoundError:
            print(f"Error: File {file} not found ")
        except IOError:
            print(f"Error: Couldn't read the {file}" )
    return combined_content

#Read and combine the contents ofthe files present in the csv file
def combine_files_contents_from_csv(csv_file_path, base_directory):
    """Reads file paths from a CSV, combines their content, and returns a string."""

    try:
        df = pd.read_csv(csv_file_path, header=None)  # No header in your CSV
        # print(f"df=>>>>>>>>>>>:{df}")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
        return None

    combined_content = ""

    for relative_file_path in df[0]:  # The file paths are in the first (and only) column
        full_file_path = base_directory / Path(relative_file_path.strip())  # Construct full path
        if full_file_path.exists() and full_file_path.is_file():
            try:
                with open(full_file_path, "r", encoding="utf-8") as f: #Explicit encoding to handle potential issues.
                    combined_content +="Content of the file:: " + str(full_file_path) + "\n"
                    combined_content += f.read() + "\n\n"  # Add content and separators
            except Exception as e:
                print(f"Error reading {full_file_path}: {e}")
                return None
        else:
            print(f"File not found: {full_file_path}")
            return None

    return combined_content

#Get file counts
def get_file_line_counts(directory,include_pattern="ALL"):
    try:
        file_line_counts = {}
        for filename in os.listdir(directory):
           if "_response" in filename:
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):  # Check if it's a file
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                        line_count = 0
                        for line in file:
                            line_count += 1
                        file_line_counts[filename] = line_count
           else:
               print(f"{filename} is ignored")
        
        print(f"file_line_counts:{file_line_counts}")
        return file_line_counts
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def write_to_csv(data, output_filename):
    try:
        with open(output_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["FileName", "LineCount","Action"])  # Write header row
            for filename, line_count in data.items():
                writer.writerow([filename, line_count,"PROCESS"])
        print(f"Data written to {output_filename}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def write_job_data_to_csv(job_data,file_name):
    """
    Writes job-related data from a dictionary to a CSV file.
    Args:
        job_data (dict): A dictionary containing the job details with the following keys:
                          'job_id', 'prompt_name', 'prompt_template', 'unit',
                          'input', 'output_type', 'output_file', 'output_value'.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = ["job_id", "time_stamp","llm_model_name","llm_processing_time","overall_processing_time", "prompt_name", "prompt_template", "unit", "input", "output_type", "output_file", "output_value"]
    row_data = [job_data.get('job_id', ''),
            timestamp,
            job_data.get('llm_model_name', 'gemini'),
            job_data.get('llm_processing_time', ''),
            job_data.get('overall_processing_time', ''),
            job_data.get('prompt_name', ''),
            job_data.get('prompt_template', ''),
            job_data.get('unit', ''),
            job_data.get('input', ''),
            job_data.get('output_type', ''),
            job_data.get('output_file', ''),
            job_data.get('output_value', '')]

    try:
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(header)
            writer.writerow(row_data)
        logger.debug(f"Data for job ID '{job_data.get('job_id')}' written to job_data.csv")
    except Exception as e:
        logger.error(f"An error occurred while writing to CSV: {e}")




if __name__ == "__main__":
    print("Executing file util..")
    # print("="*40)
    # Example usage:
    # directory_path = r"C:\KanagWS\PythonWS\project\CBS-GenAI\cobol_programs\source"  # Replace with your directory path
    # output_csv_filename = r"C:\KanagWS\PythonWS\project\CBS-GenAI\cobol_program_details.csv"

    # directory_path = r"C:\KanagWS\PythonWS\project\CBS-GenAI\cobol_programs\pseudocode"  # Replace with your directory path
    # output_csv_filename = r"C:\KanagWS\PythonWS\project\CBS-GenAI\cobol_pseudocode_details.csv"
    # include_pattern="_response"
    # result = get_file_line_counts(directory_path,include_pattern)
    # if result:
    #     write_to_csv(result, output_csv_filename)

    # file_name=rf"C:\KanagWS\PythonWS1\code-conversion-wc\mainframe_code\LTCHPPSPricerMFApp2021\output\job_details.csv"
    # Example Usage:
    # job_info = {
    #     'job_id': "job_123",
    #     'prompt_name': "summarize_article",
    #     'prompt_template': "Summarize the following article: {article_text}",
    #     'unit': "words",
    #     'input': "This is a sample article text that needs to be summarized.",
    #     'output_type': "text",
    #     'output_file': "summary.txt",
    #     'output_value': "This article was summarized..."
    # }
    # write_job_data_to_csv(job_info,file_name)

    # job_info_2 = {
    #     'job_id': "job_456",
    #     'prompt_name': "translate_to_french",
    #     'prompt_template': "Translate '{english_text}' to French.",
    #     'unit': "tokens",
    #     'input': "Hello, world!",
    #     'output_type': "text",
    #     'output_file': "french_translation.txt",
    #     'output_value': "Bonjour le monde!"
    # }
    # write_job_data_to_csv(job_info_2,file_name)