
import os
from pathlib import Path
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
mermaid_generator_agent=agent_manager.get_agent("mermaid_digram_generator")



config = load_config()

def read_program_from_path(filepath):
    """Reads content from a file."""
    with open(filepath, "r") as f: # Specify encoding
        return f.read()
    
import re

def extract_paragraphs_from_cobol(source_code):
    """
    Returns {paragraph_name: code_snippet} for a COBOL file.
    """
    # Regex: Paragraphs start with label ending with '.' at line start.
    pattern = re.compile(
        r'(?m)^\s*\d*\s*([A-Z0-9\-]+)\.\s*(.*?)(?=^\s*\d*\s*[A-Z0-9\-]+\.\s*|\Z)', 
        re.DOTALL | re.MULTILINE
    )    
    return {m.group(1): m.group(2).strip() for m in pattern.finditer(source_code)}

def func_spec(application_name, logical_unit):
    job_id = get_job_run_id_persistent()
    combined_code_path = r"C:\Users\YendetiLalith\Documents\CodeSpectre\mf_modernization\sas_combined.txt"
    # combined_code_path = r"C:\Users\YendetiLalith\Documents\CodeSpectre\mf_modernization\pyspark_combined.txt"
    
    config_data = logical_unit
    results = []
    specs = {}
    pdf_file = None
    
    print(f"DEBUG: Processing {len(config_data)} items from config")  # ← ADD
    
    for item in config_data:
        record_id = item.get('id', 'unknown_id')
        programs_list = item.get('programs', [])
        action_str = item.get('action', 'process')
        
        print(f"DEBUG: Processing record_id={record_id}, action={action_str}, programs={len(programs_list)}")  # ← ADD
        
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
                        print(f"DEBUG: Loading context {key} from {context_path}")  # ← ADD
                        
                        if context_path.exists():
                            context_content = read_program_from_path(str(context_path))
                            if context_content is not None:
                                contexts[key] = context_content
                                print(f"DEBUG: Loaded {key}, size={len(context_content)}")  # ← ADD
                            else:
                                print(f"WARNING: Failed to read {key}: {context_path}")
                        else:
                            print(f"WARNING: Context file not found: {context_path}")
                    else:
                        contexts[key] = context_value

            # Load program files
            print(f"DEBUG: Loading {len(programs_list)} programs")  # ← ADD
            
            for program in programs_list:
                program = program.strip()
                
                # Skip data files
                if program.lower().endswith(('.csv', '.txt', '.dat')):
                    print(f"DEBUG: Skipping data file: {program}")  # ← ADD
                    continue
                
                source_code_path = Path(config['source_path']['base_dir_default']) / "source_code" / program
                print(f"DEBUG: Looking for program at: {source_code_path}")  # ← ADD
                
                if not source_code_path.exists():
                    print(f"ERROR: File not found: {source_code_path}")  # ← ADD
                    results.append(f"File not found: {source_code_path}")
                    
                else:
                    try:
                        with open(source_code_path, "r", encoding="utf-8", errors='ignore') as f: 
                            code = f.read()

                        if code:
                            combined_code += f"## Content of {program}\n```sas\n{code}```\n\n"
                            # combined_code += f"## Content of {program}\n```pyspark\n{code}```\n\n"
                            with open(combined_code_path, "a") as file:
                                file.write(combined_code)
                            print(f"DEBUG: Added {program}, code length={len(code)}")  # ← ADD
                        else:
                            print(f"WARNING: Empty file: {program}")  # ← ADD
                
                    except Exception as e:
                        print(f"ERROR: Failed to read {program}: {e}")  # ← ADD
                        results.append(f"Error reading {program}: {str(e)}")
            
                print(f"DEBUG: combined_code length = {len(combined_code)}")  # ← ADD
            
                if combined_code:
                    try:
                        print(f"DEBUG: Calling fs_agent.execute for {record_id}")  # ← ADD

                        output = fs_agent.execute(
                            job_id=job_id,
                            record_id=record_id,
                            base_dir=".",
                            code=combined_code,
                            contexts=contexts,
                            programs=programs_list
                        )

                        print(f"DEBUG: Agent output length = {len(output) if output else 0}")  # ← ADD

                        # Save markdown
                        md_filename = f"{record_id}_FunctionalSpecification.md"
                        md_dir = Path(config['source_path']['base_dir_default']) / "output" / "sas_specifications"
                        # md_dir = Path(config['source_path']['base_dir_default']) / "output" / "pyspark_specifications"
                        md_dir.mkdir(parents=True, exist_ok=True)
                        md_path = md_dir / md_filename

                        print(f"DEBUG: Saving markdown to {md_path}")  # ← ADD
                        save_to_file(str(md_path), output)

                        # ---- Call validation agent automatically after spec generation ----
                        # try:
                        #     validation_agent = agent_manager.get_agent("validation_agent")
                        #     print(f"DEBUG: Invoking validation agent for record_id={record_id}")
                        #     validation_resp = validation_agent.execute(
                        #         job_id=job_id,
                        #         record_id=record_id,
                        #         base_dir=".",
                        #         source_code=combined_code,
                        #         functional_spec=output,
                        #     )
                        #     print(f"DEBUG: Validation completed for {record_id}")
                        # except Exception as ve:
                        #     # Log but don't fail the whole generation process
                        #     print(f"WARNING: Validation failed for {record_id}: {ve}")
                        #     results.append(f"Validation failed for {record_id}: {ve}")
                        # ------------------------------------------------------------------

                        # Generate PDF
                        pdf_title = f"{record_id} - SAS Functional Specifications"
                        # pdf_title = f"{record_id} - PYSPARK Functional Specifications"
                        pdf_file_name = f"{record_id}_FunctionalSpecification.pdf"

                        print(f"DEBUG: Generating PDF: {pdf_file_name}")  # ← ADD
                        pdf_file = md_string_to_pdf(output, pdf_file_name, title=pdf_title)

                        print(f"DEBUG: PDF generated: {pdf_file}")  # ← ADD

                    except Exception as e:
                        error_msg = f"Error generating spec for {record_id}: {str(e)}"
                        print(f"ERROR: {error_msg}")  # ← ADD
                        results.append(error_msg)
                        raise ValueError(error_msg)
                else:
                    print(f"WARNING: combined_code is empty for {record_id}")  # ← ADD
        else:
            print(f"DEBUG: Skipping {record_id}, action={action_str}")  # ← ADD
            results.append(f"Skipping '{record_id}' as action is '{action_str}'.")
    
    print(f"DEBUG: Final pdf_file = {pdf_file}")  # ← ADD
    # results.append("SAS Functional Specifications generation completed!")
    results.append("SAS Functional Specifications generation completed!")
    
    if pdf_file is None:
        raise ValueError(
            "No PDF file was generated. Check logs above for errors."
        )
    
    return pdf_file



    
