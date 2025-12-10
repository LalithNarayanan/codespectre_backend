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

config = load_config()
logger = logger # Use your actual logger instance
agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
fs_agent = agent_manager.get_agent("generate_functional_spec")
base_dir=config['source_path']['base_dir_default']

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


def generate_functional_spec(source_code, section_type,filename_only):
    """Placeholder for generating functional specifications."""
    functional_spec_content = fs_agent.execute(
                                       code=source_code,
                                       section_type=section_type)
    
    print(f"base_dir: {base_dir}")
    target_file_path = str(Path(base_dir) / "output" / f"{filename_only}_{section_type}_FunctionalSpecification.md")
    save_to_file(target_file_path, functional_spec_content)
    view_file_in_expander_with_download(target_file_path) 
    return target_file_path


#Generate functional specs
# def generate_functional_spec(source_code, base_dir, job_id, record_id, programs, contexts=None):
#     """Placeholder for generating functional specifications."""
#     # st.info(f"Generation for {record_id}...")
#     # Replace with your actual agent execution logic
#     functional_spec_content = fs_agent.execute(job_id=job_id, record_id=record_id,
#                                        base_dir=base_dir, code=source_code,
#                                        programs=programs, contexts=contexts)

#     target_file_path = str(Path(base_dir) / "output" / f"{record_id}_FunctionalSpecification.md")
#     save_to_file(target_file_path, functional_spec_content)
#     #TODO
#     # st.success(f"Job Id:{job_id}, \n Functional Specifications generated for {record_id}. Programs: {programs} and saved to: {target_file_path}")
#     # logger.info(f"\n********* {job_id}_{record_id} is saved at {target_file_path}  **************") # Use your logger

#     view_file_in_expander_with_download(target_file_path)  # Call the function to display in expander

#     if 'generated_spec_paths' not in st.session_state:
#         st.session_state['generated_spec_paths'] = []
#     st.session_state['generated_spec_paths'].append(target_file_path)

#     return target_file_path

# #Consolidate functional specs
# def consolidate_functional_specs(config_data, base_dir, merged_fs_file_name="consolidated_FunctionalSpecification.md"):
#     """Placeholder for consolidating functional specifications."""
#     # st.info("Consolidation...")
#     target_file_path = str(Path(base_dir) / "output" / merged_fs_file_name)

#     if not config_data:
#         return None

#     # Basic validation of config_data structure
#     if not isinstance(config_data, dict):
#         st.error("FS Consolidation Config YAML must be a dictionary.")
#         return None
#     if 'functional_specificiations' not in config_data or 'sections' not in config_data:
#         st.error("FS Consolidation Config YAML must contain 'functional_specificiations' and 'sections' keys.")
#         return None
#     if not isinstance(config_data['functional_specificiations'], list) or not isinstance(config_data['sections'], list):
#          st.error("'functional_specificiations' and 'sections' in FS Consolidation Config YAML must be lists.")
#          return None

#     combined_functional_spec = ""
#     functional_specs = config_data.get('functional_specificiations', [])
#     sections = config_data.get('sections', [])
#     action_str = config_data.get('action', 'process') # Default action is 'process'

#     if action_str.lower() == "process": # Case-insensitive check
#         # Get the contexts
#         contexts = {}
#         context_keys = ['context_1', 'context_2', 'context_3']
#         for key in context_keys:
#             context_value = config_data.get(key)
#             if context_value:
#                 # Determine if context is a file path or direct content
#                 if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
#                     context_path_temp = base_dir / "context" / context_value
#                     context_content = read_program_from_path(str(context_path_temp))
#                     if context_content is not None:
#                          contexts[key] = context_content
#                     else:
#                          st.warning(f"Context file not found or readable for key '{key}': {context_path_temp}")
#                          # logger.warning(f"Context file not found or readable for key '{key}': {context_path_temp}") # Use your logger
#                 else:
#                     # Assume direct content
#                     contexts[key] = context_value

