# import os
# from pathlib import Path
# import re
# import shutil
# import zipfile

# from fastapi.temp_pydantic_v1_params import Body
# import requests
# from tree_sitter import Query
# from config import load_config
# from fastapi import FastAPI, Form, HTTPException, File, UploadFile
# from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
# from pydantic import BaseModel
# from typing import Annotated, Any, Dict, List, Literal, Optional
# from agents.functional_spec_generator_agent import FunctionalSpecGeneratorAgent
# from agents.mermaid_diagram_generator_agent import MermaidDiagramGeneratorAgent
# from agents.functional_spec_consolidator_agent import FunctionalSpecsConsolidatorAgent
# from agents.oo_designer import ObjectOrientedDesignerAgent
# from agents.oops_coder import ObjectOrientedCoderAgent
# from pathlib import Path
# from agents.validation_agent import validate_with_llm
# from agents import ReverseEngineeringAgentManager
# from utils.job_util import get_job_run_id_persistent, load_job_run_state
# from sampleServices import programs_list_logical_unit, sample_mermaid_class_diagram
# import yaml 
# from Services2 import build_cobol_2d_array, compare_md_cobol_2d, extract_cobol_methods_from_used_files, extract_paragraphs_from_cobol, func_spec,consolidated_func_spec
# from fastapi.middleware.cors import CORSMiddleware
# from io import BytesIO
# import logging

# app = FastAPI(
#      title="CodeSpectre",
#     description="Mainframe Application Modernization powered by Generative AI"
# )
# config = load_config()

# # logger for this module
# logger = logging.getLogger("mf_modernization.services")
# if not logging.getLogger().handlers:
#     # Basic config only if logging not configured elsewhere
#     logging.basicConfig(level=logging.INFO)

# origins = ["http://localhost:8000",
#     "http://127.0.0.1:8000",
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]
# #app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     #allow_origins=origins,
#     allow_origins=["*"],
#     allow_credentials=False,
#     #allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Content-Disposition"]  # <-- expose so browser can read it
# )



# UPLOAD_DIR = Path("uploads")
# # Directory where the contents of the zip files will be extracted
# EXTRACTED_CONTENTS_DIR = Path("C:/Extracted_dir")
# # File to persist the path of the last extracted folder
# STATE_FILE_PATH = Path("last_extracted_folder.txt")

# # Ensure directories exist
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# EXTRACTED_CONTENTS_DIR.mkdir(parents=True, exist_ok=True)

# # --- Pydantic Models ---
# # Forward declaration for recursive model
# class FileSystemEntry(BaseModel):
#     name: str
#     type: Literal["file", "directory"]
#     # For directories, this will contain a list of child FileSystemEntry objects
#     children: Optional[List["FileSystemEntry"]] = None

# # Update the forward ref for FileSystemEntry
# FileSystemEntry.update_forward_refs()

# class UploadResponse(BaseModel):
#     message: str
#     extracted_path: Optional[str] = None
#     uploaded_filename: str

# # --- Pydantic Models ---
# # Forward declaration for recursive model
# class FileSystemEntry(BaseModel):
#     name: str
#     type: Literal["file", "directory"]
#     # For directories, this will contain a list of child FileSystemEntry objects
#     children: Optional[List["FileSystemEntry"]] = None

# # Update the forward ref for FileSystemEntry
# FileSystemEntry.update_forward_refs()

# class ContentsResponse(BaseModel):
#     viewing_path: Optional[str]
#     # This will now be a list of the top-level FileSystemEntry objects (the root of the tree)
#     contents_tree: List[FileSystemEntry]
    


# # --- Helper functions for state persistence ---
# def _save_last_extracted_path(path: Path):
#     """Saves the path of the last extracted folder to a file."""
#     try:
#         with open(STATE_FILE_PATH, "w") as f:
#             f.write(str(path))
#     except Exception as e:
#         print(f"Error saving state to {STATE_FILE_PATH}: {e}")

# def _load_last_extracted_path() -> Optional[Path]:
#     """Loads the path of the last extracted folder from a file."""
#     if not STATE_FILE_PATH.is_file():
#         return None
#     try:
#         with open(STATE_FILE_PATH, "r") as f:
#             path_str = f.read().strip()
#             if path_str:
#                 return Path(path_str)
#             return None
#     except Exception as e:
#         print(f"Error loading state from {STATE_FILE_PATH}: {e}")
#         return None

# # --- Recursive Helper Function to Build Directory Tree ---
# def _build_directory_tree(base_path: Path) -> List[FileSystemEntry]:
#     """
#     Recursively builds a list of FileSystemEntry objects representing
#     the directory structure starting from base_path.
#     """
#     tree: List[FileSystemEntry] = []
    
#     if not base_path.is_dir():
#         # If the base_path itself is a file, return it as a single entry
#         if base_path.is_file():
#             return [FileSystemEntry(name=base_path.name, type="file")]
#         return [] # Path does not exist or is not a file/directory

#     try:
#         for item_name in sorted(os.listdir(base_path)): # Sort for consistent output
#             item_path = base_path / item_name
#             if item_path.is_dir():
#                 children = _build_directory_tree(item_path)
#                 tree.append(FileSystemEntry(name=item_name, type="directory", children=children))
#             elif item_path.is_file():
#                 tree.append(FileSystemEntry(name=item_name, type="file"))
#     except Exception as e:
#         print(f"Error building directory tree for {base_path}: {e}")
#         pass

#     return tree



# #### API 1 Upload the Zipped Folder


# @app.post("/upload_folder_contents/", response_model=UploadResponse, summary="Upload a zipped folder")
# async def upload_folder_contents(folder: UploadFile = File(...)):
#     file = folder
#     if not file.filename.lower().endswith(".zip"):
#         raise HTTPException(status_code=400, detail="Only .zip files are allowed for folder uploads.")

#     # Create a unique filename for the uploaded zip
#     uploaded_zip_filename = f"{file.filename}"
#     uploaded_zip_path = UPLOAD_DIR / uploaded_zip_filename

#     # Create a unique directory for extraction based on the original folder name (if possible)
#     extracted_folder_name = f"{Path(file.filename).stem}"
#     extracted_full_path = EXTRACTED_CONTENTS_DIR / extracted_folder_name

#     try:
#         # 1. Save the uploaded zip file
#         with open(uploaded_zip_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # 2. Extract the contents
#         with zipfile.ZipFile(uploaded_zip_path, 'r') as zip_ref:
#             # Create the extraction directory
#             extracted_full_path.mkdir(parents=True, exist_ok=True)
#             zip_ref.extractall(extracted_full_path)
        
