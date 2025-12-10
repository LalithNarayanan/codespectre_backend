import streamlit as st
from pathlib import Path
import os
# Assuming config and utils are available in your project structure
from config import load_config
from utils.logger import logger
from agents import ReverseEngineeringAgentManager
from utils.file_util import save_to_file, read_program, combine_files_contents_from_csv
from utils.job_util import get_job_run_id_persistent, load_job_run_state
import yaml
import re
import base64

# Assuming load_config, logger, ReverseEngineeringAgentManager,
# save_to_file, read_program, combine_files_contents_from_csv,
# get_job_run_id_persistent, load_job_run_state are available globally or imported elsewhere

config = load_config()
logger = logger # Use your actual logger instance
agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
fs_agent = agent_manager.get_agent("generate_functional_spec")
fs_consolidate_agent = agent_manager.get_agent("consolidate_functional_specs")

BASE_DIR_DEFAULT=config['source_path']['base_dir_default']
PROJECT_NAME_DEFAULT=config['source_path']['proj_name_default']
BASE_DIR_PARENT=config['source_path']['base_dir_parent']
FUNCTIONAL_SPECIFICATION_FILES_DEFAULT =config['source_path']['fs_consolidation_config_default']
# config['source_path']['fs_consolidation_config_default']
# Initialize job ID (keep your existing logic, or use a placeholder)
job_id = get_job_run_id_persistent()
existing_job_id = load_job_run_state()


def load_config_from_yaml_upload(uploaded_file):
    """Loads configuration from an uploaded YAML file."""
    try:
        return yaml.safe_load(uploaded_file)
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file: {e}")
        # logger.error(f"Error parsing YAML file: {e}") # Use your logger
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading YAML: {e}")
        # logger.error(f"An unexpected error occurred while loading YAML: {e}") # Use your logger
        return None


# Placeholder functions for demonstration - Replace with your actual functions
def load_config_from_yaml(yaml_path):
    """Loads configuration from a YAML file."""
    try:
        # Check if the path exists before attempting to open
        if not Path(yaml_path).exists():
             st.error(f"Configuration file not found: {yaml_path}")
             # logger.error(f"Configuration file not found: {yaml_path}") # Use your logger
             return None
        with open(yaml_path, 'r', encoding="utf-8") as file: # Specify encoding
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error(f"YAML file not found: {yaml_path}")
        # logger.error(f"YAML file not found: {yaml_path}") # Use your logger
        return None
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file: {e}")
        # logger.error(f"Error parsing YAML file: {e}") # Use your logger
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading YAML: {e}")
        # logger.error(f"An unexpected error occurred while loading YAML: {e}") # Use your logger
        return None

#Read the program
def read_program_from_path(filepath):
    """Reads content from a file."""
    try:
        # Check if the path exists before attempting to open
        if not Path(filepath).exists():
            st.warning(f"File not found: {filepath}") # Changed to warning
            # logger.warning(f"File not found: {filepath}") # Use your logger
            return None
        with open(filepath, "r") as f: # Specify encoding
            return f.read()
    except FileNotFoundError:
        st.warning(f"File not found: {filepath}") # Changed to warning
        # logger.warning(f"File not found: {filepath}") # Use your logger
        return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        # logger.error(f"Error reading file: {e}") # Use your logger
        return None
    
#Save the file
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

#Generate functional specs
def generate_functional_spec(source_code, base_dir, job_id, record_id, programs, contexts=None):
    """Placeholder for generating functional specifications."""
    # st.info(f"Generation for {record_id}...")
    # Replace with your actual agent execution logic
    functional_spec_content = fs_agent.execute(job_id=job_id, record_id=record_id,
                                       base_dir=base_dir, code=source_code,
                                       programs=programs, contexts=contexts)

    target_file_path = str(Path(base_dir) / "output" / f"{record_id}_FunctionalSpecification.md")
    save_to_file(target_file_path, functional_spec_content)
    #TODO
    # st.success(f"Job Id:{job_id}, \n Functional Specifications generated for {record_id}. Programs: {programs} and saved to: {target_file_path}")
    # logger.info(f"\n********* {job_id}_{record_id} is saved at {target_file_path}  **************") # Use your logger

    view_file_in_expander_with_download(target_file_path)  # Call the function to display in expander

    if 'generated_spec_paths' not in st.session_state:
        st.session_state['generated_spec_paths'] = []
    st.session_state['generated_spec_paths'].append(target_file_path)

    # --- NEW: Automatically run validation on the generated spec ---
    try:
        validation_agent = agent_manager.get_agent("validation_agent")
        validation_agent.execute(
            job_id=job_id,
            record_id=record_id,
            base_dir=str(base_dir),
            source_code=source_code,
            functional_spec=functional_spec_content,
        )
        # Display the saved validation report
        validation_report_path = str(Path(base_dir) / "output" / f"{job_id}_{record_id}_validation.md")
        view_file_in_expander_with_download(validation_report_path)
    except Exception as e:
        st.warning(f"Validation step failed for {record_id}: {e}")

    return target_file_path

