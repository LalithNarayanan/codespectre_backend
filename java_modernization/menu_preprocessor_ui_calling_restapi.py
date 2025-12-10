import streamlit as st
from pathlib import Path
import os
import json
import requests # Import the requests library for making HTTP calls

# Assuming config and utils are available in your project structure
# For this example, I'll define a dummy config and logger for demonstration.
# In your actual application, ensure these are properly loaded.
class DummyConfig:
    def __init__(self):
        self.config = {
            'source_path': {'base_dir_default': 'C:\\SeenuWS\\CodeSpectre\\JavaSpringApplications'},
            'api_base_url': 'http://localhost:8000' # IMPORTANT: Set your FastAPI server URL here
        }
    def __getitem__(self, key):
        return self.config[key]

class DummyLogger:
    def info(self, message):
        print(f"INFO: {message}")
    def error(self, message):
        print(f"ERROR: {message}")

config = DummyConfig()
logger = DummyLogger() # Use your actual logger instance

# Base directory from config (if used for local file operations)
base_dir = config['source_path']['base_dir_default']
API_BASE_URL = config['api_base_url']

def generate_ast(project_path, output_ast_path=""):
    """
    Calls the AST generation REST API and saves the returned AST to a file.
    """
    st.info(f"Sending request to generate AST for project: {project_path}")
    ast_api_url = f"{API_BASE_URL}/generate_ast"
    payload = {"project_path": str(project_path), "output_ast_path": str(output_ast_path)} # Ensure project_path is a string

    try:
        with st.spinner("Generating AST via API... This might take a while if the server is processing a long task."):
            response = requests.post(ast_api_url, json=payload, timeout=600) # Set a generous client-side timeout

        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        ast_data = response.json()

        if "status" in ast_data and ast_data['status'] == "success": 
            logger.info(f"AST successfully generated and saved to {ast_data['output_file']}")
            st.success(f"AST is generated successfully and saved to {ast_data['output_file']}")
        else:
            st.error("API response did not contain 'ast_json'.")
            logger.error(f"AST generation API response missing 'ast_json': {ast_data}")

    except requests.exceptions.Timeout:
        st.error("The AST generation API request timed out. The server might still be processing.")
        logger.error(f"AST generation API timeout for {project_path}")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the FastAPI server at {API_BASE_URL}. Please ensure the server is running.")
        logger.error(f"Connection error to {API_BASE_URL} for AST generation.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error during AST generation: {e}")
        logger.error(f"HTTP error during AST generation: {e}, Response: {e.response.text}")
    except json.JSONDecodeError:
        st.error("Failed to decode JSON response from AST generation API.")
        logger.error(f"JSON decode error from AST generation API. Response: {response.text}")
    except Exception as e:
        st.error(f"An unexpected error occurred during AST generation: {e}")
        logger.error(f"Unexpected error in generate_ast: {e}")


def load_into_grapdb(output_ast_path=""):

    try:
        graph_api_url = f"{API_BASE_URL}/load_into_graphdb"
        # Send the AST as a JSON string in the payload
        payload = {"output_ast_path": output_ast_path}

        print(f"graph_api_url: {graph_api_url}")
        with st.spinner("Loading AST into GraphDB via API..."):
            response = requests.post(graph_api_url, json=payload, timeout=600) # Set a generous client-side timeout

        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        st.success(f"AST is converted to Node and loaded into GraphDB successfully: {result.get('message', 'No message from API')}")
        logger.info(f"GraphDB loading successful: {result}")

    except requests.exceptions.Timeout:
        st.error("The GraphDB loading API request timed out. The server might still be processing.")
        logger.error(f"GraphDB loading API timeout ")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the FastAPI server at {API_BASE_URL}. Please ensure the server is running.")
        logger.error(f"Connection error to {API_BASE_URL} for GraphDB loading.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error during GraphDB loading: {e}")
        logger.error(f"HTTP error during GraphDB loading: {e}, Response: {e.response.text}")
    except json.JSONDecodeError:
        st.error("Failed to decode JSON response from GraphDB loading API.")
        logger.error(f"JSON decode error from GraphDB loading API. Response: {response.text}")
    except Exception as e:
        st.error(f"An unexpected error occurred during GraphDB loading: {e}")
        logger.error(f"Unexpected error in load_into_grapdb: {e}")

