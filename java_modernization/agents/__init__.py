
from .functional_spec_generator_agent import FunctionalSpecGeneratorAgent
from .functional_spec_consolidator_agent import FunctionalSpecsConsolidatorAgent

class ReverseEngineeringAgentManager:
    def __init__(self, max_retries=2, verbose=True):
        llm_provider="google"
        self.agents = {
            "generate_functional_spec": FunctionalSpecGeneratorAgent(provider=llm_provider, model="default", max_retries=max_retries, verbose=verbose),
            "consolidate_functional_specs": FunctionalSpecsConsolidatorAgent(provider=llm_provider, model="default", max_retries=max_retries, verbose=verbose),
        }

    def get_agent(self, agent_name):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        return agent