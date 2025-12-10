# agents/oo_designer.py

from .agent_base import AgentBase
from utils.yaml_load import load_yaml_file
from loguru import logger

class ObjectOrientedDesignerAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="ObjectOrientedDesignerAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)

    def execute(self, functional_spec,context=None):
        print(f"Executing {self.name} agent...")
        prompts = load_yaml_file(f"..\\prompts_template\\agent_oodesign_prompts.yaml") 
        category = "functionalspec2design"
        section_name = "oo_design_update"
        user_message=None
        system_message=None
        if context is None:
             section_name = "oo_design_new"

        if category in prompts and section_name in prompts[category] and "versions" in prompts[category][section_name]:
            versions = prompts[category][section_name]["versions"]
            selected_version = None
            for version_data in versions:
                if version_data["version"] == "1.0":
                    selected_version = version_data
                    break  # Stop searching once version 1.0 is found
            if selected_version:
                logger.debug(f"system_message: {selected_version["system_message"]}")
                user_message=selected_version["user_message"]
                system_message=selected_version["system_message"]

                if context is None:
                    user_message = user_message.format(
                        functional_spec=functional_spec)
                else:
                    user_message = user_message.format(
                        functional_spec=functional_spec,
                        context=context)
                
            else:
                logger.info("Version '1.0' not found.")
                return f"Unable to retrieve prompt {section_name} version 1.0"
        
        if user_message is None or system_message is None:
            return f"Unable to retrieve prompt {section_name}"

        # print(f"formatted_user_message:{user_message}")
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