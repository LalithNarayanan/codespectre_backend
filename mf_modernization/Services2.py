
# import os
# from pathlib import Path

# from fastapi import Form
# from config import load_config
# from agents.functional_spec_generator_agent import FunctionalSpecGeneratorAgent
# from agents.functional_spec_consolidator_agent import FunctionalSpecsConsolidatorAgent
# from pathlib import Path
# import re
# from agents import ReverseEngineeringAgentManager
# from sampleServices2 import md_string_to_pdf
# from utils.job_util import get_job_run_id_persistent, load_job_run_state
# import yaml
# import markdown
# from utils.logger import logger

# from utils.file_util import save_to_file

# from utils.yaml_to_md import yaml_to_markdown

# agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
# fs_agent = agent_manager.get_agent("generate_functional_spec")
# fs_consolidate_agent = agent_manager.get_agent("consolidate_functional_specs")
# design_agent = agent_manager.get_agent("oo_designer")
# mermaid_generator_agent=agent_manager.get_agent("mermaid_digram_generator")



# config = load_config()

# def read_program_from_path(filepath):
#     """Reads content from a file."""
#     with open(filepath, "r") as f: # Specify encoding
#         return f.read()
    
# import re

# def extract_paragraphs_from_cobol(source_code):
#     """
#     Returns {paragraph_name: code_snippet} for a COBOL file.
#     """
#     # Regex: Paragraphs start with label ending with '.' at line start.
#     pattern = re.compile(
#         r'(?m)^\s*\d*\s*([A-Z0-9\-]+)\.\s*(.*?)(?=^\s*\d*\s*[A-Z0-9\-]+\.\s*|\Z)', 
#         re.DOTALL | re.MULTILINE
#     )    
#     return {m.group(1): m.group(2).strip() for m in pattern.finditer(source_code)}

# def func_spec(application_name, logical_unit, platform: str = Form(...)):
#     program_type = f"{platform}_programs"

#     job_id = get_job_run_id_persistent()
#     combined_code_path = r"C:\Users\YendetiLalith\Documents\CodeSpectre\mf_modernization\sas_combined.txt"
#     # combined_code_path = r"C:\Users\YendetiLalith\Documents\CodeSpectre\mf_modernization\pyspark_combined.txt"
    
#     config_data = logical_unit
#     results = []
#     specs = {}
#     pdf_file = None
    
#     print(f"DEBUG: Processing {len(config_data)} items from config")  # ← ADD
    
#     for item in config_data:
#         record_id = item.get('id', 'unknown_id')
#         programs_list = item.get('programs', [])
#         action_str = item.get('action', 'process')
        
#         print(f"DEBUG: Processing record_id={record_id}, action={action_str}, programs={len(programs_list)}")  # ← ADD
        
#         if action_str.lower() == "process":
#             combined_code = ""
#             contexts = {}
#             context_keys = ['context_1', 'context_2', 'context_3']
            
#             # Load contexts
#             for key in context_keys:
#                 context_value = item.get(key)
#                 if context_value:
#                     if isinstance(context_value, str) and (
#                         context_value.lower().endswith('.md') or 
#                         context_value.lower().endswith('.csv')
#                     ):
#                         context_path = Path(config['source_path']['base_dir_default']) / "context" / context_value
#                         print(f"DEBUG: Loading context {key} from {context_path}")  # ← ADD
                        
#                         if context_path.exists():
#                             context_content = read_program_from_path(str(context_path))
#                             if context_content is not None:
#                                 contexts[key] = context_content
#                                 print(f"DEBUG: Loaded {key}, size={len(context_content)}")  # ← ADD
#                             else:
#                                 print(f"WARNING: Failed to read {key}: {context_path}")
#                         else:
#                             print(f"WARNING: Context file not found: {context_path}")
#                     else:
#                         contexts[key] = context_value

#             # Load program files
#             print(f"DEBUG: Loading {len(programs_list)} programs")  # ← ADD
            
#             for program in programs_list:
#                 program = program.strip()
                
#                 # Skip data files
#                 if program.lower().endswith(('.csv', '.txt', '.dat')):
#                     print(f"DEBUG: Skipping data file: {program}")  # ← ADD
#                     continue
                
#                 source_code_path = Path(config['source_path']['base_dir_default']) / "source_code" / program
#                 print(f"DEBUG: Looking for program at: {source_code_path}")  # ← ADD
                
#                 if not source_code_path.exists():
#                     print(f"ERROR: File not found: {source_code_path}")  # ← ADD
#                     results.append(f"File not found: {source_code_path}")
                    
#                 else:
#                     try:
#                         with open(source_code_path, "r", encoding="utf-8", errors='ignore') as f: 
#                             code = f.read()

