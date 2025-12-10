import streamlit as st
from pathlib import Path
import os
# Assuming config and utils are available in your project structure
from config import load_config
from utils.logger import logger
from agents import ReverseEngineeringAgentManager
from utils.file_util import save_to_file, read_program
import pandas as pd
import base64 # Import base64 for download link
from utils.code_parser import extract_and_save_content, extract_and_zip_files


config = load_config()
logger = logger # Use your actual logger instance
agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
code_agent = agent_manager.get_agent("oo_coder")


# Default values (adjust paths as necessary for your environment)
app_name_default = "COBOL to Java Converter" # More descriptive name
BASE_DIR_DEFAULT = Path("./mainframe_code/MyApp") # Use relative path or configure properly

# Placeholder functions for demonstration - Replace with your actual functions
def read_program_from_path(filepath):
    """Reads content from a file."""
    try:
        # Check if the path exists before attempting to open
        if not Path(filepath).exists():
            st.warning(f"File not found: {filepath}") # Changed to warning
            # logger.warning(f"File not found: {filepath}") # Use your logger
            return None
        with open(filepath, "r", encoding="utf-8") as f: # Specify encoding
            return f.read()
    except FileNotFoundError:
        st.warning(f"File not found: {filepath}") # Changed to warning
        # logger.warning(f"File not found: {filepath}") # Use your logger
        return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        # logger.error(f"Error reading file: {e}") # Use your logger
        return None

def save_to_file(filepath, content):
    """Saves content to a file, creating directories if necessary."""
    try:
        file_path = Path(filepath)
        file_path.parent.mkdir(parents=True, exist_ok=True) # Create parent directories
        with open(file_path, "w", encoding="utf-8") as f: # Specify encoding
            f.write(content)
        # logger.info(f"File saved successfully to: {filepath}") # Use your logger
    except Exception as e:
        st.error(f"Error saving file {filepath}: {e}")
        # logger.error(f"Error saving file {filepath}: {e}") # Use your logger


# def generate_code(design_input_file_path, functional_spec_input_file_path, base_dir,language="python"):
def generate_code(design_content, functional_spec_content,base_dir,context_content=None,  language="python"):
    """Placeholder for generating code."""
    # st.info(f"Generating {language} code generation...")
    try:
        if design_content is None or functional_spec_content is None:
             st.error("Could not read content from input files for code generation.")
             return None

        target_file_path = str(base_dir / "output" / f"generated_{language}_code.md") # Changed filename and extension
        oo_code = code_agent.execute(oo_design=design_content, functional_spec=functional_spec_content,language=language)
        save_to_file(target_file_path, oo_code.content)
        # st.success(f"Generated Code saved to: {target_file_path}")
        return target_file_path
    except FileNotFoundError:
        st.error(f"Design not found: {design_content} or Functional Spec file not found: {functional_spec_content}")
        # logger.error(f"Design file not found: {design_input_file_path} or Functional Spec file not found: {functional_spec_input_file_path}") # Use your logger
        return None
    except Exception as e:
        st.error(f"Error generating Code: {e}")
        # logger.error(f"Error generating Code: {e}") # Use your logger
        return None

# --- UI Helper Functions ---
def create_download_link_with_icon(content, filename, mime, icon="download"):
    """Creates a styled HTML download link with a Material Symbols icon."""
    # Ensure content is a string before encoding
    content_str = str(content)
    b64 = base64.b64encode(content_str.encode('utf-8')).decode()
    # Use a more robust styling approach for better consistency
    href = f"""
    <a href="data:{mime};base64,{b64}" download="{filename}"
       style="display: inline-flex; align-items: center; text-decoration: none; color: #005696; /* TCS Blue */
              padding: 5px 10px; border: 1px solid #005696; border-radius: 5px; background-color: #e0f2f7; /* Light Blue */
              transition: background-color 0.3s ease, color 0.3s ease;">
        <span style="font-size: 1.2em; margin-right: 0.5em;">
            <i class="material-symbols-outlined">{icon}</i>
        </span>
        <span style="font-size: 0.9em;">
            Download {filename}
        </span>
    </a>
    """
    return href


# --- Streamlit App Layout ---