#         # 3. Persist the path of the newly extracted folder
#         _save_last_extracted_path(extracted_full_path)

#         return UploadResponse(
#             message=f"Folder '{file.filename}' uploaded successfully.",
#             extracted_path=str(extracted_full_path),
#             uploaded_filename=uploaded_zip_filename
#         )
#     except zipfile.BadZipFile:
#         # Clean up corrupted zip file
#         if uploaded_zip_path.exists():
#             uploaded_zip_path.unlink()
#         raise HTTPException(status_code=400, detail="Uploaded file is not a valid zip archive.")
#     except Exception as e:
#         # Clean up if extraction fails
#         if uploaded_zip_path.exists():
#             uploaded_zip_path.unlink()
#         if extracted_full_path.exists():
#             shutil.rmtree(extracted_full_path)
#         raise HTTPException(status_code=500, detail=f"Failed to process upload: {e}")
#     finally:
#         # Optional: Clean up the uploaded zip file after extraction
#         if uploaded_zip_path.exists():
#             uploaded_zip_path.unlink()



    
# @app.get("/list_extracted_folder/", response_model=ContentsResponse, summary="List contents of the last uploaded and extracted folder as a tree structure")
# async def list_extracted_folder():

#     # Load the path from the state file
#     _current_extracted_folder = _load_last_extracted_path()

#     if _current_extracted_folder is None:
#         raise HTTPException(status_code=400, detail="No folder has been uploaded and extracted yet. Please use /upload_folder_contents first.")

#     # Re-validate the path just in case it was deleted or changed type after being set
#     if not _current_extracted_folder.exists():
#         # If it no longer exists, clear the state file
#         if STATE_FILE_PATH.is_file():
#             STATE_FILE_PATH.unlink()
#         raise HTTPException(status_code=404, detail=f"The previously extracted folder no longer exists: {_current_extracted_folder}")
#     if not _current_extracted_folder.is_dir():
#         # If it's no longer a directory, clear the state file
#         if STATE_FILE_PATH.is_file():
#             STATE_FILE_PATH.unlink()
#         raise HTTPException(status_code=400, detail=f"The previously extracted path is not a directory: {_current_extracted_folder}")


#     top_level_contents = list(_current_extracted_folder.iterdir())
#     if len(top_level_contents) == 1 and top_level_contents[0].is_dir():
#         # If there's only one item and it's a directory, assume that's the actual root of the content
#         root_to_list = top_level_contents[0]
#     else:
#         # Otherwise, the extracted_full_path itself is the root of the content
#         root_to_list = _current_extracted_folder

#     contents_tree = _build_directory_tree(root_to_list)

#     return ContentsResponse(viewing_path=str(_current_extracted_folder), contents_tree=contents_tree)

 
# ### API 3 to view logical units file
 
# @app.post("/logical-units/")
# async def get_logical_unit(app_name: Annotated[str,Form()] = "LTCHPPSPricerMFApp2021",
#                            config_file : UploadFile = File(...)) -> Dict[str,Any]:
    
#     global current_logical_unit_content
#     if not config_file.filename.endswith((".yml",".yaml")):
#         raise HTTPException(status_code=400, detail = "Only yaml files are allowed..")

#     try:
#         contents = await config_file.read()
#         file_content_str = contents.decode('utf-8')
#         parsed_yaml = yaml.safe_load(file_content_str)  
        
#         current_logical_unit_content = parsed_yaml
        
#         if isinstance(parsed_yaml, list):
#             programs_list= programs_list_logical_unit(parsed_yaml)
#             return {
#                 "Application_name": app_name,
#                 "filename" : config_file.filename,
#                 "file_content": parsed_yaml,
#                 "programs_list" : programs_list if programs_list else []
#                 }
#         return {
#             "Application_name": app_name,
#             "filename" : config_file.filename,
#             "file_content": parsed_yaml
#             }
    
    
#     except yaml.YAMLError as e:
#         raise HTTPException(status_code=422, detail=f" Error parsing YAML file: {e}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error occured..{e}")


# @app.post("/source-file/")
# async def view_source_code(fileName :str = Form(...)):
#     fileName = fileName.split('-',1)[1] if '-' in fileName else fileName
#     fileName = fileName.replace(" ","")
#     BASE_DIR_DEFAULT=config['source_path']['base_dir_default'] + "\\" +"source_code" +  "\\" + fileName
#     path1 = BASE_DIR_DEFAULT.replace("/","\\")
#     path = path1
  

#     try:
#         with open(path,'r') as file:
#             contents=file.readlines()
#         return {
#             "filename" : fileName,
#             "contents" : contents
#         }
    
#     except Exception as e:
#         return JSONResponse(
#             status_code=404,
#             content={"status":"error","message": str(e)})
    


# # @app.post("/functspec-from-md-files/") # Changed endpoint name for clarity
# # async def funcspecs_from_md_files(specification: str = Form(...)): 

# #     path1 = "C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs"
# #     # def save_markdown_to_disk(content, filename_path):
# #     # with open(specification, 'w', encoding='utf-8') as f:
# #     #     f.write(content)
# #     filename = specification.replace(".md",".pdf")
# #     PDF_DIRECTORY = Path(path1)
# #     if not PDF_DIRECTORY.is_dir():
# #         raise HTTPException(
# #             status_code=500, detail="PDF storage directory not found on server."
# #         )
# #     file_path = PDF_DIRECTORY/filename

# #      # 🔹 Check if the file exists and is a file
# #     if not file_path.is_file():
# #         raise HTTPException(status_code=404, detail="File not found.")
    
# #      # 🔹 Return the file as a FileResponse
# #     return FileResponse(
# #         path=file_path,
# #         media_type="application/pdf",
# #         filename=filename,
# #         headers={"Content-Disposition": f"attachment; filename={filename}"},
# #     )

# @app.post("/functspec-from-md-files/")
# async def funcspecs_from_md_files(
#     specification: str = Form(...),
#     filetype: str = Form("md")    # can be "pdf" or "md"
# ):
#     OUTPUT_DIRECTORY = Path("C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs")
#     if not OUTPUT_DIRECTORY.is_dir():
#         raise HTTPException(
#             status_code=500, detail="Output directory not found on server."
#         )
#     # Normalize filename
#     filename_base = specification.replace(".pdf", "").replace(".md", "")
#     filename = filename_base + (".pdf" if filetype.lower() == "pdf" else ".md")
#     file_path = OUTPUT_DIRECTORY / filename


