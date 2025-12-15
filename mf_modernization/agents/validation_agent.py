# agents/validation_agent.py

from .agent_base import AgentBase
from loguru import logger
from utils.file_util import save_to_file, write_job_data_to_csv
from typing import Dict, Any
from config import load_config
import time
from pathlib import Path

UNIVERSAL_VALIDATION_PROMPT = """
You are a senior migration and validation engineer.

Your task: compare SOURCE CODE vs FUNCTIONAL SPECIFICATION and validate whether the spec correctly and completely describes the behavior of the code.

Return:
- Overall accuracy and completeness assessment
- Key correct points
- Missing or incorrect behaviors
- Suggestions to improve the spec

Use clear, concise markdown. Do not include the original full code or spec, only your analysis.
""".strip()


class ValidationAgent(AgentBase):
    def __init__(self, provider: str = "ollama", model: str = "llama3.2",
                 max_retries: int = 3, verbose: bool = True):
        super().__init__(
            name="ValidationAgent",
            provider=provider,
            model=model,
            max_retries=max_retries,
            verbose=verbose,
        )
        self.job_id: str | None = None
        self.record_id: str | None = None
        self.base_dir: str | None = None
        self.source_code: str | None = None
        self.functional_spec: str | None = None
        self.platform: str | None = None
        self.config = load_config()

    def execute(
        self,
        job_id: str,
        record_id: str,
        base_dir: str,
        source_code: str,
        functional_spec: str,
        platform: str = "mainframe",
        orchestrate: str = "single",
    ) -> Any:
        """
        Main entry point, similar to FunctionalSpecGeneratorAgent.execute.
        """
        self.job_id = job_id
        self.record_id = record_id
        self.base_dir = base_dir
        self.source_code = source_code
        self.functional_spec = functional_spec
        self.platform = platform.lower()

        logger.info(f"[{self.name}] [{self.platform.upper()}] "
                    f"Starting validation for record_id={record_id}")
        return self.run_validation()

    def build_prompt(self) -> Dict[str, str]:
        system_message = UNIVERSAL_VALIDATION_PROMPT

        platform_context = {
            "mainframe": "COBOL programs",
            "sas": "SAS programs and macros",
            "java": "Java classes and methods",
        }
        code_type = platform_context.get(self.platform, "source code")

        user_message = f"""
You are validating a generated functional specification against the original {code_type}.

SOURCE CODE ({code_type}, concatenated with file headers):

{{source_code}}

GENERATED FUNCTIONAL SPECIFICATION (Markdown):

{{functional_spec}}

Please provide:

1. **Overall Assessment**
   - Short summary of how accurate and complete the functional spec is.

2. **Correct Coverage**
   - Bullet list of important behaviors or modules that are correctly described.

3. **Missing or Incorrect Points**
   - Bullet list of:
     - Code behaviors present in source but missing in spec.
     - Parts where the spec is clearly inaccurate or misleading.

4. **Completeness / Accuracy Scores**
   - Completeness score (0–100) – how much of the important behavior is covered.
   - Accuracy score (0–100) – how correct the described behavior is.

5. **Detailed Findings**
   - For each module/function/macro in the source code, indicate whether it is:
     - Correctly described.
     - Missing or incorrectly described in the functional specification.
     - Use source as reference and then check against the functional specification.

6. **Actionable Suggestions**
   - Bullet list of concrete improvements to the functional specification.

Return everything as clean markdown, no JSON, no code blocks with the full original source.
""".strip()

        formatted_user_message = user_message.format(
            source_code=self.source_code or "",
            functional_spec=self.functional_spec or "",
        )

        return {
            "system_message": system_message,
            "user_message": formatted_user_message,
        }

    def run_validation(self) -> Any:
        start_time = time.time()
        prompt = self.build_prompt()

        messages = [
            {"role": "system", "content": prompt["system_message"]},
            {"role": "user", "content": prompt["user_message"]},
        ]

        llm_start_time = time.time()
        response = self.call_model(messages, max_tokens=8000)
        llm_end_time = time.time()

        response_content = response.content
        end_time = time.time()

        overall_processing_time = end_time - start_time
        llm_processing_time = llm_end_time - llm_start_time

        # Platform-aware output dir, consistent with FS agent
        output_dir = Path(self.config["get_output_dir"](self.platform))
        output_dir.mkdir(parents=True, exist_ok=True)

        file_name = output_dir / f"{self.record_id}_validation.md"
        save_to_file(str(file_name), response_content)
        logger.info(
            f"[{self.name}] [{self.platform.upper()}] "
            f"Validation markdown saved at {file_name}"
        )

        job_info = {
            "job_id": self.job_id,
            "platform": self.platform,
            "llm_model_name": self.model,
            "llm_processing_time": llm_processing_time,
            "overall_processing_time": overall_processing_time,
            "prompt_name": f"validation_{self.platform}_fs",
            "prompt_template": "inline_validation_prompt",
            "unit": self.record_id,
            "input": "source_code + functional_spec",
            "output_type": "validation_report",
            "output_file": str(file_name),
        }

        job_csv_file_name = output_dir / "job_details.csv"
        write_job_data_to_csv(job_data=job_info, file_name=str(job_csv_file_name))
        logger.info(
            f"[{self.name}] [{self.platform.upper()}] "
            f"Job updated in {job_csv_file_name}"
        )

        return response


def validate_with_llm(
    job_id: str,
    record_id: str,
    base_dir: str,
    source_code: str,
    functional_spec: str,
    platform: str = "mainframe",
) -> Dict:
    """
    Convenience wrapper to call ValidationAgent.
    """
    agent = ValidationAgent()
    return agent.execute(
        job_id=job_id,
        record_id=record_id,
        base_dir=base_dir,
        source_code=source_code,
        functional_spec=functional_spec,
        platform=platform,
    )