#                         if code:
#                             combined_code += f"## Content of {program}\n```sas\n{code}```\n\n"
#                             # combined_code += f"## Content of {program}\n```pyspark\n{code}```\n\n"
#                             with open(combined_code_path, "a") as file:
#                                 file.write(combined_code)
#                             print(f"DEBUG: Added {program}, code length={len(code)}")  # ← ADD
#                         else:
#                             print(f"WARNING: Empty file: {program}")  # ← ADD
                
#                     except Exception as e:
#                         print(f"ERROR: Failed to read {program}: {e}")  # ← ADD
#                         results.append(f"Error reading {program}: {str(e)}")
            
#                 print(f"DEBUG: combined_code length = {len(combined_code)}")  # ← ADD
            
#                 if combined_code:
#                     try:
#                         print(f"DEBUG: Calling fs_agent.execute for {record_id}")  # ← ADD

#                         output = fs_agent.execute(
#                             job_id=job_id,
#                             record_id=record_id,
#                             base_dir=".",
#                             code=combined_code,
#                             contexts=contexts,
#                             programs=programs_list
#                         )

#                         print(f"DEBUG: Agent output length = {len(output) if output else 0}")  # ← ADD

#                         # Save markdown
#                         md_filename = f"{record_id}_FunctionalSpecification.md"
#                         md_dir = Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications"
#                         # md_dir = Path(config['source_path']['base_dir_default']) / "output" / "pyspark_specifications"
#                         md_dir.mkdir(parents=True, exist_ok=True)
#                         md_path = md_dir / md_filename

#                         print(f"DEBUG: Saving markdown to {md_path}")  # ← ADD
#                         save_to_file(str(md_path), output)

#                         # ---- Call validation agent automatically after spec generation ----
#                         # try:
#                         #     validation_agent = agent_manager.get_agent("validation_agent")
#                         #     print(f"DEBUG: Invoking validation agent for record_id={record_id}")
#                         #     validation_resp = validation_agent.execute(
#                         #         job_id=job_id,
#                         #         record_id=record_id,
#                         #         base_dir=".",
#                         #         source_code=combined_code,
#                         #         functional_spec=output,
#                         #     )
#                         #     print(f"DEBUG: Validation completed for {record_id}")
#                         # except Exception as ve:
#                         #     # Log but don't fail the whole generation process
#                         #     print(f"WARNING: Validation failed for {record_id}: {ve}")
#                         #     results.append(f"Validation failed for {record_id}: {ve}")
#                         # ------------------------------------------------------------------

#                         # Generate PDF
#                         pdf_title = f"{record_id} - SAS Functional Specifications"
#                         # pdf_title = f"{record_id} - PYSPARK Functional Specifications"
#                         pdf_file_name = f"{record_id}_FunctionalSpecification.pdf"

#                         print(f"DEBUG: Generating PDF: {pdf_file_name}")  # ← ADD
#                         pdf_file = md_string_to_pdf(output, pdf_file_name, title=pdf_title)

#                         print(f"DEBUG: PDF generated: {pdf_file}")  # ← ADD

#                     except Exception as e:
#                         error_msg = f"Error generating spec for {record_id}: {str(e)}"
#                         print(f"ERROR: {error_msg}")  # ← ADD
#                         results.append(error_msg)
#                         raise ValueError(error_msg)
#                 else:
#                     print(f"WARNING: combined_code is empty for {record_id}")  # ← ADD
#         else:
#             print(f"DEBUG: Skipping {record_id}, action={action_str}")  # ← ADD
#             results.append(f"Skipping '{record_id}' as action is '{action_str}'.")
    
#     print(f"DEBUG: Final pdf_file = {pdf_file}")  # ← ADD
#     # results.append("SAS Functional Specifications generation completed!")
#     results.append("SAS Functional Specifications generation completed!")
    
#     if pdf_file is None:
#         raise ValueError(
#             "No PDF file was generated. Check logs above for errors."
#         )
    
#     return pdf_file



    
# # def func_spec(application_name,logical_unit):

# #     job_id = get_job_run_id_persistent()
# #     combined_code_path = r"C:\Users\YendetiLalith\Documents\CodeSpectre\mf_modernization\example.txt"
# #     config_data = None

# #     config_data = logical_unit
        
# #     results = []
# #     specs={}

# #     for item in config_data:
        
# #         record_id = item.get('id', 'unknown_id') 
# #         programs_list = item.get('programs', [])
# #         action_str = item.get('action', 'process')
        