#         combined_functional_spec = "# Consolidated Functional Specification\n\n"
#         for section in sections:
#             # logger.info(f"section:>>>{section}") # Use your logger
#             combined_match = ""
#             for spec in functional_specs:
#                 spec = spec.strip()
#                 # logger.info(f"spec=>>>>>>>>>>>>>>{spec}") # Use your logger
#                 fs_path = str(base_dir / "output" / spec)
#                 # logger.info(f"fs_path:>>>{fs_path}") # Use your logger
#                 fs_content = read_program_from_path(fs_path)
#                 if fs_content is None:
#                     continue # Skip if file not found or readable

#                 section_to_search = re.escape(section.strip())  # Escape special chars and remove extra spaces
#                 # Adjusted pattern to be more robust
#                 pattern = rf"^#\s+{section_to_search}\s*\n(.*?)(?:^#\s+|\Z)"
#                 # pattern = r"^#\s+Program Overview\s*\n(.*?)(?:^#\s+|\Z)" # Original pattern

#                 # logger.info(f"spec=>>>>>>>>>>>>>>{spec}-{pattern}") # Use your logger
#                 match = re.search(pattern, fs_content, re.MULTILINE | re.DOTALL)
#                 if match:
#                     # logger.info("EXACT MATCH FOUND") # Use your logger
#                     match_content = match.group(1).strip()
#                     # logger.info(f"\n\n\n******************\match:>>>{match_content} ******************end of match\n\n") # Use your logger
#                     if match_content:
#                         combined_match += f"**Content of '{section.strip()}' from '{spec}'**\n\n {match_content}\n\n---\n\n" # Added separator


#             if combined_match:
#                 # Simulate agent execution for consolidation at section level
#                 combined_functional_spec_sectionlevel= fs_consolidate_agent.execute(job_id="job_id",
#                                                                                     base_dir=base_dir,
#                                                                                     section=section,
#                                                                                     functional_specs=combined_match,
#                                                                                     contexts=contexts
#                                                                                     )

#                 combined_functional_spec += combined_functional_spec_sectionlevel.content + "\n \n"

#         # logger.info(f"All sections are created.") # Use your logger
#         save_to_file(target_file_path, combined_functional_spec)
#         # logger.info(f"\n********* {job_id}_{section} is saved at {target_file_path}  **************") # Use your logger

#     else:
#         # logger.info(f"Consolidation is ignored due to action: {action_str}") # Use your logger
#         st.info(f"Skipping consolidation as action is '{action_str}'.")
#         return None
#     #TODO
#     # st.success(f"Consolidated Functional Specifications saved to: {target_file_path}")

#     return target_file_path

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


# def display_all_generated_specifications():
#     """Displays all generated functional specifications available in session state."""
#     if 'generated_spec_paths' in st.session_state and st.session_state['generated_spec_paths']:
#         st.subheader("Generated Functional Specifications:")
#         # Display in reverse order to show latest first
#         for file_path in reversed(st.session_state['generated_spec_paths']):
#             view_file_in_expander_with_download(file_path)
#     else:
#         st.info("No functional specifications have been generated yet.")

# --- Streamlit App Layout ---

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
    

