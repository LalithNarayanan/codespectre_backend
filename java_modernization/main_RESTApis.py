import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
import json

from preprocessor.ast_generator import ASTGenerator, GraphLoader
from preprocessor.doc_gen import DocGen
#from funcspecAPItest import functional_spec


app = FastAPI(title="AST & GraphDB API", version="1.0")
base_dir=r"C:\SeenuWS\CodeSpectre\JavaSpringApplications"
# project_path = r'C:\KanagWS\CodeSpectreWS\JavaSpringApplications\JavaApplication1'
output_ast_path = ""

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class GenerateASTRequest(BaseModel):
    project_path: str
    output_ast_path: str

class LoadGraphDBRequest(BaseModel):
    output_ast_path: str

class ExtractCodeSnippetRequest(BaseModel):
    project_path: str

class GenerateSpecRequest(BaseModel):
    project_path: str

@app.post("/generate_ast")
def generate_ast_endpoint(request: GenerateASTRequest):
    try:
        #project_path = Path(base_dir)/(request.project_path)
        #output_path = Path(base_dir)/Path(request.output_ast_path)/"ast_in_json"
        project_path = Path(request.project_path)
        output_path = Path(request.output_ast_path)/"AST_in_JSON"
        print(f"project path: {project_path}")
        print(f"output path: {output_path}")

        ast = ASTGenerator(project_path=project_path).get_ast()

        os.makedirs(output_path, exist_ok=True)

        ast_file = output_path / "java_project_ast.json"
        with open(ast_file, "w") as ast_fp:
            json.dump(ast, ast_fp)

        return {"status": "success", "message": "AST generated", "output_file": str(ast_file),"ast":ast}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/load_into_graphdb")
def load_into_graphdb_endpoint(request: LoadGraphDBRequest):
    try:
        #output_ast_path = Path(base_dir)/Path(request.output_ast_path)/"ast_in_json"
        output_ast_path = Path(request.output_ast_path)/"AST_in_JSON"
        ast_file = Path(output_ast_path) /  "java_project_ast.json"
        print(f"ast file: {ast_file}")
        if not ast_file.exists():
            raise HTTPException(status_code=404, detail="AST file not found")
        
        processed_file = Path(output_ast_path) / "onloaded_ast.json"
        print(f"processed file: {processed_file}")
        if processed_file.exists():
            raise HTTPException(status_code=404, detail="AST is already onboarded into GraphDB")

        with open(ast_file, "r") as ast_fp:
            ast = json.load(ast_fp)

        GraphLoader(ast_to_load=ast).load()
        #Once the file is load , create a file to indicate it is processed
        with open(processed_file, "w") as processed_fp:
            json.dump(ast, processed_fp)

        return {"status": "success", "message": "AST loaded into GraphDB"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract_code_snippet")
def extract_code_snippet(request: ExtractCodeSnippetRequest):

    try:
        #project_path = Path(base_dir)/(request.project_path)
        project_path = Path(request.project_path)
        print(f"extract_code_snippet project path1: {project_path}")

        # GOOGLE_MODEL_NAME = "gemini-2.5-flash"
        # NEO4J_URI = "neo4j://127.0.0.1:7687"
        # NEO4J_USERNAME ="neo4j"
        # NEO4J_PASSWORD = "test@123"  #instance password
        # NEO4J_DATABASE_NAME = "java-ast"  #database base 

        docObj = DocGen(
            # project_path=r"C:\Users\Narasimha\Documents\java_spring_project"
            project_path=project_path,
        )
        response=docObj.get_controllerclasses_as_chunks()

        print(response[0][0][0])
        #level 1 - list of controllers
        #level 2 - for each controller, list of methods
        #level 3 - for each method, list of 1000 lines chunks
        
        # TODO
        # os.makedirs(output_path, exist_ok=True)
        # ast_file = output_path / "java_project_ast.json"
        # with open(ast_file, "w") as ast_fp:
        #     json.dump(ast, ast_fp)
        output_path =f"{project_path}\\LogicalUnits"
        os.makedirs(output_path, exist_ok=True)

        for item_list_level1 in response:
            for item_list_level2 in item_list_level1:
                for code_snippet_string in item_list_level2:
                # Extract the Class Name
                    class_name_match = re.search(r"Class Name: (.*?)\s*- > Method Name:", code_snippet_string)
                    if class_name_match:
                        class_name = class_name_match.group(1).strip()
                        filename = re.sub(r'[^a-zA-Z0-9_.-]', '', class_name) + ".txt"

                        # Get the entire content of the code snippet string
                        entire_content = code_snippet_string.strip()

                        file_path=f"{output_path}\\{filename}"
                        with open(file_path, "a") as f:  # Use "a" to append if class name repeats
                            f.write(entire_content)
                            f.write("\n\n") # Add a newline for separation if appending

                        print(f"Appended code for class '{class_name}' to '{file_path}'")

        return {"status": "success", "message": "Logical Units extracted", "output_file": output_path,"code":response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PathRequest(BaseModel):
    path: str

@app.post("/list_files/")
def list_files_in_path(request: PathRequest):
    """
    Returns a list of file names in the specified directory path.
    """
    try:
        # Access the path from the Pydantic model instance
        p = Path(request.path)

        # Check if the path exists and is a directory
        if not p.exists() or not p.is_dir():
            raise HTTPException(status_code=404, detail="Path not found or is not a directory.")

        # Get all file names (not directories) in the path
        files = [item.name for item in p.iterdir() if item.is_file()]

        # Return the response as a dictionary
        return {"path": request.path, "files": files}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    






# @app.post("/generate-functinal-specification/")
# async def generate_functional_spec(request: GenerateSpecRequest):
#     try: 
#         path = request.project_path
#         folder_path = f"{path}\\LogicalUnits"

#         # Check if the folder_path exists
#         if not os.path.exists(folder_path):
#             raise HTTPException(
#                 status_code=404, 
#                 detail="Please extract Logical Units to generate Functional Specifications"
#         )

#         print(f"project path: {path}")
#         results = functional_spec(path)
    
#         return {
#         "path": path,
#         "Specifications" : results
#         }
#     except HTTPException as e:
#         # If the raised exception is an HTTPException, re-raise it without modification.
#         raise e

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))