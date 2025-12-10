import os
import streamlit as st
import os
import zipfile
from io import BytesIO

def extract_and_zip_files(text):
    """
    Extracts content following '###FilePath:', saves it to individual files,
    creates a ZIP archive of the created files, and provides a download link.

    Args:
        text: A string containing one or more blocks of content
              preceded by '###FilePath:'.
    """
    files_to_zip = []  # List to store paths of created files
    if "###FilePath:" in text:
        blocks = text.split("###FilePath:")
        for block in blocks:
            if block.strip():
                lines = block.strip().split('\n')
                file_path_line = lines[0].strip()
                content = "\n".join(lines[1:])

                if file_path_line:
                    file_path = file_path_line.strip()
                    file_name, file_extension = os.path.splitext(file_path)

                    if file_extension:
                        # Create the directory if it doesn't exist
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        try:
                            with open(file_path, 'w') as f:
                                f.write(content)
                            print(f"Content written to: {file_path}")
                            files_to_zip.append(file_path)  # Add to the list of files to zip
                        except Exception as e:
                            print(f"Error writing to {file_path}: {e}")
                    else:
                        print(f"Could not determine file extension for: {file_path}")
    else:
        print("No '###FilePath:' blocks found in the input text.")
        return  # Exit if no files were processed

    # Create a ZIP file in memory
    if files_to_zip:
        memory_zip = BytesIO()
        with zipfile.ZipFile(memory_zip, 'w') as zipf:
            for file_path in files_to_zip:
                try:
                    zipf.write(file_path, os.path.basename(file_path))  # Use basename to avoid full paths in the zip
                    print(f"Added {file_path} to ZIP")
                except Exception as e:
                    print(f"Error adding {file_path} to ZIP: {e}")

        memory_zip.seek(0)  # Reset the buffer position to the beginning

        # Provide a download link for the ZIP file
        st.download_button(
            label="Download Files as ZIP",
            data=memory_zip,
            file_name="generated_files.zip",
            mime="application/zip",
            help="Click to download the generated files in a ZIP archive.",
        )
        print("ZIP file download link provided.")

        # Clean up the created files (optional)
        for file_path in files_to_zip:
            try:
                os.remove(file_path)
                print(f"Deleted temporary file: {file_path}")
            except Exception as e:
                print(f"Error deleting temporary file {file_path}: {e}")
    else:
        st.info("No files were generated to create a ZIP archive.")
    
def extract_and_save_content(text):
    """
    Extracts content following '###FilePath:' and saves it to a file,
    creating the necessary directories if they don't exist.

    Args:
        text: A string containing one or more blocks of content
              preceded by '###FilePath:'.
    """
    if "###FilePath:" in text:
        blocks = text.split("###FilePath:")
        for block in blocks:
            if block.strip():
                lines = block.strip().split('\n')
                file_path_line = lines[0].strip()
                content = "\n".join(lines[1:])

                if file_path_line:
                    file_path = file_path_line.strip()
                    file_name, file_extension = os.path.splitext(file_path)

                    if file_extension:
                        # Create the directory if it doesn't exist
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        try:
                            with open(file_path, 'w') as f:
                                f.write(content)
                            print(f"Content written to: {file_path}")
                        except Exception as e:
                            print(f"Error writing to {file_path}: {e}")
                    else:
                        print(f"Could not determine file extension for: {file_path}")
    else:
        print("No '###FilePath:' blocks found in the input text.")

    return None

# Example usage with your provided strings:
# example_text = """###FilePath: src/claim.py
# class Claim:
#     def __init__(self, NPI, ProviderNumber, PatientStatus, DRGCode, LengthOfStay, CoveredDays,
#                  CostReportDays, DischargeDate, CoveredCharges, SpecialPayIndicator, ReviewCode,
#                  DiagnosisCodes, ProcedureCodes, LTCHDPPIndicator, PaymentData):
#         self.NPI = NPI

# ###FilePath: src/main/java/com/ltch/model/Claim.java

# package com.ltch.model;

# import java.util.Collection;
# import java.util.Date;

# ###FilePath: non_existent_folder/another_file.txt
# This is some content for a file in a non-existent folder.
# """

# extract_and_save_content(example_text)

# # You can also test with a file in the current directory:
# example_current_dir = """###FilePath: src/current_file.md
# # This is a markdown file created in the current directory.
# """
# extract_and_save_content(example_current_dir)