def app():
    # --- Header Section ---
    css_path = os.path.join(os.path.dirname(__file__), 'design.css')
    with open(css_path) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)  

    st.subheader("💻 Generate Code") # Added code icon

    st.markdown("""
    Generate code based on the Object-Oriented Design and Functional Specifications.
    """)

   
    # --- Input Fields ---
    st.subheader("📄 Input Documents") # Added document icon

    # Using columns for better layout of input fields
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        # app_name = st.text_input("Application Name:", value=st.session_state.get('app_name', app_name_default), disabled=True)
        with st.container():
            app_name=st.session_state.get('app_name', app_name_default)
            st.write("Application Name:", app_name)
            language_choice = st.radio(
                "Select your preferred programming language:",
                ("python", "java"),
                index=0  # Sets "Python" as the default selected option
                )
    
    with col2:
    # Context path input (if still needed for code generation)
        context_path = st.text_input("Context File (Optional, .md file):", help="Provide an optional context file to influence the code generation.")

    with col3:
        with st.container():
            # st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)  # Spacer
            design_doc_path_from_state = st.session_state.get('generated_oo_design_path', None)
            st.markdown("<div style='margin-bottom: -100px; font-weight: bold;'>Design Path:</div>", unsafe_allow_html=True)
            st.text_input(
                # "OO Design Path (from previous step):",
                "",
                value=design_doc_path_from_state if design_doc_path_from_state else "Not generated yet",
                disabled=True,
                key="design_path_display"
            )
            # st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)  # Spacer
        with st.container():
            # File Uploader for Design Doc
            uploaded_design_file = st.file_uploader(
                "Or, Upload Design File (Optional, overrides path)",
                type=['md', 'txt'], # Adjust allowed types as needed
                key="design_uploader" # Use key to access state
            )

    with col4:
        # Use session state for default value if available from Functional Specs menu
        with st.container():    
            consolidated_fs_path_from_state = st.session_state.get('consolidated_fs_path', None)
            st.markdown("<div style='margin-bottom: -100px; font-weight: bold;'>Functional Specification:</div>", unsafe_allow_html=True)
            st.text_input(
                "",
                value=consolidated_fs_path_from_state if consolidated_fs_path_from_state else "Not generated yet",
                disabled=True,
                key="fs_path_display"
            )
        with st.container():
            # File Uploader for Design Doc
            uploaded_consolidated_fs_file = st.file_uploader(
                "Or, Upload Functional Specification (Optional, overrides path)",
                type=['md', 'txt'], # Adjust allowed types as needed
                key="fs_uploader" # Use key to access state
            )
    

    st.markdown("---") # Separator

    # --- Code Generation ---
    st.subheader("🔨 Generate Code") # Added hammer icon

    # Using a container for the button and spinner
    with st.container():
        # Check if required inputs are available in session state before enabling button
        button_disabled = 'generated_oo_design_path' not in st.session_state or 'consolidated_fs_path' not in st.session_state
        base_dir_temp = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
       
        temp_design_content=None
        temp_fs_content=None

        #check if the both design and FS files are uploaded 
        if uploaded_design_file is not None and uploaded_consolidated_fs_file is not None:
            button_disabled=False
            #print content of the both file
            temp_design_content=uploaded_design_file.read()
            temp_fs_content=uploaded_consolidated_fs_file.read()
            logger.info(f"temp_design_content:{temp_design_content}")
            logger.info(f"temp_fs_content:{temp_fs_content}")

        if st.button("Generate Code", disabled=button_disabled): # Button text, disabled if inputs missing
            if 'generated_oo_design_path' in st.session_state and 'consolidated_fs_path' in st.session_state:
                with st.spinner("Generating Code..."):
                    # Get filenames from stored paths in session state
                    design_filename = Path(st.session_state.generated_oo_design_path).name
                    fs_filename = Path(st.session_state.consolidated_fs_path).name
                    # Use session state for base_dir if available from Upload menu
                  
                    #read the content 
                    design_content=read_program_from_path(str(Path(base_dir_temp) / "output" / Path(design_filename).name))
                    functional_spec_content=read_program_from_path(str(Path(base_dir_temp) / "output" / Path(fs_filename).name))
                    context_content=""
                    
                    code_path = generate_code(
                        design_content=design_content,
                        functional_spec_content=functional_spec_content,
                        base_dir=base_dir_temp,
                        context_content=context_content,
                        language=language_choice
                    )
                    if code_path:
                        st.session_state.generated_code_path = code_path
                        st.success("✅ Code generated!") # Added checkmark icon
                    else:
                        st.error("Failed to generate Code.")
            
            #if the files are directly uploaded
            if temp_fs_content is not None and temp_design_content is not None:
                with st.spinner("Generating Code..."):
                    code_path = generate_code(
                        design_content=temp_design_content,
                        functional_spec_content=temp_fs_content,
                        base_dir=base_dir_temp,
                        context_content=None,
                        language=language_choice
                    )
                    if code_path:
                        st.session_state.generated_code_path = code_path
                        st.success("✅ Code generated!") # Added checkmark icon
                    else:
                        st.error("Failed to generate Code.")


        if button_disabled:
             st.warning("Generate Functional Specifications and OO Design first to enable code generation.") # Provide guidance


    # Display generated Code if available
    if 'generated_code_path' in st.session_state:
        st.subheader("📄 Generated Code") # Added file icon
        # Use session state for base_dir if available from Upload menu
        base_dir_temp = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
        # Construct the full path
        generated_code_path_full = base_dir_temp / "output" / Path(st.session_state.generated_code_path).name

        # Check if the file exists before attempting to read
        if generated_code_path_full.exists():
            code_content = read_program_from_path(str(generated_code_path_full))
            #parse the code using code_parser extract_and_save_content
            # extract_and_save_content(code_content)
            extract_and_zip_files(code_content)
            
            if code_content:
                st.code(code_content, language="java")
                # Provide download link
                download_link_html = create_download_link_with_icon(
                    code_content,
                    generated_code_path_full.name,
                    "text/plain", # Use text/plain for code files
                    icon="" # Added download icon
                )
                st.markdown(download_link_html, unsafe_allow_html=True)
            else:
                st.info("Generated code content could not be read.")
        else:
            st.error(f"Generated code file not found at {generated_code_path_full}")
    else:
        st.info("Generate code to view it here.")


# --- Run the App ---
if __name__ == "__main__":
    # Ensure base_dir is initialized in session state if not already present
    if 'base_dir' not in st.session_state:
         st.session_state['base_dir'] = str(BASE_DIR_DEFAULT)
    # Ensure app_name is initialized in session state if not already present
    if 'app_name' not in st.session_state:
         st.session_state['app_name'] = app_name_default

    app()
