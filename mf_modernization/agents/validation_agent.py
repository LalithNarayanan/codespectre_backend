# agents/validation_agent.py

from .agent_base import AgentBase
from loguru import logger
from utils.yaml_load import load_yaml_file
from utils.file_util import save_to_file, write_job_data_to_csv
from typing import Dict, Any
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
"""

class ValidationAgent(AgentBase):
    def __init__(self, provider="ollama", model="llama3.2", max_retries=3, verbose=True):
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

    def execute(
        self,
        job_id: str,
        record_id: str,
        base_dir: str,
        source_code: str,
        functional_spec: str,
        orchestrate: str = "single",
    ) -> Any:
        """
        Main entry point, same pattern as FunctionalSpecGeneratorAgent.execute.
        """
        self.job_id = job_id
        self.record_id = record_id
        self.base_dir = base_dir
        self.source_code = source_code
        self.functional_spec = functional_spec

        logger.info(f"[{self.name}] Starting validation for record_id={record_id}")
        result = self.run_validation()
        return result

    def build_prompt(self) -> Dict[str, str]:
        """
        Build system + user messages. You can later move this to YAML like the FS agent.
        """
        system_message = UNIVERSAL_VALIDATION_PROMPT.strip()

        user_message = """
You are validating a generated functional specification against the original SAS source code.

SOURCE CODE (SAS programs + macros, concatenated with file headers):

{source_code}

GENERATED FUNCTIONAL SPECIFICATION (Markdown):

{functional_spec}

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
   - For each macros and similar methods/modules in the source code, indicate whether it is:
     - Correctly described
     - Coorectly mention if it is missing or incorrect in the functional specification.
     - Use source code as reference and then check against functional specification.

6. **Actionable Suggestions**
   - Bullet list of concrete improvements to the functional specification.

Return everything as clean markdown, no JSON, no code blocks with the full original source.
""".strip()

        # Format with actual content
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

        response_content = response.content  # same pattern as FS agent
        end_time = time.time()

        overall_processing_time = end_time - start_time
        llm_processing_time = llm_end_time - llm_start_time

        # Save validation markdown next to other outputs
        # file_name = rf"{self.base_dir}\output\{self.job_id}_{self.record_id}_validation.md"
        file_name = rf"C:\Users\YendetiLalith\Documents\CodeSpectre\MainframeApplications\LTCHPPSPricerMFApp2021\output\sas_specifications\{self.record_id}_validation.md"
        save_to_file(file_name, response_content)
        logger.info(f"[{self.name}] Validation markdown saved at {file_name}")

        # Log job info
        job_info = {
            "job_id": self.job_id,
            "llm_model_name": self.model,
            "llm_processing_time": llm_processing_time,
            "overall_processing_time": overall_processing_time,
            "prompt_name": "validation_sas_fs",
            "prompt_template": "inline_validation_prompt",
            "unit": self.record_id,
            "input": "source_code + functional_spec",
            "output_type": "validation_report",
            "output_file": file_name,
        }
        job_csv_file_name = rf"{self.base_dir}\output\job_details.csv"
        write_job_data_to_csv(job_data=job_info, file_name=job_csv_file_name)
        logger.info(f"[{self.name}] Job updated in {job_csv_file_name}")

        return response

# Helper function for main.py
def validate_with_llm(record_id: str, source_code: str, functional_spec: str) -> Dict:
    """
    Wrapper function to call validation agent.
    """
    agent = ValidationAgent()
    return agent.execute(record_id, source_code, functional_spec)





































# # Create a new file: agents/validation_agent.py

# import requests
# from typing import Dict, List
# import json
# import re
# from dotenv import load_dotenv
# import os

# load_dotenv()

# class ValidationAgent:
#     """
#     Agent that uses LLM to validate functional specifications
#     against source code.
#     """
    
#     def __init__(self):
#         self.api_key = os.getenv("GOOGLE_API_KEY")
#         self.base_url = os.getenv("GOOGLE_BASE_URL")
#         if not self.api_key:
#             raise ValueError("GOOGLE_API_KEY not set in environment or .env file.")
#         if not self.base_url:
#             raise ValueError("GOOGLE_BASE_URL not set in environment or .env file.")
    
