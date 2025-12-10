# agents/oo_designer.py

from .agent_base import AgentBase
from utils.yaml_load import load_yaml_file
from loguru import logger

class MermaidDiagramGeneratorAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="MermaidDiagramGeneratorAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)

    def execute(self, diagram_type, data_for_diagram):
        print(f"Executing {self.name} agent...")
        prompts = load_yaml_file(f"..\\prompts_template\\agent_mermaid_diagrams_prompts.yaml") 
        category = "mermaid_diagrams"

        diagram_type = "class_diagram"
        user_message=None
        system_message=None
        if category in prompts and "versions" in prompts[category]:
            versions = prompts[category]["versions"]
            selected_version = None
            for version_data in versions:
                if version_data["version"] == diagram_type:
                    selected_version = version_data
                    break  # Stop searching once version 1.0 is found
            if selected_version:
                logger.debug(f"system_message: {selected_version["system_message"]}")
                user_message=selected_version["user_message"]
                system_message=selected_version["system_message"]
                user_message = user_message.format(
                    data_for_diagram=data_for_diagram,
                    )
            else:
                logger.info("Version {diagram_type} not found.")
                return f"Unable to retrieve prompt version {diagram_type}"
        
        if user_message is None or system_message is None:
            return f"Unable to retrieve prompt {diagram_type}"
        
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

        