#Consolidate functional specs
def consolidate_functional_specs(config_data, base_dir, merged_fs_file_name="consolidated_FunctionalSpecification.md"):
    """Placeholder for consolidating functional specifications."""
    # st.info("Consolidation...")
    target_file_path = str(Path(base_dir) / "output" / merged_fs_file_name)

    if not config_data:
        return None

    # Basic validation of config_data structure
    if not isinstance(config_data, dict):
        st.error("FS Consolidation Config YAML must be a dictionary.")
        return None
    if 'functional_specificiations' not in config_data or 'sections' not in config_data:
        st.error("FS Consolidation Config YAML must contain 'functional_specificiations' and 'sections' keys.")
        return None
    if not isinstance(config_data['functional_specificiations'], list) or not isinstance(config_data['sections'], list):
         st.error("'functional_specificiations' and 'sections' in FS Consolidation Config YAML must be lists.")
         return None

    combined_functional_spec = ""
    functional_specs = config_data.get('functional_specificiations', [])
    sections = config_data.get('sections', [])
    action_str = config_data.get('action', 'process') # Default action is 'process'

    if action_str.lower() == "process": # Case-insensitive check
        # Get the contexts
        contexts = {}
        context_keys = ['context_1', 'context_2', 'context_3']
        for key in context_keys:
            context_value = config_data.get(key)
            if context_value:
                # Determine if context is a file path or direct content
                if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
                    context_path_temp = base_dir / "context" / context_value
                    context_content = read_program_from_path(str(context_path_temp))
                    if context_content is not None:
                         contexts[key] = context_content
                    else:
                         st.warning(f"Context file not found or readable for key '{key}': {context_path_temp}")
                         # logger.warning(f"Context file not found or readable for key '{key}': {context_path_temp}") # Use your logger
                else:
                    # Assume direct content
                    contexts[key] = context_value

        combined_functional_spec = "# Consolidated Functional Specification\n\n"
        for section in sections:
            # logger.info(f"section:>>>"{section}") # Use your logger
            combined_match = ""
            for spec in functional_specs:
                spec = spec.strip()
                # logger.info(f"spec=>>>>>>>>>>>>>>{spec}") # Use your logger
                fs_path = str(base_dir / "output" / spec)
                # logger.info(f"fs_path:>>>"{fs_path}) # Use your logger
                fs_content = read_program_from_path(fs_path)
                if fs_content is None:
                    continue # Skip if file not found or readable

                section_to_search = re.escape(section.strip())  # Escape special chars and remove extra spaces
                # Adjusted pattern to be more robust
                pattern = rf"^#\s+{section_to_search}\s*\n(.*?)(?:^#\s+|\Z)"
                # pattern = r"^#\s+Program Overview\s*\n(.*?)(?:^#\s+|\Z)" # Original pattern

                # logger.info(f"spec=>>>>>>>>>>>>>>{spec}-{pattern}") # Use your logger
                match = re.search(pattern, fs_content, re.MULTILINE | re.DOTALL)
                if match:
                    # logger.info("EXACT MATCH FOUND") # Use your logger
                    match_content = match.group(1).strip()
                    # logger.info(f"\n\n\n******************\match:>>>"{match_content} ******************end of match\n\n") # Use your logger
                    if match_content:
                        combined_match += f"**Content of '{section.strip()}' from '{spec}'**\n\n {match_content}\n\n---\n\n" # Added separator


            if combined_match:
                # Simulate agent execution for consolidation at section level
                combined_functional_spec_sectionlevel= fs_consolidate_agent.execute(job_id="job_id",
                                                                                    base_dir=base_dir,
                                                                                    section=section,
                                                                                    functional_specs=combined_match,
                                                                                    contexts=contexts
                                                                                    )

                combined_functional_spec += combined_functional_spec_sectionlevel.content + "\n \n"

        # logger.info(f"All sections are created.") # Use your logger
        save_to_file(target_file_path, combined_functional_spec)
        # logger.info(f"\n********* {job_id}_{section} is saved at {target_file_path}  **************") # Use your logger

    else:
        # logger.info(f"Consolidation is ignored due to action: {action_str}") # Use your logger
        st.info(f"Skipping consolidation as action is '{action_str}'.")
        return None
    #TODO
    # st.success(f"Consolidated Functional Specifications saved to: {target_file_path}")

    return target_file_path

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

