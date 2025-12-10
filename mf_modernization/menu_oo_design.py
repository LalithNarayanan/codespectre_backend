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
import re


config = load_config()
logger = logger # Use your actual logger instance
agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
design_agent = agent_manager.get_agent("oo_designer")
mermaid_generator_agent=agent_manager.get_agent("mermaid_digram_generator")


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


def generate_oodesign_doc(input_file_path, base_dir):
    """Placeholder for generating OO Design document."""
    # logger.info(f"generate_oodesign_doc input_file_path:{input_file_path}") # Use your logger
    # st.info(f"Generation of Object Oriented Design from {input_file_path}...")
    try:
        # In a real scenario, you would use read_program from your utils
        # content = read_program(str(base_dir / "output"), Path(input_file_path).name)
        # Simulate reading content from the functional spec file
        content = read_program_from_path(str(Path(base_dir) / "output" / Path(input_file_path).name))
        if content is None:
             st.error("Could not read content from Functional Specification file.")
             return None
        oo_design = design_agent.execute(functional_spec=content)
        target_file_path = str(base_dir / "output" / "oo_design.md")
        save_to_file(target_file_path, oo_design.content)
        # st.success(f"Object Oriented Design Document is generated and saved with path:{target_file_path}")
        return target_file_path
    except FileNotFoundError:
        st.error(f"Functional Specification file not found: {input_file_path}")
        # logger.error(f"Functional Specification file not found: {input_file_path}") # Use your logger
        return None
    except Exception as e:
        st.error(f"Error generating Object Oriented Design: {e}")
        # logger.error(f"Error generating OO Design: {e}") # Use your logger
        return None

def render_mermaid_chart(mermaid_code):
    """Renders a Mermaid chart in a Streamlit app."""
    html_code = f"""
    <div class="mermaid" style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        {mermaid_code}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        setTimeout(function() {{
            mermaid.initialize({{startOnLoad:true}});
        }}, 200); // Delay of 200 milliseconds (adjust as needed)
    </script>
    """
    
    st.components.v1.html(html_code, height=3050, width=1500)