# def func_spec(application_name,logical_unit):

#     job_id = get_job_run_id_persistent()
#     combined_code_path = r"C:\Users\YendetiLalith\Documents\CodeSpectre\mf_modernization\example.txt"
#     config_data = None

#     config_data = logical_unit
        
#     results = []
#     specs={}

#     for item in config_data:
        
#         record_id = item.get('id', 'unknown_id') 
#         programs_list = item.get('programs', [])
#         action_str = item.get('action', 'process')
        
#         if action_str.lower() == "process":
#             combined_code = ""
#             contexts = {}
#             context_keys = ['context_1', 'context_2', 'context_3']
#             for key in context_keys:
#                 context_value = item.get(key)
#                 if context_value:
#                     if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
#                         context_path_temp = "C:/Users/YendetiLalith/Documents/CodeSpectre/MainframeApplications/LTCHPPSPricerMFApp2021"+ "/" +"context" +"/"+ context_value
#                         context_content = read_program_from_path(context_path_temp)
#                         if context_content is not None:
#                             contexts[key] = context_content
#                         else:
#                             print(f"Context file not found or readable for key '{key}': {context_path_temp}")
#                     else:
#                         contexts[key] = context_value

#             for program in programs_list:
#                 program = program.strip()
#                 code=None
#                 source_code_path = config['source_path']['base_dir_default'] + "/" +"source_code" + "/" + program
#                 if not Path(source_code_path).exists():
#                     results.append(f"File not found: {source_code_path}")
#                 else:
#                     with open(source_code_path, "r",encoding="utf-8", errors='ignore') as f: 
#                         source_code_content= f.read()
#                         code = source_code_content
#                     if code:
#                         combined_code += f"## Content of {program}\n```cobol\n{code}\n```\n\n"
#                         with open(combined_code_path, "a") as file:
#                             file.write(combined_code)
#                     else:
#                         results.append(f"Source code file not found or readable for program: {program}")
#                 if combined_code:
#                     try:
#                         output =  fs_agent.execute(
#                                             job_id = job_id,
#                                             record_id = record_id,
#                                             base_dir = ".",
#                                             code = combined_code,
#                                             contexts = contexts,
#                                             programs = programs_list
#                                         )
#                         # output_yaml =  fs_agent.execute(
#                         #                     job_id = job_id,
#                         #                     record_id = record_id,
#                         #                     base_dir = ".",
#                         #                     code = combined_code,
#                         #                     contexts = contexts,
#                         #                     programs = programs_list
#                         #                 )
                        