#     if not file_path.is_file():
#         raise HTTPException(status_code=404, detail=f"File [{filename}] not found.")

#     if filetype.lower() == "pdf":
#         return FileResponse(
#             path=file_path,
#             media_type="application/pdf",
#             filename=filename,
#             headers={"Content-Disposition": f"attachment; filename={filename}"},
#         )
#     else:
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()
#         print(f"Serving markdown from: {file_path}")
#         return Response(
#             content=content,
#             media_type="text/markdown"
#             # For download as file, add headers (optional):
#             # headers={"Content-Disposition": f"attachment; filename={filename}"}
#         )

# @app.post("/logical_units_lists/")
# async def logical_units_lists(file: UploadFile = File(...)):
      
#     if not file.filename.endswith(('.yaml', '.yml')):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid file type. Please upload a YAML file (.yaml or .yml)."
#         )

#     try:
#         contents = await file.read()
#         yaml_content = contents.decode("utf-8")
#         data = yaml.safe_load(yaml_content)
#         if not isinstance(data, list):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid YAML format: Expected a list of objects at the root level."
#             )
#         completed_ids = []

#         # Loop through each item (which should be a dictionary) in the parsed list.
#         for item in data:
#             if isinstance(item, dict):
#                 if "id" in item:
#                     completed_ids.append(str(item["id"])+"_FunctionalSpecification.md") # Add the 'id' to our list

#         return {"completed_ids": completed_ids}

#     except yaml.YAMLError as e:
#         raise HTTPException(status_code=400, detail=f"Invalid YAML content: {e}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# ### API 5 Generate the functional specifications of given logical unit.. 
 
# @app.post("/generate-func-spec/")
# async def generate_functional_spec(app_name: Annotated[str,Form()] = "LTCHPPSPricerMFApp2021",config_file : UploadFile = File(...) ):   
#     application_name = app_name
#     if not config_file.filename.endswith((".yml",".yaml")):
#         raise HTTPException(status_code=400, detail = "Only yaml files are allowed..")
#     try:
#         contents = await config_file.read()
#         file_content_str = contents.decode('utf-8')
#         parsed_yaml = yaml.safe_load(file_content_str)  
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error occured..{e}") 
    
#     if parsed_yaml is None:
#         raise HTTPException(status_code=400, detail="Cannot find logical unit configurations")
#     results = func_spec(application_name,parsed_yaml)

#     pdf_path = Path(results)  

#     if not pdf_path.exists():
#         raise HTTPException(status_code=500, detail="PDF generation failed.")

#     return FileResponse(
#         path=pdf_path,
#         media_type="application/pdf",
#         filename=pdf_path.name
#     )  
#     # return {
#     #     "Application_name" : application_name,
#     #     "file_name" : config_file.filename,
#     #     "specs_generated" : results
#     # }

# @app.get("/get_cobol_paragraph/")
# async def get_cobol_paragraph(file_name: str, paragraph_name: str):
#     # Path resolution depends on your storage logic
#     #file_path=config['source_path']['base_dir_default'] + "\\" +"source_code" +  "\\" + file_name
#     file_name = file_name.replace("Analysis of ", "", 1).strip()
#     file_name = file_name.replace("Analysis of COBOL program: ", "", 1).strip()
#     file_name = file_name.replace("Program: ", "", 1).strip()
#     file_path = Path("C:\\Users\\YendetiLalith\\Documents\\CodeSpectre\\MainframeApplications\\LTCHPPSPricerMFApp2021\\source_code") / file_name  # e.g., cobol_files/LTCAL032.cbl
#     print(f"Looking for paragraph '{paragraph_name}' in file: {file_path}")
#     if not file_path.exists():
#         raise HTTPException(status_code=404, detail="File not found")
#     code = file_path.read_text()
#     paragraphs = extract_paragraphs_from_cobol(code)
#     if paragraph_name not in paragraphs:
#         raise HTTPException(status_code=404, detail="Paragraph not found")
#     return {"snippet": paragraphs[paragraph_name]}

# # def extract_paragraphs_from_cobol(source_code):
# #     pattern = re.compile(r'(?m)^\s*\d*\s*([A-Z0-9\-]+)\.\s*\n(.*?)(?=^\s*\d*\s*[A-Z0-9\-]+\.\s*|\Z)', re.DOTALL | re.MULTILINE)
# #     return {m.group(1).strip(): m.group(2).strip() for m in pattern.finditer(source_code)}

# def batch_extract_programs(src_dir):
#     all_para_dict = {}
#     for fname in os.listdir(src_dir):
#         full_path = os.path.join(src_dir, fname)
#         if os.path.isfile(full_path):
#             with open(full_path, 'r', errors='ignore') as f:
#                 code = f.read()
#                 paras = extract_paragraphs_from_cobol(code)
#                 program_name = fname.split('.')[0].upper()
#                 all_para_dict[program_name] = list(paras.keys())
#     return all_para_dict

# # FastAPI Endpoint - returns { program: [paragraph, ...] } for all files
# @app.get("/list_cobol_paragraphs/")
# def list_cobol_paragraphs():
#     src_dir = r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\source_code"
#     cobol_para_dict = batch_extract_programs(src_dir)
#     return cobol_para_dict

# @app.post("/extract_paragraphs_for_used_files/")
# def extract_paragraphs_for_used_files(
#     used_programs: List[str] = Body(..., embed=True)
# ):
#     src_dir = r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\source_code" # <-- update to match your project source folder
#     cobol_dict = extract_cobol_methods_from_used_files(src_dir, used_programs)
#     return cobol_dict

# @app.post("/paragraph_comparison/")
# def paragraph_comparison(
#     md_data: List[List[str]] = Body(..., embed=True)
# ):
#     try:
#         src_dir = r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\source_code" # <-- update to match your project source folder

#         # Validate incoming md_data shape. Expect list of lists where first element is filename
#         if not isinstance(md_data, list):
#             raise ValueError("md_data must be a list of lists, e.g. [[filename, ...], ...]")

#         filenames = sorted({
#             item[0] for item in md_data
#             if isinstance(item, (list, tuple)) and len(item) > 0 and isinstance(item[0], str)
#         })