def view_file_in_expander_with_download(target_file_path):
    """
    Displays the content of a file within a Streamlit expander with a styled download link.
    """
    file_path = Path(target_file_path)
    if file_path.is_file():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            filename = file_path.name
            mime = "text/markdown"  # Adjust mime type if necessary

            # Create download link using the styled function
            download_link_html = create_download_link_with_icon(file_content, filename, mime, icon="file_download")

            with st.expander(f"📄 View Specification: {filename}"): # Added file icon
                st.markdown(download_link_html, unsafe_allow_html=True)
                st.markdown("---") # Separator
                # Display code block for better readability of markdown content
                # st.code(file_content, language="markdown")
                st.markdown(file_content)

            # Link Material Symbols font
            st.markdown("""
                <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error reading file: {e}")
            # logger.error(f"Error reading file {target_file_path}: {e}") # Use your logger
    else:
        st.warning(f"File not found at: {target_file_path}") # Changed to warning for file not found
        # logger.warning(f"File not found at: {target_file_path}") # Use your logger


def display_all_generated_specifications():
    """Displays all generated functional specifications available in session state."""
    if 'generated_spec_paths' in st.session_state and st.session_state['generated_spec_paths']:
        st.subheader("Generated Functional Specifications:")
        # Display in reverse order to show latest first
        for file_path in reversed(st.session_state['generated_spec_paths']):
            view_file_in_expander_with_download(file_path)
    else:
        st.info("No functional specifications have been generated yet.")

# --- Streamlit App Layout ---
def app():
    # --- Header Section ---
    st.subheader("📝 Functional Specifications") # Added document icon
    st.markdown("""
    Generate Functional Specifications and consolidate them based on the configurations.
    """)

    # --- Input Fields ---
    st.subheader("📁 Configuration Files") # Added folder icon
    # Using columns for better layout of input fields
    # with col1:
    app_name = st.text_input("Application Name:", value=st.session_state.get('app_name', None), disabled=True)
    # source_code_logical_units_path_default = st.session_state.get('source_code_config_path', SOURCE_CODE_CONFIG_FILE_DEFAULT)
    # source_code_logical_units_path = st.text_input("Source Code Logical Units Config (uploaded):", value=source_code_logical_units_path_default, help="Path to the YAML file defining logical units and programs.") # Added help text and icon idea
    # config_data = load_config_from_yaml(source_code_logical_units_path)
    if st.session_state.get('source_code_config') is not None and st.session_state.get('source_code_config_path') :  
        st.markdown(f"Logical Unit Config File:")
        # st.write(f"{st.session_state.get('source_code_config_path')} ")
        config_data=st.session_state.get('source_code_config')
        path=st.session_state.get('source_code_config_path')
        if config_data:
            with st.expander(f"Show Uploaded {path} Content"):
                st.write(config_data)
        #TODO provide expander 
    else:
        st.write("Upload Source code Logical units configuration file first in the previous step")

    # Use session state for default value if available from Upload menu
    functional_specification_files_path_default = st.session_state.get('fs_consolidation_config_path', FUNCTIONAL_SPECIFICATION_FILES_DEFAULT)
    functional_specification_config_file_path = st.text_input("FS Consolidation Config :", value=functional_specification_files_path_default, help="Path to the YAML file defining functional specifications and sections for consolidation.") # Added help text and icon idea
    uploaded_file = st.file_uploader("Or, Upload Consolidation Config", type=["yaml", "yml"], 
                                        help="Upload the YAML file that configuration consolidation.") # Added help text and icon idea
    fs_config_data=None
    
    if uploaded_file is not None:
        try:
            # fs_config_data = uploaded_file.read()
            fs_config_data = load_config_from_yaml_upload(uploaded_file)
            if fs_config_data:
                with st.expander(f"Uploaded {uploaded_file.name} Content"):
                    st.write(fs_config_data)
            if fs_config_data is None:
                st.error(f"No data is present. Error reading file: {e}")
                return
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        fs_spec_path = str(functional_specification_config_file_path)
        try:
            fs_config_data = load_config_from_yaml(fs_spec_path)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    st.markdown("---") # Separator

    # --- Tabs for Functionality ---
    tab1, tab2 = st.tabs(["🚀 Generate Specs", "✨ Consolidate Specs"]) # Added icons

    with tab1:
        st.subheader("Generate Individual Specifications") # Use header for tab title
        st.markdown("Generate individual functional specifications for logical units defined in the source code configuration.")

        # Using a container for the button and spinner
        with st.container():
            if st.button("Generate Specs"): # Button text
                with st.spinner("Generating Functional Specs..."):
                    st.session_state['generated_spec_paths'] = [] # Clear previous results
                    job_id = get_job_run_id_persistent() # Get new job ID
                    # job_id = "job_" + str(hash(source_code_logical_units_path + str(os.urandom(16)))) # Placeholder job ID, add randomness
                    # logger.info(f"\n*****job_id generated...>>>"{job_id}****\n\n") # Use your logger

                    # config_data = load_config_from_yaml(source_code_logical_units_path)
                    if st.session_state.get('source_code_config') is not None:  
                        config_data = st.session_state.get('source_code_config')
                        # st.write("logical unit config_data is loaded")
                    else:
                        st.write("Upload Source code Logical units configuration file first in the previous step")
                        # return

                    if config_data:
                        st.session_state.source_code_config = config_data # Store YAML data in session state
                        # Use session state for base_dir if available from Upload menu
                        base_dir = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
                        # logger.info(f"config_data:>>>>"{config_data}) # Use your logger

                        # Check if config_data is a list of dictionaries
                        if not isinstance(config_data, list):
                             st.error("Source Code Config YAML must be a list of items.")
                             return

                        for item in config_data:
                            if not isinstance(item, dict):
                                st.error("Each item in the Source Code Config YAML must be a dictionary.")
                                return
                            if 'id' not in item or 'programs' not in item:
                                st.error("Each item in the Source Code Config YAML must contain 'id' and 'programs' keys.")
                                return
                            if not isinstance(item['programs'], list):
                                st.error("The value for 'programs' must be a list.")
                                return

                            record_id = item.get('id', 'unknown_id') # Use .get for safer access
                            programs_list = item.get('programs', [])
                            action_str = item.get('action', 'process') # Default action is 'process'

                            if action_str.lower() == "process": # Case-insensitive check
                                # Get the contexts
                                combined_code = ""
                                contexts = {}
                                context_keys = ['context_1', 'context_2', 'context_3']
                                for key in context_keys:
                                    context_value = item.get(key)
                                    if context_value:
                                        # Determine if context is a file path or direct content
                                        if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
                                            context_path_temp = base_dir / "context" / context_value
                                            context_content = read_program_from_path(str(context_path_temp))
                                            if context_content is not None:
                                                contexts[key] = context_content
                                            else:
                                                st.warning(f"Context file not found or readable for key '{key}': {context_path_temp}")
                                                # logger.warning(f"Context file not found or readable for key '{key}': {context_path_temp}") # Use your logger
                                        else:
                                            # Assume direct content
                                            contexts[key] = context_value
                                #     # else:
                                #         # logger.info(f"Key {[key]} is not used for record_id: {record_id}") # Use your logger

                                # # Read source code for the programs
                                # for program in programs_list:
                                #     program = program.strip()
                                #     source_code_path = base_dir / "source_code" / program
                                #     code = read_program_from_path(str(source_code_path))
                                #     if code:
                                #         combined_code += f"## Content of {program}\n```cobol\n{code}\n```\n\n"
                                #     else:
                                #          st.warning(f"Source code file not found or readable for program: {program}")
                                #          # logger.warning(f"Source code file not found or readable for program: {program}") # Use your logger

                                # # Generate spec if code was read
                                # if combined_code is empty, read programs from file
                                combined_code = combine_files_contents_from_csv(base_dir, programs_list)

                                if combined_code:
                                    with st.spinner(f"Generating Functional Specs for {programs_list}"):
                                        generate_functional_spec(source_code=combined_code, base_dir=base_dir,
                                                                job_id=job_id, record_id=record_id,
                                                                programs=programs_list, contexts=contexts)
                                else:
                                     st.warning(f"No source code found for record_id: {record_id}. Skipping spec generation.")
                                     # logger.warning(f"No source code found for record_id: {record_id}. Skipping spec generation.") # Use your logger

                            else:
                                # logger.info(f"id:{record_id} - is ignored due to action: {action_str}") # Use your logger
                                # TODO
                                st.info(f"Skipping generation for '{record_id}' as action is '{action_str}'.")

                        st.success("🎉 Functional Specifications generation process completed!") # Added party popper icon
                    else:
                        st.error("Failed to load Source Code Config YAML file.")

        st.markdown("---") # Separator
        # display_all_generated_specifications() # Display generated specs below the button

    with tab2:
        st.subheader("Consolidate Specifications") # Use header for tab title
        st.markdown("Consolidate generated functional specifications based on the consolidation configuration.")
        # Using a container for the button and spinner
        with st.container():
            if st.button("Consolidate Specs"): # Button text
                with st.spinner("Consolidating Functional Specs..."):
                    # Use session state for base_dir if available from Upload menu
                    base_dir = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
                    consolidated_fs_path = consolidate_functional_specs(
                        config_data=fs_config_data,
                        base_dir=base_dir
                    )
                    if consolidated_fs_path:
                         st.session_state.consolidated_fs_path = consolidated_fs_path
                         st.success("✅ Functional Specifications consolidated successfully!") # Added checkmark icon
                    else:
                         st.error("Failed to consolidate Functional Specifications.")


        st.markdown("---") # Separator

        # Display consolidated spec if available
        if 'consolidated_fs_path' in st.session_state and st.session_state['consolidated_fs_path']:
            # st.subheader("Consolidated Functional Specifications")
            # Ensure base_dir is a Path object for joining
            base_dir = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
            # Construct the full path using base_dir and the stored relative path/filename
            consolidated_fs_path_full = base_dir / "output" / Path(st.session_state.consolidated_fs_path).name
            # Check if the file exists before attempting to read
            if consolidated_fs_path_full.exists():
                consolidated_fs_content = read_program_from_path(str(consolidated_fs_path_full))
                if consolidated_fs_content:
                    # Display as code block for better formatting of markdown
                    st.markdown(consolidated_fs_content)
                    # Provide download link
                    download_link_html = create_download_link_with_icon(
                        consolidated_fs_content,
                        consolidated_fs_path_full.name,
                        "text/markdown",
                        icon="" # Added download icon
                    )
                    st.markdown(download_link_html, unsafe_allow_html=True)
                else:
                    st.info("Consolidated Functional Specifications content could not be read.")
            else:
                st.error(f"Consolidated Functional Specifications file not found at {consolidated_fs_path_full}")
        else:
            st.info("Generate and consolidate functional specifications to view them here.")


# --- Run the App ---
if __name__ == "__main__":
    # Ensure base_dir is initialized in session state if not already present
    if 'base_dir' not in st.session_state:
         st.session_state['base_dir'] = str(BASE_DIR_DEFAULT)
    # Ensure app_name is initialized in session state if not already present
    if 'app_name' not in st.session_state:
         st.session_state['app_name'] = None
    # Ensure generated_spec_paths is initialized
    if 'generated_spec_paths' not in st.session_state:
        st.session_state['generated_spec_paths'] = []
    if 'source_code_config' not in st.session_state:
        st.write("logical unit config is not available")
    app()