#                         # markdown_content = yaml_to_markdown(output_yaml, include_code=True)        # For interactive Markdown file
#                         # markdown_content_for_pdf = yaml_to_markdown(output_yaml, include_code=False) # For PDF without code if desired

#                         # final_md = output.strip() + '\n\n' + markdown_content.strip()
#                         # final_md_pdf = output.strip() + '\n\n' + markdown_content_for_pdf.strip()


#                         fspec={f"new{record_id}_FunctionalSpecification.md" : output}
#                         specs["functional_specifications"] = fspec

#                         md_filename = f"{record_id}_FunctionalSpecification.md"
#                         #md_dir = Path(config['source_path']['base_dir_default']) / "output" / "generated_output_for_reference"
#                         md_dir = Path("C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs")
#                         md_dir.mkdir(parents=True, exist_ok=True)
#                         md_path = md_dir / md_filename
#                         save_to_file(str(md_path), output)

#                         pdf_title = f"{record_id} - Functional Specifications"
#                         pdf_file_name =f"{record_id}_FunctionalSpecification.pdf"
#                         pdf_file = md_string_to_pdf(output, pdf_file_name, title=pdf_title)

#                     except Exception as e:
#                         print(str(e))                 
#         else:
#             results.append(f"Skipping generation for '{record_id}' as action is '{action_str}'.")
#     results.append("Functional Specifications generation process completed!")
#     return pdf_file                                      



import os
import re

def extract_cobol_paragraphs_from_text(cobol_text):
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
        #print(f"line:>>>>{line_strip} match:>>>{match}")
        if match:
            candidate = match.group(1)  #1 or 2 debug
            print(f"candidate:>>>>{candidate}")
            if not candidate.upper().endswith('EXIT'):
                paragraphs.append(candidate)
    unique_methods = list(dict.fromkeys(paragraphs))
    return unique_methods