#         if not filenames:
#             raise ValueError("No filenames could be extracted from md_data. Ensure payload is [[filename, ...], ...]")

#         cobol_data = build_cobol_2d_array(src_dir, filenames)
#         result = compare_md_cobol_2d(md_data, cobol_data)
#         return result
#     except Exception as e:
#         # Log full traceback for debugging and return a clear error message
#         logger.exception("Error in paragraph_comparison endpoint")
#         # Return HTTPException so FastAPI sends a JSON error with status 500 and detail
#         raise HTTPException(status_code=500, detail=str(e))
    
# # Add this to your backend main file

# from pydantic import BaseModel
# from typing import Optional

# class ValidationRequest(BaseModel):
#     record_id: str
#     source_code: str  # Combined source code
#     functional_spec: str  # Generated markdown

# class ValidationMarkdownResponse(BaseModel):
#     record_id: str
#     validation_markdown: str
#     file_path: Optional[str] = None

# @app.post("/validate-functional-spec/", response_model=ValidationMarkdownResponse)
# async def validate_functional_spec(request: ValidationRequest):
#     """
#     Validate the functional spec against source code and return markdown and file path.
#     """
#     try:
#         manager = ReverseEngineeringAgentManager()
#         job_id = get_job_run_id_persistent()
#         base_dir = str(Path(config['source_path']['base_dir_default']))
#         validation_agent = manager.get_agent("validation_agent")
#         result = validation_agent.execute(
#             job_id=job_id,
#             record_id=request.record_id,
#             base_dir=base_dir,
#             source_code=request.source_code,
#             functional_spec=request.functional_spec,
#         )
#         validation_path = str(Path(base_dir) / "output" / f"{job_id}_{request.record_id}_validation.md")
#         return ValidationMarkdownResponse(
#             record_id=request.record_id,
#             validation_markdown=result.content if hasattr(result, "content") else str(result),
#             file_path=validation_path if Path(validation_path).exists() else None,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Validation failed: {str(e)}"
#         )

# @app.post("/validate-from-files/")
# async def validate_from_files(
#     record_id: str = Form(...),
#     config_file: UploadFile = File(...)
# ):
#     """
#     Validate by loading source code and functional spec from disk and return markdown and file path.
#     """
#     try:
#         md_path = Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications" / f"{record_id}_FunctionalSpecification.md"
#         if not md_path.exists():
#             raise HTTPException(status_code=404, detail=f"Functional spec not found: {md_path}")
#         with open(md_path, "r", encoding="utf-8") as f:
#             functional_spec = f.read()

#         contents = await config_file.read()
#         file_content_str = contents.decode('utf-8')
#         parsed_yaml = yaml.safe_load(file_content_str)

#         matching_item = None
#         for item in parsed_yaml:
#             if item.get('id') == record_id:
#                 matching_item = item
#                 break
#         if not matching_item:
#             raise HTTPException(status_code=404, detail=f"Record {record_id} not found in config")

#         programs_list = matching_item.get('programs', [])
#         combined_code = ""
#         for program in programs_list:
#             program = program.strip()
#             if program.lower().endswith(('.csv', '.txt', '.dat')):
#                 continue
#             source_code_path = Path(config['source_path']['base_dir_default']) / "source_code" / program
#             if source_code_path.exists():
#                 with open(source_code_path, "r", encoding="utf-8", errors='ignore') as f:
#                     code = f.read()
#                     combined_code += f"## Content of {program}\n```\n{code}\n```\n\n"
#         if not combined_code:
#             raise HTTPException(status_code=400, detail="No source code found")

#         manager = ReverseEngineeringAgentManager()
#         job_id = get_job_run_id_persistent()
#         base_dir = str(Path(config['source_path']['base_dir_default']))
#         validation_agent = manager.get_agent("validation_agent")
#         logger.info(f"Calling ValidationAgent for record_id={record_id}")
#         result = validation_agent.execute(
#             job_id=job_id,
#             record_id=record_id,
#             base_dir=base_dir,
#             source_code=combined_code,
#             functional_spec=functional_spec,
#         )
#         validation_path = str(Path(base_dir) / "output" / f"{job_id}_{record_id}_validation.md")
#         return ValidationMarkdownResponse(
#             record_id=record_id,
#             validation_markdown=result.content if hasattr(result, "content") else str(result),
#             file_path=validation_path if Path(validation_path).exists() else None,
#         )
#     except HTTPException:
#         raise HTTPException(status_code=404, detail="Record not found or file missing.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


import os
from pathlib import Path
import re
import shutil
import zipfile

from fastapi.temp_pydantic_v1_params import Body
import requests
from tree_sitter import Query
from config import load_config
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from pydantic import BaseModel
from typing import Annotated, Any, Dict, List, Literal, Optional
from agents.functional_spec_generator_agent import FunctionalSpecGeneratorAgent
from agents.mermaid_diagram_generator_agent import MermaidDiagramGeneratorAgent
from agents.functional_spec_consolidator_agent import FunctionalSpecsConsolidatorAgent
from agents.oo_designer import ObjectOrientedDesignerAgent
from agents.oops_coder import ObjectOrientedCoderAgent
from pathlib import Path
from agents.validation_agent import validate_with_llm
from agents import ReverseEngineeringAgentManager
from utils.job_util import get_job_run_id_persistent, load_job_run_state
from sampleServices import programs_list_logical_unit, sample_mermaid_class_diagram
import yaml 
from Services2 import build_cobol_2d_array, compare_md_cobol_2d, extract_cobol_methods_from_used_files, extract_paragraphs_from_cobol, func_spec,consolidated_func_spec
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import logging

app = FastAPI(
     title="CodeSpectre",
    description="Mainframe Application Modernization powered by Generative AI"
)
config = load_config()

# logger for this module
logger = logging.getLogger("mf_modernization.services")
if not logging.getLogger().handlers:
    # Basic config only if logging not configured elsewhere
    logging.basicConfig(level=logging.INFO)

origins = ["http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # ← Add your React dev server
    "http://127.0.0.1:5173",
]
#app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=False,
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]  # <-- expose so browser can read it
)



UPLOAD_DIR = Path("uploads")
# Directory where the contents of the zip files will be extracted
EXTRACTED_CONTENTS_DIR = Path("C:/Extracted_dir")
# File to persist the path of the last extracted folder
STATE_FILE_PATH = Path("last_extracted_folder.txt")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTED_CONTENTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Pydantic Models ---
# Forward declaration for recursive model
class FileSystemEntry(BaseModel):
    name: str
    type: Literal["file", "directory"]
    # For directories, this will contain a list of child FileSystemEntry objects
    children: Optional[List["FileSystemEntry"]] = None