# #         if action_str.lower() == "process":
# #             combined_code = ""
# #             contexts = {}
# #             context_keys = ['context_1', 'context_2', 'context_3']
# #             for key in context_keys:
# #                 context_value = item.get(key)
# #                 if context_value:
# #                     if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
# #                         context_path_temp = "C:/Users/YendetiLalith/Documents/CodeSpectre/MainframeApplications/LTCHPPSPricerMFApp2021"+ "/" +"context" +"/"+ context_value
# #                         context_content = read_program_from_path(context_path_temp)
# #                         if context_content is not None:
# #                             contexts[key] = context_content
# #                         else:
# #                             print(f"Context file not found or readable for key '{key}': {context_path_temp}")
# #                     else:
# #                         contexts[key] = context_value

# #             for program in programs_list:
# #                 program = program.strip()
# #                 code=None
# #                 source_code_path = config['source_path']['base_dir_default'] + "/" +"source_code" + "/" + program
# #                 if not Path(source_code_path).exists():
# #                     results.append(f"File not found: {source_code_path}")
# #                 else:
# #                     with open(source_code_path, "r",encoding="utf-8", errors='ignore') as f: 
# #                         source_code_content= f.read()
# #                         code = source_code_content
# #                     if code:
# #                         combined_code += f"## Content of {program}\n```cobol\n{code}\n```\n\n"
# #                         with open(combined_code_path, "a") as file:
# #                             file.write(combined_code)
# #                     else:
# #                         results.append(f"Source code file not found or readable for program: {program}")
# #                 if combined_code:
# #                     try:
# #                         output =  fs_agent.execute(
# #                                             job_id = job_id,
# #                                             record_id = record_id,
# #                                             base_dir = ".",
# #                                             code = combined_code,
# #                                             contexts = contexts,
# #                                             programs = programs_list
# #                                         )
# #                         # output_yaml =  fs_agent.execute(
# #                         #                     job_id = job_id,
# #                         #                     record_id = record_id,
# #                         #                     base_dir = ".",
# #                         #                     code = combined_code,
# #                         #                     contexts = contexts,
# #                         #                     programs = programs_list
# #                         #                 )
                        
# #                         # markdown_content = yaml_to_markdown(output_yaml, include_code=True)        # For interactive Markdown file
# #                         # markdown_content_for_pdf = yaml_to_markdown(output_yaml, include_code=False) # For PDF without code if desired

# #                         # final_md = output.strip() + '\n\n' + markdown_content.strip()
# #                         # final_md_pdf = output.strip() + '\n\n' + markdown_content_for_pdf.strip()


# #                         fspec={f"new{record_id}_FunctionalSpecification.md" : output}
# #                         specs["functional_specifications"] = fspec

# #                         md_filename = f"{record_id}_FunctionalSpecification.md"
# #                         #md_dir = Path(config['source_path']['base_dir_default']) / "output" / "generated_output_for_reference"
# #                         md_dir = Path("C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs")
# #                         md_dir.mkdir(parents=True, exist_ok=True)
# #                         md_path = md_dir / md_filename
# #                         save_to_file(str(md_path), output)

# #                         pdf_title = f"{record_id} - Functional Specifications"
# #                         pdf_file_name =f"{record_id}_FunctionalSpecification.pdf"
# #                         pdf_file = md_string_to_pdf(output, pdf_file_name, title=pdf_title)

# #                     except Exception as e:
# #                         print(str(e))                 
# #         else:
# #             results.append(f"Skipping generation for '{record_id}' as action is '{action_str}'.")
# #     results.append("Functional Specifications generation process completed!")
# #     return pdf_file                                      



# import os
# import re

# def extract_cobol_paragraphs_from_text(cobol_text):
#     in_procedure = False
#     paragraphs = []
#     paragraph_pattern = re.compile(r'^\s*\d{0,6}\s+([A-Za-z0-9\-]+)\.\s*$', re.MULTILINE)
#     for line in cobol_text.splitlines():
#         line_strip = line.strip()
#         line_upper = line_strip.upper()
#         if 'PROCEDURE DIVISION' in line_upper:
#             in_procedure = True
#             continue
#         if not in_procedure or not line_strip:
#             continue
#         match = paragraph_pattern.match(line_strip)
#         #print(f"line:>>>>{line_strip} match:>>>{match}")
#         if match:
#             candidate = match.group(1)  #1 or 2 debug
#             print(f"candidate:>>>>{candidate}")
#             if not candidate.upper().endswith('EXIT'):
#                 paragraphs.append(candidate)
#     unique_methods = list(dict.fromkeys(paragraphs))
#     return unique_methods

# def build_cobol_2d_array(src_dir, filenames):
#     cobol_data = []
#     for filename in filenames:
#         file_path = os.path.join(src_dir, filename)
#         if os.path.exists(file_path):
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 cobol_text = f.read()
#                 paragraphs = extract_cobol_paragraphs_from_text(cobol_text)
#                 for para in paragraphs:
#                     cobol_data.append([filename, para])
#     return cobol_data


