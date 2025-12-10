import streamlit as st
from pathlib import Path
import os
# Assuming config and utils are available in your project structure
from config import load_config
from utils.logger import logger
import yaml
import re
import base64
import json
# import preprocessor.ast_generator as ast_generator

from preprocessor.ast_generator import ASTGenerator
from preprocessor.ast_generator import GraphLoader


config = load_config()
logger = logger # Use your actual logger instance
base_dir=config['source_path']['base_dir_default']



    # ast = ASTGenerator(
    #     project_path=Path(project_path)
    # ).get_ast()

    # with open(os.path.join(output_ast_path, "java_project_ast.json"), 'w') as ast_fp:
    #     json.dump(ast, ast_fp)

    # with open(os.path.join(output_ast_path, "java_project_ast.json"), 'r') as ast_fp:
    #     ast = json.load(ast_fp)
    
    # gl = GraphLoader(
    #     ast_to_load=ast
    # ).load()


def generate_ast(project_path,output_ast_path=""):
    """Placeholder for generating functional specifications."""
    print(f"project_path: {project_path}")
    ast = ASTGenerator(
         project_path=Path(project_path)
     ).get_ast()

    with open(os.path.join(output_ast_path, "java_project_ast.json"), 'w') as ast_fp:
         json.dump(ast, ast_fp)
    print(f'ast=>{ast}')
    st.success("AST is generated successfully")

    return

def load_into_grapdb(output_ast_path=""):
    with open(os.path.join(output_ast_path, "java_project_ast.json"), 'r') as ast_fp:
         ast = json.load(ast_fp)
    
    gl = GraphLoader(
         ast_to_load=ast
     ).load()
    
    st.success("AST is convereted to Node and loaded into GraphDB successfully")

    return 


def app():
    # --- Header Section ---
    st.subheader("📝 Pre process Java Application") # Added document icon
    st.markdown("""
    Generation of  AST (Abstract Syntax Tree). \n
    Creation of Node Graph for the generated AST    """)
    source_code_path_default="C:\\KanagWS\\PythonWS1\\CodeSpectre\\JavaSpringApplications"
    # --- Input Fields ---
    st.subheader("📁 Configuration File") # Added folder icon
    source_code_path = st.text_input("Source Code Path:", value=source_code_path_default, help="Path Java Spring Application") # Added help text and icon idea
    
    # --- Tabs for Functionality ---
    # tab1, tab2 = st.tabs(["🚀 AST Generation and Loading t", "✨ Consolidate Specs"]) # Added icons
    
    tab1, tab2 = st.tabs(["🚀 AST Generation", "✨ Load into GraphDB"]) # Added icons
    with tab1:
        st.subheader("Abstract Syntax Tree Generation") # Use header for tab title
        st.markdown("Generate individual functional specifications for logical units defined in the source code configuration.")
        # Using a container for the button and spinner
        with st.container():
            if st.button("Generate AST",key="generate_ast"): # Button text
                # Generate spec if code was read
                if source_code_path:
                    output_folder=r"C:/KanagWS/PythonWS1/CodeSpectre/JavaSpringApplications/output/ast_json"
                    generate_ast(source_code_path,output_ast_path=output_folder)
                    

        st.markdown("---") # Separator

    with tab2:
        st.subheader("Abstract Syntax Tree Generation") # Use header for tab title
        st.markdown("For the all Java classes Abstract Syntax Tree structure (json format) will be created")
        # Using a container for the button and spinner
        with st.container():
            if st.button("Load to GraphDB", key="load_to_graphdb"): # Button text
                if source_code_path_default:
                    # folder_path=r"C:\KanagWS\CodeSpectreWS\code_extractor\controller_wise_code_snippets"
                    output_ast_path=r'C:/KanagWS/PythonWS1/CodeSpectre/JavaSpringApplications/output/ast_json'
                    load_into_grapdb(output_ast_path)
                      
        st.markdown("---") # Separator

    

# --- Run the App ---
if __name__ == "__main__":
    app()