def app():
    # --- Header Section ---
    st.subheader("📝 Functional Specifications") # Added document icon
    st.markdown("""
    Generate Functional Specifications and consolidate them based on the configurations.
    """)
    source_code_path_default="C:\\SeenuWS\\CodeSpectre\\java_modernization\\JavaSpringApplications"
    # --- Input Fields ---
    st.subheader("📁 Configuration Files") # Added folder icon
    source_code_path = st.text_input("Source Code Path:", value=source_code_path_default, help="Path Java Spring Application") # Added help text and icon idea
    
    # --- Tabs for Functionality ---
    tab1, tab2 = st.tabs(["🚀 Generate Specs", "✨ Consolidate Specs"]) # Added icons

    with tab1:
        st.subheader("Generate Individual Specifications") # Use header for tab title
        st.markdown("Generate individual functional specifications for logical units defined in the source code configuration.")

        # Using a container for the button and spinner
        with st.container():
            if st.button("Generate Specs"): # Button text
        # with st.spinner("Generating Functional Specs..."):
                # Generate spec if code was read
                if source_code_path_default:
                    section_type="extract_program_overview"
                    folder_path=r"C:\SeenuWS\CodeSpectre\java_modernization\code_extractor\controller_wise_code_snippets"
                    file_list=read_files_in_directory(folder_path)
                    no_files=1
                    for filename in file_list:
                        # if no_files>1:
                        #     break
                        file_path = os.path.join(folder_path, filename)
                        filename_only, _ = os.path.splitext(filename)
                        # Check if it's a file (not a subdirectory)
                        st.success(f"🎉 {no_files} of {len(file_list)} {filename}")
                        no_files+=1
                        with st.spinner(f"Generating Functional Specs for {filename}"):
                            if os.path.isfile(file_path):
                                print(f"--- Reading content of: {filename} ---")
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                        print(f"read file...")
                                        # print(content)
                                        generate_functional_spec(source_code=content,section_type=section_type,filename_only=filename_only)
                                    print(f"--- End of {filename} ---\n")
                                except Exception as e:
                                    print(f"Error reading file {filename}: {e}\n")
                        # st.success(f"🎉 Functional Specifications generation for {filename} process completed!") # Added party popper icon
                        # st.success("🎉 Functional Specifications generation process completed!") # Added party popper icon
           

        st.markdown("---") # Separator
        # display_all_generated_specifications() # Display generated specs below the button

    # with tab2:
    #     st.subheader("Consolidate Specifications") # Use header for tab title
    #     st.markdown("Consolidate generated functional specifications based on the consolidation configuration.")
    #     # Using a container for the button and spinner
    #     with st.container():
    #         if st.button("Consolidate Specs"): # Button text
    #             with st.spinner("Consolidating Functional Specs..."):
    #                 # Use session state for base_dir if available from Upload menu
    #                 base_dir = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
    #                 consolidated_fs_path = consolidate_functional_specs(
    #                     config_data=fs_config_data,
    #                     base_dir=base_dir
    #                 )
    #                 if consolidated_fs_path:
    #                      st.session_state.consolidated_fs_path = consolidated_fs_path
    #                      st.success("✅ Functional Specifications consolidated successfully!") # Added checkmark icon
    #                 else:
    #                      st.error("Failed to consolidate Functional Specifications.")


    #     st.markdown("---") # Separator

        # # Display consolidated spec if available
        # if 'consolidated_fs_path' in st.session_state and st.session_state['consolidated_fs_path']:
        #     # st.subheader("Consolidated Functional Specifications")
        #     # Ensure base_dir is a Path object for joining
        #     base_dir = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
        #     # Construct the full path using base_dir and the stored relative path/filename
        #     consolidated_fs_path_full = base_dir / "output" / Path(st.session_state.consolidated_fs_path).name
        #     # Check if the file exists before attempting to read
        #     if consolidated_fs_path_full.exists():
        #         consolidated_fs_content = read_program_from_path(str(consolidated_fs_path_full))
        #         if consolidated_fs_content:
        #             # Display as code block for better formatting of markdown
        #             st.markdown(consolidated_fs_content)
        #             # Provide download link
        #             download_link_html = create_download_link_with_icon(
        #                 consolidated_fs_content,
        #                 consolidated_fs_path_full.name,
        #                 "text/markdown",
        #                 icon="" # Added download icon
        #             )
        #             st.markdown(download_link_html, unsafe_allow_html=True)
        #         else:
        #             st.info("Consolidated Functional Specifications content could not be read.")
        #     else:
        #         st.error(f"Consolidated Functional Specifications file not found at {consolidated_fs_path_full}")
        # else:
        #     st.info("Generate and consolidate functional specifications to view them here.")


# --- Run the App ---
if __name__ == "__main__":
    # Ensure base_dir is initialized in session state if not already present
    # if 'base_dir' not in st.session_state:
    #      st.session_state['base_dir'] = str(BASE_DIR_DEFAULT)
    # Ensure app_name is initialized in session state if not already present
    if 'app_name' not in st.session_state:
         st.session_state['app_name'] = None
    # Ensure generated_spec_paths is initialized
    if 'generated_spec_paths' not in st.session_state:
        st.session_state['generated_spec_paths'] = []
    if 'source_code_config' not in st.session_state:
        st.write("logical unit config is not available")
    app()