def generate_mermaid_diagram_content(file_name, base_dir):
    """Placeholder for generating Mermaid diagram content."""
    # st.info(f"Generating Class diagram generation from {file_name}...")
    try:
        content = read_program_from_path(str(Path(base_dir) / "output" / Path(file_name).name))
        if content is None:
             st.error("Could not read content from OO Design file for diagram generation.")
             return None

        mermaid_digram = mermaid_generator_agent.execute(diagram_type="class_diagram",data_for_diagram=content)
        logger.info(f"mermaid_digram:{mermaid_digram}") # Use your logger

        mermaid_content=mermaid_digram.content
        
        mermaid_content = re.sub(r"^```mermaid\s*\n?", "", mermaid_content, flags=re.IGNORECASE)
        mermaid_content = re.sub(r"\n?\s*```\s*$", "", mermaid_content, flags=re.IGNORECASE)
        mermaid_content = mermaid_content.strip()
        # mermaid_diagram_code=mermaid_content
        # Simulate agent output (example class diagram code)
        mermaid_diagram_code1 = """classDiagram
            class LTCHBill {
                -billData : BILL-REC
                +validate()
                +prepareCalculation()
                +getPaymentAmount()
            }

            class Provider {
                -providerData : PROV-RECORD-FROM-USER
                +loadProviderDataFromFile()
                +getRate()
                +getRatio()
            }

            class PaymentCalculator {
                -ltchBill : LTCHBill
                -provider : Provider
                +calculatePayment(LTCHBill)
            }

            LTCHBill "1" -- "1" PaymentCalculator : used by
            Provider "1" -- "1" PaymentCalculator : used by
            """


        mermaid_diagram_code = """  
        classDiagram
    class MedicarePaymentCalculator {
        -fiscalYearStrategy : FiscalYearStrategy
        -providerTypeStrategy : ProviderTypeStrategy
        -drgTableManager : DRGTableManager
        -wageIndexManager : WageIndexManager
        +calculatePayment(billRecord : BillRecord) : PaymentSummary
    }

    class BillRecord {
        -attributes : ... // From BILL-NEW-DATA
    }

    class PaymentSummary {
        -attributes : ... // From PPS-DATA-ALL and PPS-PAYMENT-DATA
    }

    class DRGTableManager {
        -drgTables : DRGTable[]
        +getDRGData(drgCode : String, fiscalYear : int) : DRGData
    }

    class DRGTable {
        -fiscalYear : int
        -drgData : ...
        +lookupDRG(drgCode : String) : DRGData
    }

    class WageIndexManager {
        -wageIndexTables : WageIndexTable[]
        +getWageIndex(location : String, date : Date, providerType : String) : double
    }

    class WageIndexTable {
        -indexType : String
        -year : int
        -indexData : ...
    }

    class RuralFloorFactorTable {
        -data : ... //From RUFL200
    }

    class PaymentCalculationStrategy {
        +calculatePayment(billRecord : BillRecord, drgData : DRGData, wageIndex : double) : double
    }

    class LTCAL032Strategy extends PaymentCalculationStrategy {
        +calculatePayment(billRecord : BillRecord, drgData : DRGData, wageIndex : double) : double
    }

    class LTCAL162Strategy extends PaymentCalculationStrategy {
        +calculatePayment(billRecord : BillRecord, drgData : DRGData, wageIndex : double) : double
    }

    class FiscalYearStrategy {
        +getPaymentCalculationStrategy(fiscalYear : int) : PaymentCalculationStrategy
    }

    class ProviderTypeStrategy {
        +getPaymentCalculationStrategy(providerType : String) : PaymentCalculationStrategy
    }

    class DRGData {
        -weight : double
        -otherAttributes : ...
    }

    MedicarePaymentCalculator -- BillRecord : uses
    MedicarePaymentCalculator -- PaymentSummary : creates
    MedicarePaymentCalculator -- FiscalYearStrategy : uses
    MedicarePaymentCalculator -- ProviderTypeStrategy : uses
    MedicarePaymentCalculator -- DRGTableManager : uses
    MedicarePaymentCalculator -- WageIndexManager : uses

    DRGTableManager -- DRGTable : manages

    WageIndexManager -- WageIndexTable : manages

    FiscalYearStrategy .. PaymentCalculationStrategy : creates
    ProviderTypeStrategy .. PaymentCalculationStrategy : creates

    PaymentCalculationStrategy <|-- LTCAL032Strategy
    PaymentCalculationStrategy <|-- LTCAL162Strategy

    MedicarePaymentCalculator .. DRGData : uses
    MedicarePaymentCalculator .. Date : uses // Assuming 'Date' is a standard type

    PaymentCalculationStrategy .. BillRecord : uses
    PaymentCalculationStrategy .. DRGData : uses"""

        target_file_path = str(base_dir / "output" / "mermaid_diagram.md")
        save_to_file(target_file_path, mermaid_diagram_code)
        # st.success(f"OO class diagram generated and saved to: {target_file_path}")
        # logger.info(f"mermaid_path:>{target_file_path}") # Use your logger
        return target_file_path
    except FileNotFoundError:
        st.error(f"OO Design file not found: {file_name}")
        # logger.error(f"OO Design file not found: {file_name}") # Use your logger
        return None
    except Exception as e:
        st.error(f"Error generating Class Diagram: {e}")
        # logger.error(f"Error generating Class Diagram: {e}") # Use your logger
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
    css_path = os.path.join(os.path.dirname(__file__), 'design.css')
    with open(css_path) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True) 

    st.markdown("""
    <style>
    /* Font - Using a common sans-serif font similar to TCS */
    html, body, [class*="css"] {
        font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    }

    /* Header Styling */
    .css-18e3th9 { /* Target the main content div */
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 5%; /* Add some padding */
        padding-right: 5%;
    }

    /* Sidebar Styling (Optional - requires more specific selectors) */
    .css-1lcbmhc, .css-1lcbmhc > div > section { /* Target sidebar */
        background-color: #f8f8f8; /* Light grey background */
        color: #333; /* Darker text */
    }

    /* Button Styling (Inspired by TCS button styles) */
    .stButton>button {
        background-color: #005696; /* TCS Blue */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1em;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #003d6b; /* Darker blue on hover */
        color: white;
    }

    /* Input Field Styling */
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }

     /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #e0f2f7; /* Light blue header */
        color: #005696; /* TCS Blue text */
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }

    /* Success/Error/Info Message Styling */
    .stAlert {
        border-radius: 5px;
    }

    /* Add more specific styling as needed */

    </style>
    """, unsafe_allow_html=True)

    # Link Material Symbols font
    st.markdown("""
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    """, unsafe_allow_html=True)


    # --- Header Section ---
    st.subheader("📐 Object Oriented Design & Diagrams") # Added ruler/design icon

    st.markdown("""
    Generate Object-Oriented Design documents and visual class diagrams from the consolidated functional specifications.
    """)

    # --- Input Fields ---
    st.subheader("📄 Input Specifications") # Added document icon

    # Using columns for better layout of input fields
    col1, col2 = st.columns(2)

    with col1:
        app_name = st.text_input("Application Name:", value=st.session_state.get('app_name', app_name_default), disabled=True)
        # Use session state for default value if available from Functional Specs menu
        functional_specs_path_default = st.session_state.get('consolidated_fs_path', "consolidated_FunctionalSpecification.md")
        functional_specs_path = st.text_input("Consolidated Functional Specifications(from previous step):", value=functional_specs_path_default, disabled=True, help="This should be the output file from the 'Consolidate Specs' step in the Functional Specifications menu.") # Disabled as it's an output from another step

    with col2:
         # Context path input (if still needed for OO design generation)
        context_path = st.text_input("Context File (Optional, .md file):", help="Provide an optional context file to influence the OO design generation.")


    st.markdown("---") # Separator

    # --- OO Design Generation ---
    st.subheader("📝 Generate Object Oriented Design Document") # Added document icon

    # Using a container for the button and spinner
    with st.container():
        if st.button("Generate Object Oriented Design"): # Button text
            if 'consolidated_fs_path' in st.session_state:
                # logger.info(f"consolidated_fs_path:{st.session_state.consolidated_fs_path}") # Use your logger
                with st.spinner("Generating OO Design..."):
                    # Get the filename from the stored consolidated_fs_path
                    fs_filename = Path(st.session_state.consolidated_fs_path).name
                    # Use session state for base_dir if available from Upload menu
                    base_dir_temp = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
                    # logger.info(f"name:{fs_filename}") # Use your logger
                    # logger.info(f"base_dir_temp:{base_dir_temp}") # Use your logger

                    oo_design_path = generate_oodesign_doc(fs_filename, base_dir_temp)

                    if oo_design_path:
                        st.session_state.generated_oo_design_path = oo_design_path
                        st.success("✅ Object Oriented Design generated!") # Added checkmark icon
                    else:
                        st.error("Failed to generate OO Design.")
            else:
                st.error("Please generate Functional Specifications first in the 'Functional Specification' menu.")

    # Display generated OO Design if available
    if 'generated_oo_design_path' in st.session_state:
        st.subheader("📖 Object Oriented Design Document") # Added book icon
        # Use session state for base_dir if available from Upload menu
        base_dir_temp = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
        # Construct the full path
        oo_design_path_full = base_dir_temp / "output" / Path(st.session_state.generated_oo_design_path).name

        # Check if the file exists before attempting to read
        if oo_design_path_full.exists():
            oo_design_content = read_program_from_path(str(oo_design_path_full))
            if oo_design_content:
                # Display as code block for better formatting of markdown
                st.markdown(oo_design_content)
                # Provide download link
                download_link_html = create_download_link_with_icon(
                    oo_design_content,
                    oo_design_path_full.name,
                    "text/markdown",
                    icon="download" # Added download icon
                )
                st.markdown(download_link_html, unsafe_allow_html=True)
            else:
                st.info("OO Design document content could not be read.")
        else:
            st.error(f"OO Design document file not found at {oo_design_path_full}")
    else:
        st.info("Generate OO Design to view it here.")

    st.markdown("---") # Separator

    # --- Class Diagram Generation ---
    st.subheader("📊 Generate Class Diagram") # Added chart icon

    # Using a container for the button and spinner
    with st.container():
        if st.button("Generate Class Diagram"): # Button text
            if 'generated_oo_design_path' in st.session_state:
                with st.spinner("Generating Class Diagram..."):
                    # Get the filename from the stored generated_oo_design_path
                    oo_design_filename = Path(st.session_state.generated_oo_design_path).name
                     # Use session state for base_dir if available from Upload menu
                    base_dir_temp = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
                    # logger.info(f"mermaid_path:>{mermaid_path}") # Use your logger

                    mermaid_path = generate_mermaid_diagram_content(oo_design_filename, base_dir_temp)

                    if mermaid_path:
                        st.session_state.generated_mermaid_diagram_path = mermaid_path
                        st.success("✅ Class Diagram Script generated!") # Added checkmark icon
                    else:
                        st.error("Failed to generate Class Diagram.")
            else:
                st.error("Please generate OO Design first.")

    # Display generated Class Diagram if available
    if 'generated_mermaid_diagram_path' in st.session_state:
        # logger.info(f"generated_mermaid_diagram_path:{st.session_state['generated_mermaid_diagram_path']}") # Use your logger
        st.subheader("📈 Class Diagram Visualization") # Added chart icon

        # Use session state for base_dir if available from Upload menu
        base_dir_temp = Path(st.session_state.get('base_dir', str(BASE_DIR_DEFAULT)))
         # Construct the full path
        mermaid_diagram_path_full = base_dir_temp / "output" / Path(st.session_state.generated_mermaid_diagram_path).name

        # Check if the file exists before attempting to read
        if mermaid_diagram_path_full.exists():
             mermaid_diagram_content = read_program_from_path(str(mermaid_diagram_path_full))
             if mermaid_diagram_content:
                 # Render the Mermaid chart
                 render_mermaid_chart(mermaid_diagram_content)
                 # Display the Mermaid code for reference
                 st.subheader("Mermaid Code")
                 st.code(mermaid_diagram_content, language="text") # Use text language for mermaid syntax
                 # Provide download link
                 download_link_html = create_download_link_with_icon(
                     mermaid_diagram_content,
                     mermaid_diagram_path_full.name,
                     "text/markdown", # Or text/plain
                     icon="download" # Added download icon
                 )
                 st.markdown(download_link_html, unsafe_allow_html=True)
             else:
                 st.info("Class Diagram content could not be read.")
        else:
             st.error(f"Class Diagram file not found at {mermaid_diagram_path_full}")
    else:
        st.info("Generate Class Diagram to view it here.")


# --- Run the App ---
if __name__ == "__main__":
    # Ensure base_dir is initialized in session state if not already present
    if 'base_dir' not in st.session_state:
         st.session_state['base_dir'] = str(BASE_DIR_DEFAULT)
    # Ensure app_name is initialized in session state if not already present
    if 'app_name' not in st.session_state:
         st.session_state['app_name'] = app_name_default

    app()
