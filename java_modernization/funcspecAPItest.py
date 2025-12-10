# from agents import ReverseEngineeringAgentManager
# from pathlib import Path
# import os
# from config import load_config


# config = load_config()
# agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
# fs_agent = agent_manager.get_agent("generate_functional_spec")



# def read_files_in_directory(folder_path):
#     """
#     Lists all files in the given folder path and reads their content one by one.
#     Args:
#         folder_path (str): The path to the directory.
#     """
#     if not os.path.isdir(folder_path):
#         print(f"Error: The provided path '{folder_path}' is not a valid directory.")
#         return

#     print(f"Reading files from: {folder_path}\n")

#     file_list = os.listdir(folder_path)
#     return file_list


# def functional_spec(code_path):
#     output = {}
#     #source_code_path_default="C:\\SeenuWS\\CodeSpectre\\java_modernization\\JavaSpringApplications"
#     if code_path:
#         section_type="extract_program_overview"
#         folder_path = f"{code_path}\\LogicalUnits"              #C:\Extracted_dir\JavaSpringApplications\LogicalUnits
#         output_path = f"{code_path}\\FunctionalSpecs"
#         os.makedirs(output_path, exist_ok=True)
#         #folder_path=r"C:\SeenuWS\CodeSpectre\java_modernization\code_extractor\controller_wise_code_snippets"
#         file_list=read_files_in_directory(folder_path)
#         no_files=1
#         for filename in file_list:
#             file_path = os.path.join(folder_path, filename)
#             filename_only, _ = os.path.splitext(filename)
#             no_files+=1
#             if os.path.isfile(file_path):
#                 print(f"--- Reading content of: {filename} ---")
#                 try:
#                     with open(file_path, 'r', encoding='utf-8') as f:
#                         content = f.read()         
#                         functional_spec_content = fs_agent.execute(
#                                        code=content,
#                                        section_type=section_type)
#                         if functional_spec_content:
#                             with open(f"{output_path}\\{filename_only}_FS.md",'w') as file:
#                                 file.write(functional_spec_content)
#                             output.update({f"{filename_only}_Functional_Specifications":functional_spec_content})
#                     print(f"--- End of {filename} ---\n")
#                 except Exception as e:
#                     print(f"Error reading file {filename}: {e}\n")
#         if output:
#             return output

#functional_spec()


# import os
# import asyncio
# from pathlib import Path
# from functools import lru_cache
# from typing import Dict, Any

# from agents import ReverseEngineeringAgentManager
# from config import load_config

# # --- 1. Load Configurations and Initialize Agents ---
# config = load_config()
# agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
# fs_agent = agent_manager.get_agent("generate_functional_spec")

# # --- 2. The Core Fix: Separate Caching and Async Calls ---

# @lru_cache(maxsize=256)
# def _get_spec_from_llm_sync(code_content: str, section_type: str) -> str:
#     """
#     A synchronous, cached function that calls the blocking LLM agent.
    
#     The @lru_cache decorator caches the string result of this function, 
#     not a coroutine object.
#     """

#     return fs_agent.execute(
#         code=code_content,
#         section_type=section_type
#     )

# async def get_functional_spec_from_llm(code_content: str, section_type: str) -> str:
#     """
#     An async wrapper that runs the cached function in a separate thread.
    
#     This ensures a new coroutine is created for every call, avoiding the reuse error.
#     """
#     return await asyncio.to_thread(_get_spec_from_llm_sync, code_content, section_type)

# def read_files_in_directory(folder_path: str) -> list[str]:
#     """
#     Lists all files in the given folder path.
#     """
#     if not os.path.isdir(folder_path):
#         print(f"Error: The provided path '{folder_path}' is not a valid directory.")
#         return []
    
#     print(f"Reading files from: {folder_path}\n")
#     return os.listdir(folder_path)

# # --- 3. Main Logic (Remains largely the same) ---

# async def functional_spec(code_path: str) -> Dict[str, str]:
#     """
#     Generates a functional specification by processing code files concurrently.
#     """
#     output = {}
    
#     if not code_path:
#         print("Error: code_path is not provided.")
#         return output

#     section_type = "extract_program_overview"
#     folder_path = Path(code_path) / "LogicalUnits"
#     output_path = Path(code_path) / "FunctionalSpecs"
    
#     if not folder_path.exists() or not folder_path.is_dir():
#         print(f"Error: LogicalUnits folder not found at {folder_path}")
#         return output

#     os.makedirs(output_path, exist_ok=True)
    
#     file_list = read_files_in_directory(str(folder_path))

#     # Create a list of async tasks for concurrent execution
#     tasks = []
    
#     for filename in file_list:
#         file_path = folder_path / filename
#         if file_path.is_file():
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read()
                    
#                     # Create a task for each file to run the LLM call concurrently
#                     tasks.append(
#                         get_functional_spec_from_llm(content, section_type)
#                     )
#             except Exception as e:
#                 print(f"Error reading file {filename}: {e}")

#     print(f"Submitting {len(tasks)} LLM tasks concurrently...")
    
#     # Run all tasks in parallel
#     results = await asyncio.gather(*tasks)

#     # Process results and write to files sequentially
#     for i, result_content in enumerate(results):
#         filename = file_list[i]
#         filename_only, _ = os.path.splitext(filename)
        