#     def validate(
#         self,
#         record_id: str,
#         source_code: str,
#         functional_spec: str
#     ) -> Dict:
#         """
#         Validate functional spec against source code using LLM.
#         """
        
#         prompt = self._build_validation_prompt(source_code, functional_spec)
        
#         # Google Generative Language API expects a POST to /models/{model}:generateContent
#         # We'll use the model 'gemini-pro' (or as required)
#         url = f"{self.base_url}models/gemini-pro:generateContent?key={self.api_key}"
#         headers = {"Content-Type": "application/json"}
#         payload = {
#             "contents": [{"parts": [{"text": prompt}]}],
#             "generationConfig": {"maxOutputTokens": 2048}
#         }
#         resp = requests.post(url, headers=headers, json=payload)
#         if not resp.ok:
#             raise RuntimeError(f"Google API error: {resp.status_code} {resp.text}")
#         data = resp.json()
#         # Extract the text response
#         result_text = ""
#         try:
#             result_text = data["candidates"][0]["content"]["parts"][0]["text"]
#         except Exception:
#             result_text = str(data)
#         # Parse LLM response
#         validation_result = self._parse_validation_response(result_text)
#         validation_result['record_id'] = record_id
#         return validation_result
    
#     def _build_validation_prompt(self, source_code: str, functional_spec: str) -> str:
#         return f"""You are a validation expert. Compare the SOURCE CODE with the GENERATED FUNCTIONAL SPECIFICATION and provide a detailed validation report.

# SOURCE CODE:
# {source_code[:50000]}  # Limit to avoid token limits

# GENERATED FUNCTIONAL SPECIFICATION:
# {functional_spec[:30000]}

# Your task:
# 1. Verify that all major components in the source code are documented in the functional spec
# 2. Check if business logic is accurately described
# 3. Validate data flow descriptions
# 4. Identify missing or incorrect information
# 5. Assess overall completeness and accuracy

# Provide your response in the following JSON format:

# {{
#   "validation_score": <number 0-100>,
#   "accuracy_rating": "<Excellent|Good|Fair|Poor>",
#   "findings": {{
#     "correct_items": [<list of correctly documented items>],
#     "missing_items": [<list of missing items>],
#     "incorrect_items": [<list of incorrectly documented items>],
#     "incomplete_items": [<list of incomplete descriptions>]
#   }},
#   "suggestions": [<list of improvement suggestions>],
#   "summary": "<brief overall assessment>"
# }}

# SCORING GUIDELINES:
# - 90-100: Excellent - Comprehensive, accurate, complete
# - 75-89: Good - Mostly accurate with minor gaps
# - 60-74: Fair - Significant gaps or inaccuracies
# - 0-59: Poor - Major gaps or critical inaccuracies

# Be thorough and specific in your findings."""

#     def _parse_validation_response(self, response_text: str) -> Dict:
#         """
#         Parse LLM response into structured validation result.
#         """
#         try:
#             # Try to extract JSON from response
#             json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
#             if json_match:
#                 result = json.loads(json_match.group())
#                 return result
#             else:
#                 # Fallback if JSON not found
#                 return {
#                     "validation_score": 0,
#                     "accuracy_rating": "Unknown",
#                     "findings": {
#                         "correct_items": [],
#                         "missing_items": ["Failed to parse validation results"],
#                         "incorrect_items": [],
#                         "incomplete_items": []
#                     },
#                     "suggestions": ["Please review manually"],
#                     "summary": response_text[:500]
#                 }
#         except json.JSONDecodeError:
#             return {
#                 "validation_score": 0,
#                 "accuracy_rating": "Error",
#                 "findings": {
#                     "correct_items": [],
#                     "missing_items": ["JSON parsing failed"],
#                     "incorrect_items": [],
#                     "incomplete_items": []
#                 },
#                 "suggestions": ["Manual review required"],
#                 "summary": response_text[:500]
#             }