# Update the forward ref for FileSystemEntry
FileSystemEntry.update_forward_refs()

class UploadResponse(BaseModel):
    message: str
    extracted_path: Optional[str] = None
    uploaded_filename: str

# --- Pydantic Models ---
# Forward declaration for recursive model
class FileSystemEntry(BaseModel):
    name: str
    type: Literal["file", "directory"]
    # For directories, this will contain a list of child FileSystemEntry objects
    children: Optional[List["FileSystemEntry"]] = None

# Update the forward ref for FileSystemEntry
FileSystemEntry.update_forward_refs()

class ContentsResponse(BaseModel):
    viewing_path: Optional[str]
    # This will now be a list of the top-level FileSystemEntry objects (the root of the tree)
    contents_tree: List[FileSystemEntry]
    


# --- Helper functions for state persistence ---
def _save_last_extracted_path(path: Path):
    """Saves the path of the last extracted folder to a file."""
    try:
        with open(STATE_FILE_PATH, "w") as f:
            f.write(str(path))
    except Exception as e:
        print(f"Error saving state to {STATE_FILE_PATH}: {e}")

def _load_last_extracted_path() -> Optional[Path]:
    """Loads the path of the last extracted folder from a file."""
    if not STATE_FILE_PATH.is_file():
        return None
    try:
        with open(STATE_FILE_PATH, "r") as f:
            path_str = f.read().strip()
            if path_str:
                return Path(path_str)
            return None
    except Exception as e:
        print(f"Error loading state from {STATE_FILE_PATH}: {e}")
        return None

# --- Recursive Helper Function to Build Directory Tree ---
def _build_directory_tree(base_path: Path) -> List[FileSystemEntry]:
    """
    Recursively builds a list of FileSystemEntry objects representing
    the directory structure starting from base_path.
    """
    tree: List[FileSystemEntry] = []
    
    if not base_path.is_dir():
        # If the base_path itself is a file, return it as a single entry
        if base_path.is_file():
            return [FileSystemEntry(name=base_path.name, type="file")]
        return [] # Path does not exist or is not a file/directory

    try:
        for item_name in sorted(os.listdir(base_path)): # Sort for consistent output
            item_path = base_path / item_name
            if item_path.is_dir():
                children = _build_directory_tree(item_path)
                tree.append(FileSystemEntry(name=item_name, type="directory", children=children))
            elif item_path.is_file():
                tree.append(FileSystemEntry(name=item_name, type="file"))
    except Exception as e:
        print(f"Error building directory tree for {base_path}: {e}")
        pass

    return tree



#### API 1 Upload the Zipped Folder