# def extract_cobol_methods_from_used_files(src_dir, used_programs):
#     results = {}
#     for program in used_programs:
#         file_path = os.path.join(src_dir, program)
#         if os.path.exists(file_path):
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 results[program] = extract_cobol_paragraphs_from_text(content)
#     return results

# def compare_md_cobol_2d(md_data, cobol_data):
#     # Convert to set of tuples for fast lookup
#     def norm(s): return s.strip().upper()
#     md_set = set((fn, para) for fn, para in md_data)
#     cobol_set = set((fn, para) for fn, para in cobol_data)
#     both = md_set & cobol_set

#     md_only = md_set - cobol_set
#     cobol_only = cobol_set - md_set

#     return {
#         "matched": sorted(list(both)),
#         "only_in_md": sorted(list(md_only)),
#         "only_in_cobol": sorted(list(cobol_only))
#     }


# def consolidated_func_spec(application_name,logical_unit):
#     config_data = None 
#     config_data = logical_unit
#     results =[] 
#     job_id = get_job_run_id_persistent()
#     consolidated_spec ={}
    
#     if not config_data:
#         return None
    
#     if not isinstance(config_data, dict):
#         results.append("FS Consolidation Config YAML must be a dictionary.")
        
#     if 'functional_specificiations' not in config_data or 'sections' not in config_data:
#         results.append("FS Consolidation Config YAML must contain 'functional_specificiations' and 'sections' keys.")
    
#     if not isinstance(config_data['functional_specificiations'], list) or not isinstance(config_data['sections'], list):
#         results.append("'functional_specificiations' and 'sections' in FS Consolidation Config YAML must be lists.")
        
#     combined_functional_spec = ""
#     functional_specs = config_data.get('functional_specificiations', [])
#     sections = config_data.get('sections', [])
#     action_str = config_data.get('action', 'process') # Default action is 'process'
    
#     if action_str.lower() == "process":
#         contexts = {}
#         context_keys = ['context_1', 'context_2', 'context_3']
#         for key in context_keys:
#             context_value = config_data.get(key)
#             if context_value:
#                 # Determine if context is a file path or direct content
#                 if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
#                     context_path_temp = context_path_temp = "C:/Users/YendetiLalith/Documents/CodeSpectre/MainframeApplications/LTCHPPSPricerMFApp2021"+ "/" +"context" +"/"+ context_value
#                     context_content = read_program_from_path(context_path_temp)
#                     if context_content is not None:
#                          contexts[key] = context_content
#                     else:
#                          print(f"Context file not found or readable for key '{key}': {context_path_temp}")
#                          # logger.warning(f"Context file not found or readable for key '{key}': {context_path_temp}") # Use your logger
#                 else:
#                     # Assume direct content
#                     contexts[key] = context_value
#         combined_functional_spec = "# Consolidated Functional Specification\n\n"
#         for section in sections:
#             combined_match = ""
#             for spec in functional_specs:
#                 spec = spec.strip()
#                 fs_path = config['source_path']['base_dir_default']+"/"+"output"+"/"+"generated_output_for_reference"+"/"+ spec
#                 fs_content = None
#                 if not Path(fs_path).exists():
#                     results.append(f"File not found: {fs_path}")
#                     fs_content = None
#                     continue
#                 else:    
#                     with open(fs_path, "r",encoding="utf-8", errors='ignore') as f: 
#                         fs_content = f.read()
#                 if fs_content is None:
#                     continue 

#                 section_to_search = re.escape(section.strip()) 
#                 pattern = rf"^#\s+{section_to_search}\s*\n(.*?)(?:^#\s+|\Z)"
#                 match = re.search(pattern, fs_content, re.MULTILINE | re.DOTALL)
#                 if match:
#                     match_content = match.group(1).strip()
#                     if match_content:
#                         combined_match += f"**Content of '{section.strip()}' from '{spec}'**\n\n {match_content}\n\n---\n\n" # Added separator

#             if combined_match:
#                 #agent = FunctionalSpecsConsolidatorAgent()
#                 result = fs_consolidate_agent.execute(
#                                     job_id = job_id,
#                                     base_dir = ".",
#                                     functional_specs = combined_match,
#                                 contexts = contexts,
#                                     section = section
#                                     )
                
#                 combined_functional_spec += result.content + "\n \n"
#                 pdf_file = md_string_to_pdf(combined_functional_spec, "Consolidated_spec.pdf", title="")

#                 consolidated_spec.update({"spec1":combined_functional_spec})
                
