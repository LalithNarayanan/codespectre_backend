# agents/oo_designer.py

from .agent_base import AgentBase
from utils.yaml_load import load_yaml_file
from loguru import logger

class ObjectOrientedCoderAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="ObjectOrientedCoderAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)

    def execute(self, oo_design,context=None, functional_spec=None,language="python"):
        print(f"Executing {self.name} agent...")
        prompts = load_yaml_file(f"..\\prompts_template\\agent_code_prompts.yaml") 
        category = "design2code"
        user_message=None
        system_message=None
        # if context is None:
        #      section_name = "java_new"

        if category in prompts and "versions" in prompts[category]:
            versions = prompts[category]["versions"]
            selected_version = None
            for version_data in versions:
                if version_data["version"] == language:
                    selected_version = version_data
                    break  # Stop searching once version 1.0 is found
            if selected_version:
                logger.debug(f"system_message: {selected_version["system_message"]}")
                user_message=selected_version["user_message"]
                system_message=selected_version["system_message"]

                if context is None:
                    user_message = user_message.format(
                        functional_spec=functional_spec,
                        oo_design=oo_design)
                else:
                    user_message = user_message.format(
                        functional_spec=functional_spec,
                        oo_design=oo_design,
                        context=context)
            else:
                logger.info("Version '1.0' not found.")
                return f"Unable to retrieve prompt  version 1.0"
        
        if user_message is None or system_message is None:
            return f"Unable to retrieve prompt"
        
        logger.info(f"\n\n ***** \nCODING...user_message: {user_message} end*****\n\n")

        # Create an object oriented design from the detailed functional specification.
        messages = [
            {
                "role": "system", 
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        summary = self.call_model(messages, max_tokens=130000)
        return summary

        