@app.post("/upload_folder_contents/", response_model=UploadResponse, summary="Upload a zipped folder")
async def upload_folder_contents(folder: UploadFile = File(...)):
    file = folder
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed for folder uploads.")

    # Create a unique filename for the uploaded zip
    uploaded_zip_filename = f"{file.filename}"
    uploaded_zip_path = UPLOAD_DIR / uploaded_zip_filename

    # Create a unique directory for extraction based on the original folder name (if possible)
    extracted_folder_name = f"{Path(file.filename).stem}"
    extracted_full_path = EXTRACTED_CONTENTS_DIR / extracted_folder_name

    try:
        # 1. Save the uploaded zip file
        with open(uploaded_zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Extract the contents
        with zipfile.ZipFile(uploaded_zip_path, 'r') as zip_ref:
            # Create the extraction directory
            extracted_full_path.mkdir(parents=True, exist_ok=True)
            zip_ref.extractall(extracted_full_path)
        
        # 3. Persist the path of the newly extracted folder
        _save_last_extracted_path(extracted_full_path)

        return UploadResponse(
            message=f"Folder '{file.filename}' uploaded successfully.",
            extracted_path=str(extracted_full_path),
            uploaded_filename=uploaded_zip_filename
        )
    except zipfile.BadZipFile:
        # Clean up corrupted zip file
        if uploaded_zip_path.exists():
            uploaded_zip_path.unlink()
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid zip archive.")
    except Exception as e:
        # Clean up if extraction fails
        if uploaded_zip_path.exists():
            uploaded_zip_path.unlink()
        if extracted_full_path.exists():
            shutil.rmtree(extracted_full_path)
        raise HTTPException(status_code=500, detail=f"Failed to process upload: {e}")
    finally:
        # Optional: Clean up the uploaded zip file after extraction
        if uploaded_zip_path.exists():
            uploaded_zip_path.unlink()



    
@app.get("/list_extracted_folder/", response_model=ContentsResponse, summary="List contents of the last uploaded and extracted folder as a tree structure")
async def list_extracted_folder():

    # Load the path from the state file
    _current_extracted_folder = _load_last_extracted_path()

    if _current_extracted_folder is None:
        raise HTTPException(status_code=400, detail="No folder has been uploaded and extracted yet. Please use /upload_folder_contents first.")

    # Re-validate the path just in case it was deleted or changed type after being set
    if not _current_extracted_folder.exists():
        # If it no longer exists, clear the state file
        if STATE_FILE_PATH.is_file():
            STATE_FILE_PATH.unlink()
        raise HTTPException(status_code=404, detail=f"The previously extracted folder no longer exists: {_current_extracted_folder}")
    if not _current_extracted_folder.is_dir():
        # If it's no longer a directory, clear the state file
        if STATE_FILE_PATH.is_file():
            STATE_FILE_PATH.unlink()
        raise HTTPException(status_code=400, detail=f"The previously extracted path is not a directory: {_current_extracted_folder}")


    top_level_contents = list(_current_extracted_folder.iterdir())
    if len(top_level_contents) == 1 and top_level_contents[0].is_dir():
        # If there's only one item and it's a directory, assume that's the actual root of the content
        root_to_list = top_level_contents[0]
    else:
        # Otherwise, the extracted_full_path itself is the root of the content
        root_to_list = _current_extracted_folder

    contents_tree = _build_directory_tree(root_to_list)

    return ContentsResponse(viewing_path=str(_current_extracted_folder), contents_tree=contents_tree)

 
### API 3 to view logical units file
 
@app.post("/logical-units/")
async def get_logical_unit(app_name: Annotated[str,Form()] = "LTCHPPSPricerMFApp2021",
                           config_file : UploadFile = File(...)) -> Dict[str,Any]:
    
    global current_logical_unit_content
    if not config_file.filename.endswith((".yml",".yaml")):
        raise HTTPException(status_code=400, detail = "Only yaml files are allowed..")

    try:
        contents = await config_file.read()
        file_content_str = contents.decode('utf-8')
        parsed_yaml = yaml.safe_load(file_content_str)  
        
        current_logical_unit_content = parsed_yaml
        
        if isinstance(parsed_yaml, list):
            programs_list= programs_list_logical_unit(parsed_yaml)
            return {
                "Application_name": app_name,
                "filename" : config_file.filename,
                "file_content": parsed_yaml,
                "programs_list" : programs_list if programs_list else []
                }
        return {
            "Application_name": app_name,
            "filename" : config_file.filename,
            "file_content": parsed_yaml
            }
    
    
    except yaml.YAMLError as e:
        raise HTTPException(status_code=422, detail=f" Error parsing YAML file: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occured..{e}")


@app.post("/source-file/")
async def view_source_code(fileName :str = Form(...)):
    fileName = fileName.split('-',1)[1] if '-' in fileName else fileName
    fileName = fileName.replace(" ","")
    BASE_DIR_DEFAULT=config['source_path']['base_dir_default'] + "\\" +"source_code" +  "\\" + fileName
    path1 = BASE_DIR_DEFAULT.replace("/","\\")
    path = path1
  

    try:
        with open(path,'r') as file:
            contents=file.readlines()
        return {
            "filename" : fileName,
            "contents" : contents
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=404,
            content={"status":"error","message": str(e)})
    


# @app.post("/functspec-from-md-files/") # Changed endpoint name for clarity
# async def funcspecs_from_md_files(specification: str = Form(...)): 

#     path1 = "C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs"
#     # def save_markdown_to_disk(content, filename_path):
#     # with open(specification, 'w', encoding='utf-8') as f:
#     #     f.write(content)
#     filename = specification.replace(".md",".pdf")
#     PDF_DIRECTORY = Path(path1)
#     if not PDF_DIRECTORY.is_dir():
#         raise HTTPException(
#             status_code=500, detail="PDF storage directory not found on server."
#         )
#     file_path = PDF_DIRECTORY/filename

#      # 🔹 Check if the file exists and is a file
#     if not file_path.is_file():
#         raise HTTPException(status_code=404, detail="File not found.")
    
#      # 🔹 Return the file as a FileResponse
#     return FileResponse(
#         path=file_path,
#         media_type="application/pdf",
#         filename=filename,
#         headers={"Content-Disposition": f"attachment; filename={filename}"},
#     )

@app.post("/functspec-from-md-files/")
async def funcspecs_from_md_files(
    specification: str = Form(...),
    filetype: str = Form("md")    # can be "pdf" or "md"
):
    OUTPUT_DIRECTORY = Path("C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs")
    if not OUTPUT_DIRECTORY.is_dir():
        raise HTTPException(
            status_code=500, detail="Output directory not found on server."
        )
    # Normalize filename
    filename_base = specification.replace(".pdf", "").replace(".md", "")
    filename = filename_base + (".pdf" if filetype.lower() == "pdf" else ".md")
    file_path = OUTPUT_DIRECTORY / filename


    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File [{filename}] not found.")

    if filetype.lower() == "pdf":
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Serving markdown from: {file_path}")
        return Response(
            content=content,
            media_type="text/markdown"
            # For download as file, add headers (optional):
            # headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

@app.post("/logical_units_lists/")
async def logical_units_lists(file: UploadFile = File(...)):
      
    if not file.filename.endswith(('.yaml', '.yml')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a YAML file (.yaml or .yml)."
        )

    try:
        contents = await file.read()
        yaml_content = contents.decode("utf-8")
        data = yaml.safe_load(yaml_content)
        if not isinstance(data, list):
            raise HTTPException(
                status_code=400,
                detail="Invalid YAML format: Expected a list of objects at the root level."
            )
        completed_ids = []

        # Loop through each item (which should be a dictionary) in the parsed list.
        for item in data:
            if isinstance(item, dict):
                if "id" in item:
                    completed_ids.append(str(item["id"])+"_FunctionalSpecification.md") # Add the 'id' to our list

        return {"completed_ids": completed_ids}

    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML content: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

### API 5 Generate the functional specifications of given logical unit.. 
 
@app.post("/generate-func-spec/")
async def generate_functional_spec(app_name: Annotated[str,Form()] = "LTCHPPSPricerMFApp2021",config_file : UploadFile = File(...) ):   
    application_name = app_name
    if not config_file.filename.endswith((".yml",".yaml")):
        raise HTTPException(status_code=400, detail = "Only yaml files are allowed..")
    try:
        contents = await config_file.read()
        file_content_str = contents.decode('utf-8')
        parsed_yaml = yaml.safe_load(file_content_str)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occured..{e}") 
    
    if parsed_yaml is None:
        raise HTTPException(status_code=400, detail="Cannot find logical unit configurations")
    results = func_spec(application_name,parsed_yaml)

    pdf_path = Path(results)  
    logger.info(f"Generated PDF path: {pdf_path}")
    print(f"Generated PDF path: {pdf_path}")

    if not pdf_path.exists():
        raise HTTPException(status_code=500, detail="PDF generation failed.")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name
    )  
    # return {
    #     "Application_name" : application_name,
    #     "file_name" : config_file.filename,
    #     "specs_generated" : results
    # }

@app.get("/get_cobol_paragraph/")
async def get_cobol_paragraph(file_name: str, paragraph_name: str):
    # Path resolution depends on your storage logic
    #file_path=config['source_path']['base_dir_default'] + "\\" +"source_code" +  "\\" + file_name
    file_name = file_name.replace("Analysis of ", "", 1).strip()
    file_name = file_name.replace("Analysis of COBOL program: ", "", 1).strip()
    file_name = file_name.replace("Program: ", "", 1).strip()
    file_path = Path("C:\\Users\\YendetiLalith\\Documents\\CodeSpectre\\MainframeApplications\\LTCHPPSPricerMFApp2021\\source_code") / file_name  # e.g., cobol_files/LTCAL032.cbl
    print(f"Looking for paragraph '{paragraph_name}' in file: {file_path}")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    code = file_path.read_text()
    paragraphs = extract_paragraphs_from_cobol(code)
    if paragraph_name not in paragraphs:
        raise HTTPException(status_code=404, detail="Paragraph not found")
    return {"snippet": paragraphs[paragraph_name]}

# def extract_paragraphs_from_cobol(source_code):
#     pattern = re.compile(r'(?m)^\s*\d*\s*([A-Z0-9\-]+)\.\s*\n(.*?)(?=^\s*\d*\s*[A-Z0-9\-]+\.\s*|\Z)', re.DOTALL | re.MULTILINE)
#     return {m.group(1).strip(): m.group(2).strip() for m in pattern.finditer(source_code)}

def batch_extract_programs(src_dir):
    all_para_dict = {}
    for fname in os.listdir(src_dir):
        full_path = os.path.join(src_dir, fname)
        if os.path.isfile(full_path):
            with open(full_path, 'r', errors='ignore') as f:
                code = f.read()
                paras = extract_paragraphs_from_cobol(code)
                program_name = fname.split('.')[0].upper()
                all_para_dict[program_name] = list(paras.keys())
    return all_para_dict

# FastAPI Endpoint - returns { program: [paragraph, ...] } for all files
@app.get("/list_cobol_paragraphs/")
def list_cobol_paragraphs():
    src_dir = r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\source_code"
    cobol_para_dict = batch_extract_programs(src_dir)
    return cobol_para_dict

@app.post("/extract_paragraphs_for_used_files/")
def extract_paragraphs_for_used_files(
    used_programs: List[str] = Body(..., embed=True)
):
    src_dir = r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\source_code" # <-- update to match your project source folder
    cobol_dict = extract_cobol_methods_from_used_files(src_dir, used_programs)
    return cobol_dict

@app.post("/paragraph_comparison/")
def paragraph_comparison(
    md_data: List[List[str]] = Body(..., embed=True)
):
    try:
        src_dir = r"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\source_code" # <-- update to match your project source folder

        # Validate incoming md_data shape. Expect list of lists where first element is filename
        if not isinstance(md_data, list):
            raise ValueError("md_data must be a list of lists, e.g. [[filename, ...], ...]")

        filenames = sorted({
            item[0] for item in md_data
            if isinstance(item, (list, tuple)) and len(item) > 0 and isinstance(item[0], str)
        })

        if not filenames:
            raise ValueError("No filenames could be extracted from md_data. Ensure payload is [[filename, ...], ...]")

        cobol_data = build_cobol_2d_array(src_dir, filenames)
        result = compare_md_cobol_2d(md_data, cobol_data)
        return result
    except Exception as e:
        # Log full traceback for debugging and return a clear error message
        logger.exception("Error in paragraph_comparison endpoint")
        # Return HTTPException so FastAPI sends a JSON error with status 500 and detail
        raise HTTPException(status_code=500, detail=str(e))
    
# Add this to your backend main file

# from pydantic import BaseModel
# from typing import Optional

# class ValidationRequest(BaseModel):
#     record_id: str
#     source_code: str  # Combined source code
#     functional_spec: str  # Generated markdown

# class ValidationMarkdownResponse(BaseModel):
#     record_id: str
#     validation_markdown: str
#     file_path: Optional[str] = None

# @app.post("/validate-functional-spec/", response_model=ValidationMarkdownResponse)
# async def validate_functional_spec(request: ValidationRequest):
#     """
#     Validate the functional spec against source code and return markdown and file path.
#     """
#     try:
#         manager = ReverseEngineeringAgentManager()
#         job_id = get_job_run_id_persistent()
#         base_dir = str(Path(config['source_path']['base_dir_default']))
#         validation_agent = manager.get_agent("validation_agent")
#         result = validation_agent.execute(
#             job_id=job_id,
#             record_id=request.record_id,
#             base_dir=base_dir,
#             source_code=request.source_code,
#             functional_spec=request.functional_spec,
#         )
#         #validation_path = str(Path(base_dir) / "output" / f"{job_id}_{request.record_id}_validation.md")
#         validation_path = str(Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications" / f"{job_id}_validation.md")
#         return ValidationMarkdownResponse(
#             record_id=request.record_id,
#             validation_markdown=result.content if hasattr(result, "content") else str(result),
#             file_path=validation_path if Path(validation_path).exists() else None,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Validation failed: {str(e)}"
#         )

# @app.post("/validate-from-files/")
# async def validate_from_files(
#     record_id: str = Form(...),
#     config_file: UploadFile = File(...)
# ):
#     """
#     Validate by loading source code and functional spec from disk and return markdown and file path.
#     """
#     try:
#         # md_path = Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications" / f"{record_id}_FunctionalSpecification.md"
#         md_path = Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications" / f"{record_id}_FunctionalSpecification.md"
#         if not md_path.exists():
#             raise HTTPException(status_code=404, detail=f"Functional spec not found: {md_path}")
#         with open(md_path, "r", encoding="utf-8") as f:
#             functional_spec = f.read()

#         contents = await config_file.read()
#         file_content_str = contents.decode('utf-8')
#         parsed_yaml = yaml.safe_load(file_content_str)

#         matching_item = None
#         for item in parsed_yaml:
#             if item.get('id') == record_id:
#                 matching_item = item
#                 break
#         if not matching_item:
#             raise HTTPException(status_code=404, detail=f"Record {record_id} not found in config")

#         programs_list = matching_item.get('programs', [])
#         combined_code = ""
#         for program in programs_list:
#             program = program.strip()
#             if program.lower().endswith(('.csv', '.txt', '.dat')):
#                 continue
#             source_code_path = Path(config['source_path']['base_dir_default']) / "source_code" / program
#             if source_code_path.exists():
#                 with open(source_code_path, "r", encoding="utf-8", errors='ignore') as f:
#                     code = f.read()
#                     combined_code += f"## Content of {program}\n```\n{code}\n```\n\n"
#         if not combined_code:
#             raise HTTPException(status_code=400, detail="No source code found")

#         manager = ReverseEngineeringAgentManager()
#         job_id = get_job_run_id_persistent()
#         base_dir = str(Path(config['source_path']['base_dir_default']))
#         validation_agent = manager.get_agent("validation_agent")
#         logger.info(f"Calling ValidationAgent for record_id={record_id}")
#         result = validation_agent.execute(
#             job_id=job_id,
#             record_id=record_id,
#             base_dir=base_dir,
#             source_code=combined_code,
#             functional_spec=functional_spec,
#         )
#         validation_path = str(Path(base_dir) / "output" / f"{job_id}_{record_id}_validation.md")
#         return ValidationMarkdownResponse(
#             record_id=record_id,
#             validation_markdown=result.content if hasattr(result, "content") else str(result),
#             file_path=validation_path if Path(validation_path).exists() else None,
#         )
#     except HTTPException:
#         raise HTTPException(status_code=404, detail="Record not found or file missing.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

# New: Read-only endpoint to return existing validation report without re-running validation
class ValidationReportResponse(BaseModel):
    record_id: str
    validation_markdown: str
    file_path: str

@app.get("/validation-report/", response_model=ValidationReportResponse)
async def get_validation_report(record_id: str, job_id: Optional[str] = None):
    """
    Return the saved validation markdown for a given `record_id`.
    If `job_id` is not provided, uses the persistent job run id.
    Falls back to the latest matching report if the exact file is not found.
    """
    try:
        base_dir = Path(config['source_path']['base_dir_default'])
        if job_id is None:
            job_id = get_job_run_id_persistent()
        output_dir = base_dir / "output" / "sas_specifications"
        # candidate = output_dir / f"{job_id}_{record_id}_validation.md"
        candidate = output_dir / f"{record_id}_validation.md"
        # validation_path = str(Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications" / f"{job_id}_validation.md")

        if not candidate.exists():
            matches = sorted(output_dir.glob(f"*_{record_id}_validation.md"), key=lambda p: p.stat().st_mtime)
            if not matches:
                raise HTTPException(status_code=404, detail=f"Validation report not found for record_id={record_id}")
            candidate = matches[-1]
        content = candidate.read_text(encoding="utf-8")
        
        return {
            "record_id": record_id,
            "validation_markdown": content,
            "file_path": str(candidate)
        }
        
        # return ValidationReportResponse(
        #     record_id=record_id,
        #     validation_markdown=content,
        #     file_path=str(candidate),
        # )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load validation report: {str(e)}")


#### API 6 consolidated functional spec generation.....

@app.get("/get-func-spec-md/")
async def get_func_spec_md(filename: str):
    # Example filename: "L8_FunctionalSpecification.md"
    # Assuming files saved in: ./output/generated_output_for_reference/
    # md_file_path = Path(config['source_path']['base_dir_default']) / "output" / "generated_output_for_reference" / filename
    md_file_path = Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications" / filename
    if not md_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Markdown file '{filename}' not found."
        )
    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Response as plain text or text/markdown
    return Response(content=content, media_type="text/markdown")

