## CodeSpectre 
### mainframe_code to FS and then Java/python Code generations 
Mainframe COBOL code to Java/Python Code conversion. 
This application contains the following key functionalities: 
  generation of functional specification for the uploaded cobol code.
  consolidation of functional specifications
  generaion of object oriented design document and class diagram
  generation of java/pytho code

## CodeSpectre
sourcecode is present  in mf_modernization folder 
  PromptTemplate: All prompts are stored inside the application, under prompts_template folder
  ### config.py
  this contains the default configuration required such as base_dir for application to run.
  ### env
  this contains API KEY and URLs
  ### agents/agent_config.py
  this contains all configuration required for agents to run.
  ### design.css contains css details

## Configuration for the given Mainframe Application(eg MainframeApplications\LTCHPPSPricerMFApp2021)
Base directory: Mainframe Source Code Base directory.
SourceCode: COBOL Source code are stored at BaseDirectory/sourcecode
Contexts: Contexts used are stored at BaseDirectory/contexts
Config: default configuration files are present. logical unit configuration and functional specification consolidation
Outputs: 
FunctionalSpecfications/Design/Code outputs are stored at BaseDirectory/output
Prompt response/logs : while running, prompts response and logs are stored at BaseDirectory/output


### Install all required python dependencies in your virutal environment

### Logical Units - details
List of source files(logical units) that need to be processed is to be uploaded.
reference file: logical_units_sourcecode_with_dependencies_config.yaml.
for example,MainframeApplications\LTCHPPSPricerMFApp2021\config\logical_units_sourcecode_with_dependencies_config.yaml

This supports three contexts
content of configuration file:
- id: L8
  programs: [LTCAL032, LTCAL042, LTDRG031]
  context_1: additional_context.md
  context_2: LTCAL032, LTCAL042, LTDRG031
  context_3: SampleCSV.csv
  action: process   //process records only with process
  remarks: 8th level

### Functional Speicification Generation:
All functional specifications(generated for logical units level) and are stored at output folder.
For example L1_FunctionalSpecification.md, L2_FunctionalSpecification.md etc.

### Consolidate Functional Speicification
Consolidation config is uploaded
reference file: .
for example,MainframeApplications\LTCHPPSPricerMFApp2021\config\functional_specification_consolidation_config.yaml
Based consolidation configuration file, all different sections of all Functional Specifications are consolidated.
outputfile name:consolidated_FunctionalSpecification.md

### Generate OO Design
Input: Consolidated Functional Speicification.e.gconsolidated_FunctionalSpecification.md
Output: Design document (oo_design.md)

### Generate Class Diagram
Input: Design Document.(oo_design.md)
Output: Class Diagram (oo_diagram.md)

### Generate OO code
Input: OO Design and Consolidated Functional Speicification (oo_design.md, consolidated_FunctionalSpecification.md)
Output: Java Code/Python Code.

## How to run the application.
streamlit run main_app.py 