def extract_code_snippets(project_path):
    try:
        api_url = f"{API_BASE_URL}/extract_code_snippet"
        # Send the AST as a JSON string in the payload
        payload = {"project_path": project_path}
        print(f"api_url: {api_url}")
        with st.spinner("Extracting Code Snippet via API..."):
            response = requests.post(api_url, json=payload, timeout=600) # Set a generous client-side timeout

        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()
        st.success(f"Code is extracted  successfully:  {result.get('message', 'No message from API')}")
        logger.info(f"GraphDB loading successful: {result}")

    except requests.exceptions.Timeout:
        st.error("The GraphDB loading API request timed out. The server might still be processing.")
        logger.error(f"GraphDB loading API timeout ")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the FastAPI server at {API_BASE_URL}. Please ensure the server is running.")
        logger.error(f"Connection error to {API_BASE_URL} for GraphDB loading.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error during GraphDB loading: {e}")
        logger.error(f"HTTP error during GraphDB loading: {e}, Response: {e.response.text}")
    except json.JSONDecodeError:
        st.error("Failed to decode JSON response from GraphDB loading API.")
        logger.error(f"JSON decode error from GraphDB loading API. Response: {response.text}")
    except Exception as e:
        st.error(f"An unexpected error occurred during GraphDB loading: {e}")
        logger.error(f"Unexpected error in load_into_grapdb: {e}")

def app():
    # --- Header Section ---
    st.subheader("📝 Pre process Java Application")
    st.markdown("""
    Generation of AST (Abstract Syntax Tree). \n
    Creation of Node Graph for the generated AST.
    """)
    source_code_path_default = "JavaApplication1"
    output_folder_default = ""

    # --- Input Fields ---
    st.subheader("📁 Configuration")
    source_code_path = st.text_input("Source Code Path:", value=source_code_path_default, help="Path to Java Spring Application root directory.")
    output_ast_path = st.text_input("Output AST JSON Path:", value=str(output_folder_default), help="Directory to save the generated AST JSON file.")

    # --- Tabs for Functionality ---
    tab1, tab2, tab3 = st.tabs(["🚀 AST Generation", "✨ Load into GraphDB", "📄 Code Snippet Extraction"])

    with tab1:
        st.subheader("Abstract Syntax Tree Generation")
        st.markdown("Generate Abstract Syntax Tree structure (JSON format) for all Java classes in the specified source code path.")
        with st.container():
            if st.button("Generate AST", key="generate_ast_button"):
                if source_code_path:
                    # Ensure the output directory exists before passing to the function
                    Path(output_ast_path).mkdir(parents=True, exist_ok=True)
                    generate_ast(source_code_path, output_ast_path=output_ast_path)
                else:
                    st.warning("Please provide a source code path.")
        st.markdown("---")

    with tab2:
        st.subheader("Load AST into GraphDB")
        st.markdown("Load the previously generated AST (from the JSON file) into a Graph Database.")
        with st.container():
            if st.button("Load to GraphDB", key="load_to_graphdb_button"):
                if output_ast_path:
                    load_into_grapdb(output_ast_path)
                else:
                    st.warning("Please ensure the output AST path is set and AST is generated.")
        st.markdown("---")
    
    with tab3:
        st.subheader("Source Code Extraction")
        st.markdown("Extract the code snipperts")
        with st.container():
            if st.button("Extract Code Snippet", key="extract_code_snippets"):
                if source_code_path:
                    extract_code_snippets(project_path=source_code_path)
                else:
                    st.warning("Please ensure the output AST path is set and AST is generated.")
        st.markdown("---")

# --- Run the App ---
if __name__ == "__main__":
    app()