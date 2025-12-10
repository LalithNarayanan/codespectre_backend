# agents/functional_spec_generator_agent.py

from .agent_base import AgentBase
from loguru import logger
from utils.yaml_load import load_yaml_file, load_topics
from utils.file_util import save_to_file,write_job_data_to_csv
import time


UNIVERSAL_MARKDOWN_PROMPT = """
    For all sections, format your answer exclusively using markdown syntax. Use appropriate markdown elements such as headings, subheadings, bullet points, numbered lists, code blocks, and tables to enhance readability and organization of the content.
    Follow same and best practice(s) in markdown formatting.
    Dont include tables, nor code snippets unless specifically requested.
    """
#To generate the functional specification from the Code
class FunctionalSpecGeneratorAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="FunctionalSpecGeneratorAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)
        self.functional_specification: str = None
        self.code: str = None
        self.job_id: str =None
        self.record_id: str =None
        self.contexts: object =None
        self.base_dir: str = None
        self.programs: str = None
        self.template_key: str = None
        self.placeholders: object = None

# functional_spec = fs_agent.execute(job_id=job_id,record_id=record_id,code=source_code,contexts=contexts)
    def execute(self, job_id,record_id,base_dir,code,contexts,programs, orchestrate="sequential"):
        # print(f"execute...fs_agent..!!.{base_dir}")
        self.job_id = job_id
        self.record_id = record_id
        self.code = code
        self.contexts=contexts
        self.placeholders = self.contexts.copy()
        self.placeholders['code']=self.code
        logger.info(f"placeholders:>>>{self.placeholders}")
        ############################
        # print(f"context:>>>> {contexts}")
        keys_with_values = ['code']
        for key, value in self.contexts.items():
            if value:  # Checks for truthiness (not None, not empty string/list/dict, not 0, not False)
                keys_with_values.append(key)
        # print(f"{keys_with_values}") 
        #Including code and all contexts
        self.template_key=keys_with_values
        ############################
        self.base_dir=base_dir
        self.programs=programs
        summary = self.create_functional_specification(orchestrate)
        return summary

    def are_representations_equal(self,str_repr, list_repr):
        list_from_string = str_repr.split(',')
        list_from_string = [item.strip() for item in list_from_string]
        flag = sorted(list_from_string) == sorted(list_repr)
        # print(f"flag:>>>>>>>>{flag}")
        return flag
    
    #Extract user message and system message for the given system
    def extract_prompt(self,section_name):
        #prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_cbl_prompts.yaml") 
        prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_sas_prompts_versioned.yaml") 
        # prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_pyspark_versioned.yaml") 
        # prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_sas_prompts_improved.yaml") 
        # TODO
        category = "code2functionalspec"
        if category in prompts and section_name in prompts[category] and "versions" in prompts[category][section_name]:
            versions = prompts[category][section_name]["versions"]
            selected_version = None
            for version_data in versions:
                logger.info(f"version=>>: {version_data["version"]}")
                foundFlag =  self.are_representations_equal(version_data["version"], self.template_key)
                if foundFlag:
                    selected_version = version_data
                    break  # Stop searching once version 1.0 is found
             #Go for default           
            if selected_version is None:
                for version_data in versions:
                    if version_data["version"]=='code':
                        selected_version=version_data
                        break
            if selected_version:
                logger.info(f"system_message: {selected_version["system_message"]}")
                    # STEP: Prepend universal prompt to user message
                selected_version['user_message'] = (
                    UNIVERSAL_MARKDOWN_PROMPT.strip() + "\n\n" + selected_version['user_message'].strip()
                )
                logger.info(f"***************************user_message:>>>>> {selected_version["user_message"]}")
                return selected_version
            else:
                logger.info("Version  not found.")
            return selected_version
            
        else:
            logger.error(f"Prompt name=> {section_name} with version information not found.")
            return None

    #Extract prompt and execute
    def extract_prompt_and_execute(self,topic):
        logger.info(f"\n extract_prompt_and_execute topic:***********{topic}*********")
        start_time = time.time()
        prompts=self.extract_prompt(topic)
        if prompts:
            system_message = prompts["system_message"]
            user_message = prompts["user_message"]
            prompt_template=prompts["user_message"]
            # formatted_user_message = user_message.format(
            #     code=self.code,
            # )
            try:
                formatted_user_message=user_message.format(
                **self.placeholders)
            except KeyError as e:
                print(f"Warning: Could not replace placeholder '{e}' in the message. Key not found in data.")
                formatted_user_message=user_message

            messages = [
                { "role": "system", "content": system_message },
                { "role": "user", "content": formatted_user_message } ]
            llm_start_time = time.time()
            response = self.call_model(messages, max_tokens=650000)
            response_content=response.content
        else:
            response = f"Unable to fetch prompt extract_programoverview"
        end_time = time.time()
        overall_processing_time = end_time - start_time
        llm_processing_time= end_time - llm_start_time
        
        file_name=rf"{self.base_dir}\output\{self.job_id}_{self.record_id}_{topic}.md"
        save_to_file(file_name,response_content)
        logger.info(f"\n********* {topic} is saved at {file_name}  **************")

        #save the response;
        job_info = {
        'job_id': self.job_id,
        'llm_model_name': self.model,
        'llm_processing_time': llm_processing_time,  
        'overall_processing_time': overall_processing_time,
        'prompt_name': topic,
        'prompt_template': prompt_template,
        'unit':  self.record_id,
        'input': self.programs,
        'output_type': "func_spec",
        'output_file': file_name,
        }
        job_csv_file_name=rf"{self.base_dir}\output\job_details.csv"
        write_job_data_to_csv(job_data=job_info, file_name=job_csv_file_name)
        logger.info(f"\n********* Job:{self.job_id} is updated at {job_csv_file_name}*********")
        return response
    
    def create_functional_specification(self, orchestrate):
        logger.info(f"[{self.name}] Create Functional Specification")
        if orchestrate == "sequential":
            # all_topics = load_yaml_file(f"..\\prompts_template\\agent_fs_prompts_list.yaml") 
            all_topics = load_yaml_file(f"..\\prompts_template\\agent_fs_sas_prompts_list.yaml") 
            # all_topics = load_yaml_file(f"..\\prompts_template\\agent_fs_pyspark_prompts_list.yaml") 
            topics=None
            #TODO
            #program_type = "non_batch_programs_cbl"
            # program_type = "batch_programs"

            program_type = "sas_programs"
            logger.info(f"topics:{topics}")

            if program_type == "sas_programs":
                topics= all_topics.get("sas_programs", [])

            # program_type = "pyspark_programs"
            # logger.info(f"topics:{topics}")

            # if program_type == "pyspark_programs":
            #     topics= all_topics.get("pyspark_programs", [])
            
            # if program_type == "batch_programs":
            #     topics= all_topics.get("batch_programs", [])
            # elif program_type == "non_batch_programs":
            #     topics= all_topics.get("non_batch_programs", [])
            # elif program_type == "non_batch_programs_cbl":
            #     topics= all_topics.get("non_batch_programs_cbl", [])
            
            
            self.functional_specification = ""
            # print("✅ Topics loaded:", topics)
            for item in topics:
                title = item.get("title", "Untitled")
                topic = item.get("topic")

                if topic:
                    logger.info(f"Processing topic: {topic}")
                    content = self.extract_prompt_and_execute(topic).content
                    self.functional_specification += f"\n# {title}\n{content}"
                else:
                    logger.error(f"Warning: Topic missing from YAML entry: {item}")
            # print("✅ Final spec content:", self.functional_specification)

        return self.functional_specification
   
