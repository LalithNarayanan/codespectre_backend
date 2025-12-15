# agents/functional_spec_generator_agent.py

from .agent_base import AgentBase
from loguru import logger
from utils.yaml_load import load_yaml_file, load_topics
from utils.file_util import save_to_file, write_job_data_to_csv
from config import load_config
from pathlib import Path
import time

UNIVERSAL_MARKDOWN_PROMPT = """
For all sections, format your answer exclusively using markdown syntax. Use appropriate markdown elements such as headings, subheadings, bullet points, numbered lists, code blocks, and tables to enhance readability and organization of the content.
Follow same and best practice(s) in markdown formatting.
Don't include tables, nor code snippets unless specifically requested.
"""

PLATFORM_PROMPT_TEMPLATES = {
    "mainframe": {
        "prompts_versioned": "agent_fs_cbl_prompts_versioned.yaml",
        "prompts_list": "agent_fs_cbl_prompts_list.yaml"
    },
    "sas": {
        "prompts_versioned": "agent_fs_sas_prompts_versioned.yaml",
        "prompts_list": "agent_fs_sas_prompts_list.yaml"
    },
    "java": {
        "prompts_versioned": "agent_fs_java_prompts_versioned.yaml",
        "prompts_list": "agent_fs_java_prompts_list.yaml"
    }
}

class FunctionalSpecGeneratorAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
        super().__init__(name="FunctionalSpecGeneratorAgent", provider=provider, model=model, max_retries=max_retries, verbose=verbose)
        self.functional_specification: str = None
        self.code: str = None
        self.job_id: str = None
        self.record_id: str = None
        self.contexts: object = None
        self.base_dir: str = None
        self.programs: str = None
        self.template_key: str = None
        self.placeholders: object = None
        self.platform: str = None
        self.program_type: str = None
        self.config = load_config()

    def execute(self, job_id, record_id, base_dir, code, contexts, programs, 
                platform="mainframe", program_type=None, orchestrate="sequential"):
        """
        Execute functional spec generation
        
        Args:
            job_id: Job identifier
            record_id: Record/logical unit identifier
            base_dir: Base directory (usually ".")
            code: Source code to analyze
            contexts: Context information (dict)
            programs: List of program files
            platform: Target platform (mainframe/sas/java)
            program_type: Type of programs (batch_programs/sas_programs/java_programs)
            orchestrate: Orchestration mode (sequential/parallel)
        """
        self.job_id = job_id
        self.record_id = record_id
        self.code = code
        self.contexts = contexts
        self.base_dir = base_dir
        self.programs = programs
        self.platform = platform.lower()
        self.program_type = program_type
        
        # Setup placeholders
        self.placeholders = self.contexts.copy()
        self.placeholders['code'] = self.code
        logger.info(f"[{self.platform.upper()}] Placeholders: {list(self.placeholders.keys())}")
        
        # Determine template keys
        keys_with_values = ['code']
        for key, value in self.contexts.items():
            if value:
                keys_with_values.append(key)
        self.template_key = keys_with_values
        
        # Generate specification
        summary = self.create_functional_specification(orchestrate)
        return summary

    def are_representations_equal(self, str_repr, list_repr):
        list_from_string = str_repr.split(',')
        list_from_string = [item.strip() for item in list_from_string]
        flag = sorted(list_from_string) == sorted(list_repr)
        return flag
    
    def extract_prompt(self, section_name):
        """Extract prompt for section using platform-specific template"""
        
        if self.platform not in PLATFORM_PROMPT_TEMPLATES:
            logger.error(f"Unknown platform: {self.platform}")
            return None
        
        prompt_file = PLATFORM_PROMPT_TEMPLATES[self.platform]["prompts_versioned"]
        prompts = load_yaml_file(f"..\\prompts_template\\{prompt_file}")
        logger.info(f"[{self.platform.upper()}] Loading prompts from: {prompt_file}")
        
        category = "code2functionalspec"
        if category in prompts and section_name in prompts[category] and "versions" in prompts[category][section_name]:
            versions = prompts[category][section_name]["versions"]
            selected_version = None
            
            for version_data in versions:
                logger.info(f"Checking version: {version_data['version']}")
                foundFlag = self.are_representations_equal(version_data["version"], self.template_key)
                if foundFlag:
                    selected_version = version_data
                    break
            
            if selected_version is None:
                for version_data in versions:
                    if version_data["version"] == 'code':
                        selected_version = version_data
                        break
            
            if selected_version:
                logger.info(f"System message: {selected_version['system_message'][:100]}...")
                selected_version['user_message'] = (
                    UNIVERSAL_MARKDOWN_PROMPT.strip() + "\n\n" + selected_version['user_message'].strip()
                )
                return selected_version
            else:
                logger.warning("No matching version found")
                return None
        else:
            logger.error(f"Prompt '{section_name}' not found in {prompt_file}")
            return None

    def extract_prompt_and_execute(self, topic):
        """Extract prompt and execute LLM call for topic"""
        logger.info(f"\n[{self.platform.upper()}] Processing topic: {topic}")
        start_time = time.time()
        
        prompts = self.extract_prompt(topic)
        if not prompts:
            logger.error(f"Unable to fetch prompt for {topic}")
            return type('obj', (object,), {'content': f"Error: Unable to fetch prompt for {topic}"})()
        
        system_message = prompts["system_message"]
        user_message = prompts["user_message"]
        prompt_template = prompts["user_message"]
        
        try:
            formatted_user_message = user_message.format(**self.placeholders)
        except KeyError as e:
            logger.warning(f"Could not replace placeholder '{e}' in message")
            formatted_user_message = user_message
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": formatted_user_message}
        ]
        llm_start_time = time.time()
        response = self.call_model(messages, max_tokens=650000)
        response_content = response.content
        
        end_time = time.time()
        overall_processing_time = end_time - start_time
        llm_processing_time = end_time - llm_start_time
        
        output_dir = Path(self.config['get_output_dir'](self.platform))
        intermediary_dir = output_dir / "intermediary" / self.record_id
        intermediary_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = intermediary_dir / f"{self.job_id}_{self.record_id}_{topic}.md"
        save_to_file(str(file_name), response_content)
        logger.info(f"[{self.platform.upper()}] Saved intermediary: {file_name}")
        
        job_info = {
            'job_id': self.job_id,
            'platform': self.platform,
            'llm_model_name': self.model,
            'llm_processing_time': llm_processing_time,
            'overall_processing_time': overall_processing_time,
            'prompt_name': topic,
            'prompt_template': prompt_template[:100],
            'unit': self.record_id,
            'input': str(self.programs),
            'output_type': "func_spec_intermediary",
            'output_file': str(file_name),
        }
        
        job_csv_file_name = output_dir / "job_details.csv"
        write_job_data_to_csv(job_data=job_info, file_name=str(job_csv_file_name))
        logger.info(f"Job info updated: {job_csv_file_name}")
        
        return response
    
    def create_functional_specification(self, orchestrate):
        """Create complete functional specification by processing all topics"""
        logger.info(f"[{self.name}] Creating functional specification for {self.platform.upper()}")
        
        if orchestrate == "sequential":
            if self.platform not in PLATFORM_PROMPT_TEMPLATES:
                logger.error(f"Unknown platform: {self.platform}")
                return ""
            
            topics_file = PLATFORM_PROMPT_TEMPLATES[self.platform]["prompts_list"]
            all_topics = load_yaml_file(f"..\\prompts_template\\{topics_file}")
            logger.info(f"[{self.platform.upper()}] Loading topics from: {topics_file}")
            
            # ✅ IMPROVED: Use passed program_type with intelligent fallback
            if self.program_type:
                logger.info(f"[{self.platform.upper()}] Using provided program_type: {self.program_type}")
                topics = all_topics.get(self.program_type, [])
            else:
                logger.warning(f"[{self.platform.upper()}] No program_type provided, attempting auto-detection")
                topics = self._auto_detect_topics(all_topics)
            
            # ✅ FALLBACK: If still no topics found
            if not topics:
                logger.warning(f"[{self.platform.upper()}] No topics found for program_type: {self.program_type}")
                logger.info(f"[{self.platform.upper()}] Trying fallback lookup...")
                topics = self._fallback_topic_lookup(all_topics)
            
            if not topics:
                logger.error(f"[{self.platform.upper()}] No topics found after all attempts!")
                logger.error(f"Available keys in YAML: {list(all_topics.keys())}")
                return ""
            
            logger.info(f"[{self.platform.upper()}] Processing {len(topics)} topics")
            
            self.functional_specification = ""
            for item in topics:
                title = item.get("title", "Untitled")
                topic = item.get("topic")
                
                if topic:
                    logger.info(f"[{self.platform.upper()}] Processing topic: {topic}")
                    content = self.extract_prompt_and_execute(topic).content
                    self.functional_specification += f"\n# {title}\n{content}"
                else:
                    logger.error(f"Warning: Topic missing from YAML entry: {item}")
            
            logger.info(f"[{self.platform.upper()}] Functional specification complete, length: {len(self.functional_specification)}")
        
        return self.functional_specification
    
    def _auto_detect_topics(self, all_topics):
        """Auto-detect which topic list to use from available keys"""
        platform_key = f"{self.platform}_programs"
        if platform_key in all_topics:
            logger.info(f"Auto-detected topic key: {platform_key}")
            return all_topics[platform_key]
        
        for key in all_topics.keys():
            logger.info(f"Found available key: {key}, using it")
            return all_topics[key]
        
        return []
    
    def _fallback_topic_lookup(self, all_topics):
        """Fallback logic to find topics when primary lookup fails"""
        fallback_keys = {
            "mainframe": ["batch_programs", "non_batch_programs", "mainframe_programs"],
            "sas": ["sas_programs", "batch_programs"],
            "java": ["java_programs", "batch_programs"]
        }
        
        for key in fallback_keys.get(self.platform, []):
            if key in all_topics:
                logger.info(f"Found topics using fallback key: {key}")
                return all_topics[key]
        
        if all_topics:
            first_key = list(all_topics.keys())[0]
            logger.warning(f"Using first available key as last resort: {first_key}")
            return all_topics[first_key]
        
        return []