#         if result_content:
#             output_file_path = output_path / f"{filename_only}_FS.md"
#             with open(output_file_path, 'w', encoding='utf-8') as file:
#                 file.write(result_content)
#             output[f"{filename_only}_Functional_Specifications"] = result_content
#             print(f"Processed and saved spec for {filename}")

#     return output










# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from pathlib import Path
# import asyncio

# from todocx import md_string_to_docx  
# from agents import ReverseEngineeringAgentManager
# from config import load_config

# # Initialize global resources
# config = load_config()
# agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
# fs_agent = agent_manager.get_agent("generate_functional_spec")

# MAX_CONCURRENT_LLM_CALLS = 5
# llm_semaphore = asyncio.Semaphore(MAX_CONCURRENT_LLM_CALLS)

# app = FastAPI(title="Functional Specification Generator")


# class FilePathRequest(BaseModel):
#     filepath: str


# @app.post("/generate-functional-spec-individual-file/")
# async def generate_functional_spec_for_file(request: FilePathRequest):
#     """
#     Generates functional specification, converts to DOCX,
#     saves to disk, and returns it as a downloadable FileResponse.
#     """
#     input_filepath = Path(request.filepath)
#     if not input_filepath.is_file():
#         raise HTTPException(status_code=404, detail=f"File not found: {input_filepath}")

#     filename = input_filepath.stem
#     section_type = "extract_program_overview"

#     try:
#         # read code file
#         with open(input_filepath, "r", encoding="utf-8") as f:
#             content = f.read()

#         # run agent to generate markdown
#         async with llm_semaphore:
#             functional_spec_content = await asyncio.to_thread(
#                 fs_agent.execute,
#                 code=content,
#                 section_type=section_type,
#             )

#         if not functional_spec_content:
#             raise HTTPException(status_code=500, detail="No functional spec generated")

#         # output docx path
#         output_docx_path = Path(f"{filename}_FS.docx")

#         # generate docx and save
#         final_path = md_string_to_docx(
#             functional_spec_content,
#             output_file=str(output_docx_path),
#             title=f"📄 Functional Specification for {filename}",
#         )

#         # return as downloadable file
#         return FileResponse(
#             path=final_path,
#             filename=Path(final_path).name,
#             media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import asyncio
import os
from fastapi.middleware.cors import CORSMiddleware
from todocx import md_string_to_docx, md_string_to_pdf  
from agents import ReverseEngineeringAgentManager
from config import load_config

# Initialize global resources
config = load_config()
agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
fs_agent = agent_manager.get_agent("generate_functional_spec")

MAX_CONCURRENT_LLM_CALLS = 5
llm_semaphore = asyncio.Semaphore(MAX_CONCURRENT_LLM_CALLS)

app = FastAPI(title="Functional Specification Generator")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FilePathRequest(BaseModel):
    filepath: str
    file_name :str

@app.post("/generate-functional-spec-individual-file/")
async def generate_functional_spec_for_file(request: FilePathRequest):
    """
    Generates functional specification, converts to DOCX,
    saves to disk, and returns JSON with download URL + spec content.
    """

    path = request.filepath
    folder_path = f"{path}\\LogicalUnits\\{request.file_name}"
    input_filepath = Path(folder_path)
    if not input_filepath.is_file():
        raise HTTPException(status_code=404, detail=f"File not found: {input_filepath}")

    filename = input_filepath.stem
    section_type = "extract_program_overview"
    try:
        # read code file
        with open(input_filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # run agent to generate markdown
        async with llm_semaphore:
            functional_spec_content = await asyncio.to_thread(
                fs_agent.execute,
                code=content,
                section_type=section_type,
            )

        if not functional_spec_content:
            raise HTTPException(status_code=500, detail="No functional spec generated")

        # output docx path
        output_path = Path(path) / "FunctionalSpecs"
        os.makedirs(output_path, exist_ok=True)
    

        # generate pdf document and save
        final_path = md_string_to_pdf(
            functional_spec_content,
            output_file=f"{filename}_FS.pdf",
            title=f"Functional Specification for {filename}",
            output_path = output_path
        )

        # return JSON with download URL + spec content
        return {
            "download_url": f"/download/{Path(final_path).name}",
            "functional_spec": {filename: functional_spec_content}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GetDocxRequest(BaseModel):
    filepath: str
    file_name :str

@app.post("/func-spec-document-file")
async def spec_docx_file(request : GetDocxRequest):
    """
    Endpoint to serve generated DOCX files.
    """
    docx_path = f"{request.filepath}\\FunctionalSpecs\\{request.file_name}"
    file_path = Path(docx_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


class GetPDFRequest(BaseModel):
    filepath: str
    file_name :str


@app.post("/funcspec-from-pdf-files/") # Changed endpoint name for clarity
async def funcspecs_from_md_files(request : GetPDFRequest): 

    path1 = f"{request.filepath}\\FunctionalSpecs"
    filename = request.file_name
    PDF_DIRECTORY = Path(path1)
    if not PDF_DIRECTORY.is_dir():
        raise HTTPException(
            status_code=500, detail="PDF storage directory not found on server."
        )
    file_path = PDF_DIRECTORY/filename

     # 🔹 Check if the file exists and is a file
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")
    
     # 🔹 Return the file as a FileResponse
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