#     else:
#         results.append(f"Skipping consolidation as action is '{action_str}'.")
#     results.append("Functional Specifications consolidated successfully!")
    
#     #return consolidated_spec
#     return pdf_file













import os
from pathlib import Path

from fastapi import Form
from config import load_config
from agents.functional_spec_generator_agent import FunctionalSpecGeneratorAgent
from agents.functional_spec_consolidator_agent import FunctionalSpecsConsolidatorAgent
from pathlib import Path
import re
from agents import ReverseEngineeringAgentManager
from sampleServices2 import md_string_to_pdf
from utils.job_util import get_job_run_id_persistent, load_job_run_state
import yaml
import markdown
from utils.logger import logger

from utils.file_util import save_to_file
from utils.yaml_to_md import yaml_to_markdown

agent_manager = ReverseEngineeringAgentManager(max_retries=2, verbose=True)
fs_agent = agent_manager.get_agent("generate_functional_spec")
fs_consolidate_agent = agent_manager.get_agent("consolidate_functional_specs")
design_agent = agent_manager.get_agent("oo_designer")
mermaid_generator_agent = agent_manager.get_agent("mermaid_digram_generator")

config = load_config()

# ===========================
# REMOVED: PLATFORM_CONFIG - Now use config['platforms']
# ===========================

def validate_platform(platform: str) -> str:
    """Validate platform parameter using config"""
    platform = platform.lower()
    # ✅ Use config['platforms'] instead of hardcoded dict
    if platform not in config['platforms']:
        raise ValueError(f"Invalid platform: {platform}. Must be one of: {list(config['platforms'].keys())}")
    return platform

# ===========================
# HELPER FUNCTIONS
# ===========================