@app.post("/consolidate-functional-spec/")
async def consolidated_functional_spec(
    app_name: Annotated[str, Form()] = "LTCHPPSPricerMFApp2021",
    config_file: UploadFile = File(...)
):
    application_name = app_name
    if not config_file.filename.endswith((".yml", ".yaml")):
        raise HTTPException(status_code=400, detail="Only yaml files are allowed..")

    try:
        contents = await config_file.read()
        file_content_str = contents.decode('utf-8')
        parsed_yaml = yaml.safe_load(file_content_str)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred.. {e}") 

    if isinstance(parsed_yaml, list):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "FS Consolidation Config YAML must be a dictionary. Failed to consolidate Functional Specifications."
            }
        )

    # 🔹 This should return the path to the generated PDF file
    results = consolidated_func_spec(application_name, parsed_yaml)

    # Ensure results is a path string or Path object
    pdf_path = Path(results)  

    if not pdf_path.exists():
        raise HTTPException(status_code=500, detail="PDF generation failed.")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name
    )  

  # return {
    #     "Application_name" : application_name,
    #     "file_name" : config_file.filename,
    #     "consolidated_specs" : results
    # }
        
    
    
class OODesignRequest(BaseModel):
    functional_spec : str                        
    context : Optional[str] = None
    
@app.post("/generate-oo-design-doc",summary="Consolidated Functional spec generated previously is the input ")
async def oo_design_document(request : OODesignRequest):
    try:
        agent = ObjectOrientedDesignerAgent()
        base_dir ="."
        result = agent.execute(
            functional_spec = request.functional_spec,
            base_dir = base_dir
        )
        return {"design" : result.content if hasattr(result, "content") else str(result)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
   
 ### API 7 To generate the class diagram using the mermaid code. given by agent 
    
class MermaidDiagramRequest(BaseModel):
    diagram_type : Literal["class_diagram","flow_diagram","mind_map_diagram"]
    data_for_diagram : str     #### OO-dsign document 
    
    
class MermaidDiagramResponse(BaseModel):
    diagram_type : str
    diagram_text : str

    
@app.post("/generate-mermaid-diagram", summary="Class Diagram Generation, OO-Design Document as data_for_diagram") #, response_model = MermaidDiagramResponse
async def generate_mermaid_diagram(request: MermaidDiagramRequest):
    try:
        agent = MermaidDiagramGeneratorAgent()
        result = agent.execute(
                diagram_type = request.diagram_type,
                data_for_diagram = request.data_for_diagram
        )
        diagram_text=  result.content if hasattr(result,"content") else result
        
        if diagram_text == "This is the dummy content in bytes.":
        
            diagram_text = sample_mermaid_class_diagram()
            
            url = "https://kroki.io/mermaid/svg"
            headers = {"Content-Type": "text/plain"}

            response = requests.post(url, data=diagram_text.encode("utf-8"), headers=headers,verify=False)
            if response.status_code == 200:
                return Response(content=response.content, media_type="image/svg+xml")
            return {"error":response.status_code, "details":response.text}
        

    #     return MermaidDiagramResponse(
    #         diagram_type=request.diagram_type, 
    #         diagram_text = diagram_text,
    # )
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))

    

## To generate the JAVA or PYTHON Code from the Object Oriented Design & Functional Spec Generated Previously...

class GenerateCodeRequest(BaseModel):
    functional_spec : str                        
    context : Optional[str] = None
    design_content : str
    language : str             ## JAVA / PYTHON

@app.post("/generate-code",summary="use the contents of Consolidated Functional spec document and OO-Design document as inputs")
async def oo_design_document(request : GenerateCodeRequest):
    try:
        agent = ObjectOrientedCoderAgent()
        base_dir ="."
        result = agent.execute(
            oo_design=request.design_content, 
            functional_spec=request.functional_spec,
            language=request.language,
            base_dir=base_dir
        )
        print(result.content)
        return {"code" : result.content , "language":request.language if hasattr(result, "content") else str(result)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