def build_cobol_2d_array(src_dir, filenames):
    cobol_data = []
    for filename in filenames:
        file_path = os.path.join(src_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                cobol_text = f.read()
                paragraphs = extract_cobol_paragraphs_from_text(cobol_text)
                for para in paragraphs:
                    cobol_data.append([filename, para])
    return cobol_data


def extract_cobol_methods_from_used_files(src_dir, used_programs):
    results = {}
    for program in used_programs:
        file_path = os.path.join(src_dir, program)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                results[program] = extract_cobol_paragraphs_from_text(content)
    return results

def compare_md_cobol_2d(md_data, cobol_data):
    # Convert to set of tuples for fast lookup
    def norm(s): return s.strip().upper()
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


def consolidated_func_spec(application_name,logical_unit):
    config_data = None 
    config_data = logical_unit
    results =[] 
    job_id = get_job_run_id_persistent()
    consolidated_spec ={}
    
    if not config_data:
        return None
    
    if not isinstance(config_data, dict):
        results.append("FS Consolidation Config YAML must be a dictionary.")
        
    if 'functional_specificiations' not in config_data or 'sections' not in config_data:
        results.append("FS Consolidation Config YAML must contain 'functional_specificiations' and 'sections' keys.")
    
    if not isinstance(config_data['functional_specificiations'], list) or not isinstance(config_data['sections'], list):
        results.append("'functional_specificiations' and 'sections' in FS Consolidation Config YAML must be lists.")
        
    combined_functional_spec = ""
    functional_specs = config_data.get('functional_specificiations', [])
    sections = config_data.get('sections', [])
    action_str = config_data.get('action', 'process') # Default action is 'process'
    
    if action_str.lower() == "process":
        contexts = {}
        context_keys = ['context_1', 'context_2', 'context_3']
        for key in context_keys:
            context_value = config_data.get(key)
            if context_value:
                # Determine if context is a file path or direct content
                if isinstance(context_value, str) and (context_value.lower().endswith('.md') or context_value.lower().endswith('.csv')):
                    context_path_temp = context_path_temp = "C:/Users/YendetiLalith/Documents/CodeSpectre/MainframeApplications/LTCHPPSPricerMFApp2021"+ "/" +"context" +"/"+ context_value
                    context_content = read_program_from_path(context_path_temp)
                    if context_content is not None:
                         contexts[key] = context_content
                    else:
                         print(f"Context file not found or readable for key '{key}': {context_path_temp}")
                         # logger.warning(f"Context file not found or readable for key '{key}': {context_path_temp}") # Use your logger
                else:
                    # Assume direct content
                    contexts[key] = context_value
        combined_functional_spec = "# Consolidated Functional Specification\n\n"
        for section in sections:
            combined_match = ""
            for spec in functional_specs:
                spec = spec.strip()
                fs_path = config['source_path']['base_dir_default']+"/"+"output"+"/"+"generated_output_for_reference"+"/"+ spec
                fs_content = None
                if not Path(fs_path).exists():
                    results.append(f"File not found: {fs_path}")
                    fs_content = None
                    continue
                else:    
                    with open(fs_path, "r",encoding="utf-8", errors='ignore') as f: 
                        fs_content = f.read()
                if fs_content is None:
                    continue 

                section_to_search = re.escape(section.strip()) 
                pattern = rf"^#\s+{section_to_search}\s*\n(.*?)(?:^#\s+|\Z)"
                match = re.search(pattern, fs_content, re.MULTILINE | re.DOTALL)
                if match:
                    match_content = match.group(1).strip()
                    if match_content:
                        combined_match += f"**Content of '{section.strip()}' from '{spec}'**\n\n {match_content}\n\n---\n\n" # Added separator

            if combined_match:
                #agent = FunctionalSpecsConsolidatorAgent()
                result = fs_consolidate_agent.execute(
                                    job_id = job_id,
                                    base_dir = ".",
                                    functional_specs = combined_match,
                                contexts = contexts,
                                    section = section
                                    )
                
                combined_functional_spec += result.content + "\n \n"
                pdf_file = md_string_to_pdf(combined_functional_spec, "Consolidated_spec.pdf", title="")

                consolidated_spec.update({"spec1":combined_functional_spec})
                
    else:
        results.append(f"Skipping consolidation as action is '{action_str}'.")
    results.append("Functional Specifications consolidated successfully!")
    
    #return consolidated_spec
    return pdf_file