def read_program_from_path(filepath):
    """Reads content from a file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        return None

def extract_paragraphs_from_cobol(source_code):
    """
    Returns {paragraph_name: code_snippet} for a COBOL file.
    """
    pattern = re.compile(
        r'(?m)^\s*\d*\s*([A-Z0-9\-]+)\.\s*(.*?)(?=^\s*\d*\s*[A-Z0-9\-]+\.\s*|\Z)', 
        re.DOTALL | re.MULTILINE
    )    
    return {m.group(1): m.group(2).strip() for m in pattern.finditer(source_code)}

# ===========================
# MAIN FUNCTIONAL SPEC GENERATION
# ===========================

def func_spec(application_name: str, logical_unit: list, platform: str):
    """
    Generate functional specifications for specific platform
    
    Args:
        application_name: Name of the application
        logical_unit: List of logical unit configurations
        platform: "mainframe", "sas", or "java"
    
    Returns:
        Path to generated PDF file
    """
    # Validate and get platform config
    platform = validate_platform(platform)
    # ✅ Use config['platforms'] instead of PLATFORM_CONFIG
    platform_cfg = config['platforms'][platform]
    
    job_id = get_job_run_id_persistent()
    
    # ✅ Create platform-specific combined code path dynamically
    base_dir = Path(config['source_path']['base_dir_default'])
    combined_code_path = base_dir / "temp" / f"{platform}_combined.txt"
    combined_code_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Clear previous combined file for this platform
    if combined_code_path.exists():
        combined_code_path.unlink()
    
    config_data = logical_unit
    results = []
    specs = {}
    pdf_file = None
    
    logger.info(f"[{platform_cfg['display_name']}] Processing {len(config_data)} items from config")
    print(f"DEBUG: [{platform_cfg['display_name']}] Processing {len(config_data)} items from config")
    
    for item in config_data:
        record_id = item.get('id', 'unknown_id')
        programs_list = item.get('programs', [])
        action_str = item.get('action', 'process')
        
        print(f"DEBUG: [{platform_cfg['display_name']}] Processing record_id={record_id}, action={action_str}, programs={len(programs_list)}")
        logger.info(f"[{platform_cfg['display_name']}] Processing record_id={record_id}")
        
        if action_str.lower() == "process":
            combined_code = ""
            contexts = {}
            context_keys = ['context_1', 'context_2', 'context_3']
            
            # Load contexts
            for key in context_keys:
                context_value = item.get(key)
                if context_value:
                    if isinstance(context_value, str) and (
                        context_value.lower().endswith('.md') or 
                        context_value.lower().endswith('.csv')
                    ):
                        context_path = Path(config['source_path']['base_dir_default']) / "context" / context_value
                        print(f"DEBUG: [{platform_cfg['display_name']}] Loading context {key} from {context_path}")
                        
                        if context_path.exists():
                            context_content = read_program_from_path(str(context_path))
                            if context_content is not None:
                                contexts[key] = context_content
                                print(f"DEBUG: Loaded {key}, size={len(context_content)}")
                            else:
                                logger.warning(f"Failed to read {key}: {context_path}")
                                print(f"WARNING: Failed to read {key}: {context_path}")
                        else:
                            logger.warning(f"Context file not found: {context_path}")
                            print(f"WARNING: Context file not found: {context_path}")
                    else:
                        contexts[key] = context_value

            # Load program files
            print(f"DEBUG: [{platform_cfg['display_name']}] Loading {len(programs_list)} programs")
            logger.info(f"[{platform_cfg['display_name']}] Loading {len(programs_list)} programs")
            
            for program in programs_list:
                program = program.strip()
                
                # Skip data files
                if program.lower().endswith(('.csv', '.txt', '.dat', '.xlsx')):
                    print(f"DEBUG: Skipping data file: {program}")
                    continue
                
                # ✅ Use dynamic source directory helper
                source_dir = Path(config['get_source_dir'](platform))
                source_code_path = source_dir / program
                print(f"DEBUG: Looking for program at: {source_code_path}")
                
                if not source_code_path.exists():
                    error_msg = f"File not found: {source_code_path}"
                    logger.error(error_msg)
                    print(f"ERROR: {error_msg}")
                    results.append(error_msg)
                    
                else:
                    try:
                        with open(source_code_path, "r", encoding="utf-8", errors='ignore') as f: 
                            code = f.read()

                        if code:
                            # Use platform-specific language for code blocks
                            combined_code += f"## Content of {program}\n```\n{code}\n```\n\n"
                            
                            # Append to platform-specific combined file
                            with open(combined_code_path, "a", encoding="utf-8") as file:
                                file.write(f"## Content of {program}\n```\n{code}\n```\n\n")
                            
                            print(f"DEBUG: [{platform_cfg['display_name']}] Added {program}, code length={len(code)}")
                            logger.info(f"Added {program}, code length={len(code)}")
                        else:
                            logger.warning(f"Empty file: {program}")
                            print(f"WARNING: Empty file: {program}")
                
                    except Exception as e:
                        error_msg = f"Failed to read {program}: {e}"
                        logger.error(error_msg)
                        print(f"ERROR: {error_msg}")
                        results.append(f"Error reading {program}: {str(e)}")
            
            print(f"DEBUG: [{platform_cfg['display_name']}] combined_code length = {len(combined_code)}")
            
            if combined_code:
                try:
                    print(f"DEBUG: [{platform_cfg['display_name']}] Calling fs_agent.execute for {record_id}")
                    logger.info(f"Calling fs_agent for {record_id}")

                    # Determine program_type from platform config or item
                    program_type = item.get('program_type', platform_cfg.get('program_type', 'batch_programs'))

                    output = fs_agent.execute(
                        job_id=job_id,
                        record_id=record_id,
                        base_dir=".",
                        code=combined_code,
                        contexts=contexts,
                        programs=programs_list,
                        platform=platform,
                        program_type=program_type
                    )

                    print(f"DEBUG: Agent output length = {len(output) if output else 0}")

                    # ✅ Save markdown to platform-specific directory using helper
                    md_filename = f"{record_id}_FunctionalSpecification.md"
                    md_dir = Path(config['get_output_dir'](platform))
                    md_dir.mkdir(parents=True, exist_ok=True)
                    md_path = md_dir / md_filename

                    print(f"DEBUG: [{platform_cfg['display_name']}] Saving markdown to {md_path}")
                    save_to_file(str(md_path), output)
                    logger.info(f"Saved markdown to {md_path}")

                    # Optional: Call validation agent
                    try:
                        validation_agent = agent_manager.get_agent("validation_agent")
                        print(f"DEBUG: [{platform_cfg['display_name']}] Invoking validation agent for record_id={record_id}")
                        logger.info(f"Invoking validation agent for {record_id}")
                        
                        validation_resp = validation_agent.execute(
                            job_id=job_id,
                            record_id=record_id,
                            base_dir=".",
                            source_code=combined_code,
                            functional_spec=output,
                            platform=platform
                        )
                        print(f"DEBUG: Validation completed for {record_id}")
                        logger.info(f"Validation completed for {record_id}")
                    except Exception as ve:
                        logger.warning(f"Validation failed for {record_id}: {ve}")
                        print(f"WARNING: Validation failed for {record_id}: {ve}")
                        results.append(f"Validation failed for {record_id}: {ve}")

                    # ✅ Generate PDF using dynamic PDF directory helper
                    pdf_title = f"{record_id} - {platform_cfg['display_name']} Functional Specifications"
                    pdf_file_name = f"{record_id}_FunctionalSpecification.pdf"
                    
                    # Use dynamic PDF directory
                    pdf_dir = Path(config['get_pdf_dir'](platform))
                    pdf_dir.mkdir(parents=True, exist_ok=True)
                    
                    print(f"DEBUG: [{platform_cfg['display_name']}] Generating PDF: {pdf_file_name}")
                    
                    pdf_file = md_string_to_pdf(
                        output, 
                        pdf_file_name, 
                        title=pdf_title,
                        output_dir=str(pdf_dir)
                    )

                    print(f"DEBUG: PDF generated: {pdf_file}")
                    logger.info(f"PDF generated: {pdf_file}")

                except Exception as e:
                    error_msg = f"Error generating spec for {record_id}: {str(e)}"
                    logger.error(error_msg)
                    print(f"ERROR: {error_msg}")
                    results.append(error_msg)
                    raise ValueError(error_msg)
            else:
                logger.warning(f"combined_code is empty for {record_id}")
                print(f"WARNING: combined_code is empty for {record_id}")
        else:
            logger.info(f"Skipping {record_id}, action={action_str}")
            print(f"DEBUG: Skipping {record_id}, action={action_str}")
            results.append(f"Skipping '{record_id}' as action is '{action_str}'.")
    
    print(f"DEBUG: Final pdf_file = {pdf_file}")
    results.append(f"{platform_cfg['display_name']} Functional Specifications generation completed!")
    logger.info(f"{platform_cfg['display_name']} Functional Specifications generation completed!")
    
    if pdf_file is None:
        raise ValueError(
            "No PDF file was generated. Check logs above for errors."
        )
    
    return pdf_file

# ===========================
# CONSOLIDATED FUNCTIONAL SPEC
# ===========================

def consolidated_func_spec(application_name: str, logical_unit: dict, platform: str):
    """
    Consolidate functional specifications for specific platform
    
    Args:
        application_name: Name of the application
        logical_unit: Dictionary containing consolidation configuration
        platform: "mainframe", "sas", or "java"
    
    Returns:
        Path to generated consolidated PDF file
    """
    # Validate and get platform config
    platform = validate_platform(platform)
    # ✅ Use config['platforms'] instead of PLATFORM_CONFIG
    platform_cfg = config['platforms'][platform]
    
    config_data = logical_unit
    results = [] 
    job_id = get_job_run_id_persistent()
    consolidated_spec = {}
    
    logger.info(f"[{platform_cfg['display_name']}] Starting consolidation for {application_name}")
    print(f"DEBUG: [{platform_cfg['display_name']}] Starting consolidation")
    
    if not config_data:
        logger.error("No config data provided for consolidation")
        return None
    
    if not isinstance(config_data, dict):
        error_msg = "FS Consolidation Config YAML must be a dictionary."
        logger.error(error_msg)
        results.append(error_msg)
        raise ValueError(error_msg)
        
    if 'functional_specificiations' not in config_data or 'sections' not in config_data:
        error_msg = "FS Consolidation Config YAML must contain 'functional_specificiations' and 'sections' keys."
        logger.error(error_msg)
        results.append(error_msg)
        raise ValueError(error_msg)
    
    if not isinstance(config_data['functional_specificiations'], list) or not isinstance(config_data['sections'], list):
        error_msg = "'functional_specificiations' and 'sections' in FS Consolidation Config YAML must be lists."
        logger.error(error_msg)
        results.append(error_msg)
        raise ValueError(error_msg)
        
    combined_functional_spec = ""
    functional_specs = config_data.get('functional_specificiations', [])
    sections = config_data.get('sections', [])
    action_str = config_data.get('action', 'process')
    
    if action_str.lower() == "process":
        contexts = {}
        context_keys = ['context_1', 'context_2', 'context_3']
        
        # Load contexts
        for key in context_keys:
            context_value = config_data.get(key)
            if context_value:
                if isinstance(context_value, str) and (
                    context_value.lower().endswith('.md') or 
                    context_value.lower().endswith('.csv')
                ):
                    context_path = Path(config['source_path']['base_dir_default']) / "context" / context_value
                    context_content = read_program_from_path(str(context_path))
                    if context_content is not None:
                        contexts[key] = context_content
                        logger.info(f"Loaded context {key}")
                    else:
                        logger.warning(f"Context file not found or readable for key '{key}': {context_path}")
                else:
                    contexts[key] = context_value
        
        combined_functional_spec = f"# Consolidated {platform_cfg['display_name']} Functional Specification\n\n"
        
        # ✅ Use dynamic output directory helper
        output_base_dir = Path(config['get_output_dir'](platform))
        
        for section in sections:
            combined_match = ""
            
            for spec in functional_specs:
                spec = spec.strip()
                
                # Look for spec in platform-specific directory
                fs_path = output_base_dir / spec
                
                logger.info(f"Looking for spec file: {fs_path}")
                
                if not fs_path.exists():
                    logger.warning(f"File not found: {fs_path}")
                    results.append(f"File not found: {fs_path}")
                    continue
                
                fs_content = read_program_from_path(str(fs_path))
                
                if fs_content is None:
                    continue

                # Extract section content
                section_to_search = re.escape(section.strip()) 
                pattern = rf"^#\s+{section_to_search}\s*\n(.*?)(?:^#\s+|\Z)"
                match = re.search(pattern, fs_content, re.MULTILINE | re.DOTALL)
                
                if match:
                    match_content = match.group(1).strip()
                    if match_content:
                        combined_match += f"**Content of '{section.strip()}' from '{spec}'**\n\n{match_content}\n\n---\n\n"

            if combined_match:
                logger.info(f"Consolidating section: {section}")
                
                result = fs_consolidate_agent.execute(
                    job_id=job_id,
                    base_dir=".",
                    functional_specs=combined_match,
                    contexts=contexts,
                    section=section,
                    platform=platform
                )
                
                combined_functional_spec += result.content + "\n\n"
        
        # Generate consolidated PDF with platform-specific name
        pdf_filename = f"{application_name}_{platform_cfg['display_name']}_Consolidated_FunctionalSpec.pdf"
        pdf_title = f"{application_name} - {platform_cfg['display_name']} Consolidated Functional Specifications"
        
        # ✅ Save to platform-specific PDF directory (or subdirectory)
        pdf_output_dir = Path(config['get_pdf_dir'](platform)).parent / "consolidated"
        pdf_output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Generating consolidated PDF: {pdf_filename}")
        print(f"DEBUG: [{platform_cfg['display_name']}] Generating consolidated PDF")
        
        pdf_file = md_string_to_pdf(
            combined_functional_spec, 
            pdf_filename, 
            title=pdf_title,
            output_dir=str(pdf_output_dir)
        )

        consolidated_spec.update({"spec1": combined_functional_spec})
        logger.info(f"Consolidated PDF generated: {pdf_file}")
        
    else:
        logger.info(f"Skipping consolidation as action is '{action_str}'")
        results.append(f"Skipping consolidation as action is '{action_str}'.")
    
    results.append(f"{platform_cfg['display_name']} Functional Specifications consolidated successfully!")
    logger.info(f"{platform_cfg['display_name']} consolidation completed")
    
    return pdf_file

# ===========================
# COBOL-SPECIFIC FUNCTIONS (Mainframe only)
# ===========================

def extract_cobol_paragraphs_from_text(cobol_text):
    """Extract paragraphs from COBOL text - Mainframe specific"""
    in_procedure = False
    paragraphs = []
    paragraph_pattern = re.compile(r'^\s*\d{0,6}\s+([A-Za-z0-9\-]+)\.\s*$', re.MULTILINE)
    
    for line in cobol_text.splitlines():
        line_strip = line.strip()
        line_upper = line_strip.upper()
        
        if 'PROCEDURE DIVISION' in line_upper:
            in_procedure = True
            continue
        
        if not in_procedure or not line_strip:
            continue
        
        match = paragraph_pattern.match(line_strip)
        
        if match:
            candidate = match.group(1)
            print(f"candidate:>>>>{candidate}")
            if not candidate.upper().endswith('EXIT'):
                paragraphs.append(candidate)
    
    unique_methods = list(dict.fromkeys(paragraphs))
    return unique_methods

def build_cobol_2d_array(src_dir, filenames):
    """Build 2D array of COBOL paragraphs - Mainframe specific"""
    cobol_data = []
    
    for filename in filenames:
        file_path = os.path.join(src_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                cobol_text = f.read()
                paragraphs = extract_cobol_paragraphs_from_text(cobol_text)
                for para in paragraphs:
                    cobol_data.append([filename, para])
    
    return cobol_data

def extract_cobol_methods_from_used_files(src_dir, used_programs):
    """Extract COBOL methods from used files - Mainframe specific"""
    results = {}
    
    for program in used_programs:
        file_path = os.path.join(src_dir, program)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                results[program] = extract_cobol_paragraphs_from_text(content)
    
    return results

def compare_md_cobol_2d(md_data, cobol_data):
    """Compare markdown and COBOL data - Mainframe specific"""
    def norm(s): 
        return s.strip().upper()
    
    md_set = set((fn, para) for fn, para in md_data)
    cobol_set = set((fn, para) for fn, para in cobol_data)
    both = md_set & cobol_set

    md_only = md_set - cobol_set
    cobol_only = cobol_set - md_set

    return {
        "matched": sorted(list(both)),
        "only_in_md": sorted(list(md_only)),
        "only_in_cobol": sorted(list(cobol_only))
    }
