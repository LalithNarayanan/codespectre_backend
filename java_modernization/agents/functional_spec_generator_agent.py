# agents/functional_spec_generator_agent.py

from .agent_base import AgentBase
from loguru import logger
from utils.yaml_load import load_yaml_file
import time


#To generate the functional specification from the Code
class FunctionalSpecGeneratorAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="FunctionalSpecGeneratorAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)
        self.functional_specification: str = None
        self.code: str = None
        self.template_key: str = None
        self.placeholders: object = None

    def execute(self,code,section_type):
        print(f"execute...fs_agent..!!.")
        self.code = code
        # self.placeholders = self.contexts.copy()
        self.placeholders={}
        self.placeholders['code']=self.code
        logger.info(f"placeholders:>>>{self.placeholders}")
        ############################
        # print(f"context:>>>> {contexts}")
        keys_with_values = ['code']
        # for key, value in self.contexts.items():
        #     if value:  # Checks for truthiness (not None, not empty string/list/dict, not 0, not False)
        #         keys_with_values.append(key)
        print(f"{keys_with_values}") 
        #Including code and all contexts
        self.template_key=keys_with_values
        ############################
        summary = self.create_functional_specification(section_type)
        return summary

    def are_representations_equal(self,str_repr, list_repr):
        list_from_string = str_repr.split(',')
        list_from_string = [item.strip() for item in list_from_string]
        flag = sorted(list_from_string) == sorted(list_repr)
        print(f"flag:>>>>>>>>{flag}")
        return flag
    
    #Extract user message and system message for the given system
    def extract_prompt(self,section_name):
        prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_javaspring_prompts.yaml") 
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
                logger.info(f"***************************user_message:>>>>> {selected_version["user_message"]}")
                return selected_version
            else:
                logger.info("Version  not found.")
            return selected_version
            
        else:
            logger.error(f"Prompt name=> {section_name} with version information not found.")
            return None

    #Extract prompt and execute
    def extract_prompt_and_execute(self,section_type):
        logger.info(f"\n extract_prompt_and_execute section_type:***********{section_type}*********")
        start_time = time.time()
        prompts=self.extract_prompt(section_type)
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
            response = self.call_model(messages, max_tokens=130000)
            response_content=response.content
        else:
            response = f"Unable to fetch prompt extract_programoverview"
        end_time = time.time()
        overall_processing_time = end_time - start_time
        llm_processing_time= end_time - llm_start_time
        return response
    
    def create_functional_specification(self, section_type):
        logger.info(f"Processing section_type: {section_type}")
        content = self.extract_prompt_and_execute(section_type).content
        return content
   
