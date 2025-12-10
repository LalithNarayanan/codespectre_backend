# agents/functional_spec_generator_agent.py

from .agent_base import AgentBase
from loguru import logger
from utils.yaml_load import load_yaml_file, load_topics
from utils.file_util import save_to_file,write_job_data_to_csv
import time
#To generate the functional specification from the Code
class FunctionalSpecsConsolidatorAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="FunctionalSpecsConsolidatorAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)
        self.functional_specification: str = None
        self.functional_specs: str = None
        self.job_id: str =None
        self.base_dir: str =None
        self.template_key: str =None
        self.placeholders: object = None
        self.sections: str = None
        self.contexts: object = None
        

    def are_representations_equal(self,str_repr, list_repr):
        list_from_string = str_repr.split(',')
        list_from_string = [item.strip() for item in list_from_string]
        flag = sorted(list_from_string) == sorted(list_repr)
        print(f"flag:>>>>>>>>{flag}")
        return flag

    def extract_prompt(self,section_name):
        prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_cbl_prompts.yaml") 
        category = "code2functionalspec"
        if category in prompts and section_name in prompts[category] and "versions" in prompts[category][section_name]:
            versions = prompts[category][section_name]["versions"]
            selected_version = None
            for version_data in versions:
                # logger.info(f"version=>>: {version_data["version"]}")
                foundFlag =  self.are_representations_equal(version_data["version"], self.template_key)
                if foundFlag:
                    selected_version = version_data
                    break  # Stop searching once version 1.0 is found
             #Go for default           
            if selected_version is None:
                for version_data in versions:
                    if version_data["version"]=='functional_specs':
                        selected_version=version_data
                        break
            if selected_version:
                logger.info(f"system_message: {selected_version["system_message"]}")
                logger.info(f"***************************user_message:>>>>> {selected_version["user_message"]}")
                return selected_version
            else:
                logger.info("Version  not found.")
            return selected_version
            
        else:
            logger.error(f"Prompt name=> {section_name} with version information not found.")
            return None


    #Consolidating Functional Specs..
    def execute(self, job_id, base_dir, functional_specs, contexts=None, section=None):
            logger.info(f"Executing ==>>> {self.name} agent...")
            start_time = time.time()
            self.base_dir=base_dir
            self.job_id=job_id
            self.functional_specs=functional_specs
            self.contexts=contexts
            self.section=section
            #Get the unique to search the prompt
            keys_with_values = ['functional_specs','section']
            for key, value in self.contexts.items():
                if value:  
                    keys_with_values.append(key)
            print(f"{keys_with_values}") 
            #Including functional_spec and all contexts
            self.template_key=keys_with_values
            self.placeholders = self.contexts.copy()
            self.placeholders['functional_specs']=self.functional_specs
            self.placeholders['section']=self.section
            prompt_name="merge_functional_specs"
            prompts=self.extract_prompt(prompt_name)
            logger.info(f"\n\nn\ merge prompts:>>>>{prompts} ****************\n\n\n")
            response_content=""
            prompt_template=""
            if prompts:
                system_message = prompts["system_message"]
                user_message = prompts["user_message"]
                prompt_template=prompts["user_message"]
                try:
                    formatted_user_message=user_message.format(
                    **self.placeholders)
                except KeyError as e:
                    print(f"Warning: Could not replace placeholder '{e}' in the message. Key not found in data.")
                    formatted_user_message=user_message

                logger.info(f"self.placeholders>>>>:{self.placeholders}")
                logger.info(f"formatted_user_message>>>>:{formatted_user_message}")
                messages = [
                    { "role": "system", "content": system_message },
                    { "role": "user", "content": formatted_user_message } ]
                llm_start_time = time.time()
                response = self.call_model(messages, max_tokens=130000)
                response_content=response.content
            else:
                response = f"Unable to fetch prompt extract_programoverview"
            
            file_name_temp=rf"{self.base_dir}\output\{self.job_id}_consolidated_functional_specificaitons.md"
            file_name=rf"{self.base_dir}\output\consolidated_functional_specificaitons.md"
            save_to_file(file_name_temp,response_content)
            save_to_file(file_name,response_content)
            logger.info(f"\n********* {file_name} is saved at {file_name}  **************")
            end_time = time.time()
            overall_processing_time = end_time - start_time
            llm_processing_time= end_time - llm_start_time
    
            #save the response;
            job_info = {
            'job_id': self.job_id,
            'llm_model_name': self.model,
            'llm_processing_time': llm_processing_time,  
            'overall_processing_time': overall_processing_time,
            'prompt_name': prompt_name,
            'prompt_template': prompt_template,
            'input': "Functional Specs...",
            'output_type': "functional_consolidation",
            'output_file': "consolidated_functional_specificaitons.md",
            }

            job_csv_file_name=rf"{self.base_dir}\output\job_details.csv"
            write_job_data_to_csv(job_data=job_info, file_name=job_csv_file_name)
            logger.info(f"{job_csv_file_name} is updated...")

            return response

    
