# agents/validation_agent.py

from .agent_base import AgentBase
from .simple_chunker import SimpleChunker
from loguru import logger
from utils.file_util import save_to_file, write_job_data_to_csv
from typing import Dict, Any, Optional
from config import load_config
import time
from pathlib import Path
import re


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
                 max_retries: int = 3, verbose: bool = True, chunker=None,
                 min_accuracy_score: int = 75):  # ✅ NEW: Configurable accuracy threshold
        super().__init__(
            name="ValidationAgent",
            provider=provider,
            model=model,
            max_retries=max_retries,
            verbose=verbose,
        )
        
        # Chunker setup
        if chunker:
            self.chunker = chunker
        else:
            max_tokens = 6000 if provider == "gemma12b" else 100000
            self.chunker = SimpleChunker(max_tokens=max_tokens)
        
        self.job_id: str | None = None
        self.record_id: str | None = None
        self.base_dir: str | None = None
        self.source_code: str | None = None
        self.functional_spec: str | None = None
        self.platform: str | None = None
        self.config = load_config()
        
        # ✅ NEW: Retry configuration
        self.min_accuracy_score = min_accuracy_score
        self.max_validation_attempts = 3
        self.validation_attempts = []  # Store all attempts

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
        Main entry point with retry logic based on accuracy scores.
        """
        self.job_id = job_id
        self.record_id = record_id
        self.base_dir = base_dir
        self.source_code = source_code
        self.functional_spec = functional_spec
        self.platform = platform.lower()
        self.validation_attempts = []  # Reset attempts for this execution

        logger.info(f"[{self.name}] [{self.platform.upper()}] "
                    f"Starting validation for record_id={record_id}")
        logger.info(f"[{self.name}] Minimum accuracy threshold: {self.min_accuracy_score}%")
        
        # Check if chunking needed
        combined_content = f"{source_code}\n\n{functional_spec}"
        chunks = self.chunker.chunk_code(combined_content)
        
        logger.info(f"[{self.name}] [{self.platform.upper()}] "
                    f"Validation content split into {len(chunks)} chunk(s)")
        for chunk in chunks:
            logger.info(f"  Chunk {chunk['chunk_id']}: {chunk['tokens']:,} tokens")
        
        # ✅ NEW: Retry loop with accuracy check
        for attempt in range(1, self.max_validation_attempts + 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"[{self.name}] 🔄 VALIDATION ATTEMPT {attempt}/{self.max_validation_attempts}")
            logger.info(f"{'='*80}\n")
            
            attempt_start = time.time()
            
            # Run validation (chunked or single)
            if len(chunks) == 1:
                result = self.run_validation()
            else:
                result = self.run_validation_chunked()
            
            attempt_end = time.time()
            
            # Extract accuracy score from result
            accuracy_score = self._extract_accuracy_score(result.content)
            
            # ✅ Store attempt info
            attempt_info = {
                'attempt_number': attempt,
                'accuracy_score': accuracy_score,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'processing_time': attempt_end - attempt_start,
                'result': result,
                'passed_threshold': accuracy_score >= self.min_accuracy_score if accuracy_score else False
            }
            self.validation_attempts.append(attempt_info)
            
            # ✅ Log attempt results
            logger.info(f"\n{'='*80}")
            logger.info(f"[{self.name}] 📊 ATTEMPT {attempt} RESULTS:")
            logger.info(f"  Accuracy Score: {accuracy_score}%" if accuracy_score else "  Accuracy Score: Not found")
            logger.info(f"  Threshold: {self.min_accuracy_score}%")
            logger.info(f"  Processing Time: {attempt_end - attempt_start:.2f}s")
            
            # Save attempt-specific output
            self._save_attempt_output(attempt, result.content, accuracy_score)
            
            # ✅ Decision logic
            if accuracy_score is None:
                logger.warning(f"[{self.name}] ⚠️ Could not extract accuracy score from validation")
                if attempt < self.max_validation_attempts:
                    logger.info(f"[{self.name}] 🔄 Retrying... (attempt {attempt + 1})")
                    continue
                else:
                    logger.warning(f"[{self.name}] ⚠️ Max attempts reached, accepting result without score")
                    logger.info(f"{'='*80}\n")
                    break
            
            if accuracy_score >= self.min_accuracy_score:
                logger.info(f"[{self.name}] ✅ PASSED! Accuracy {accuracy_score}% >= {self.min_accuracy_score}%")
                logger.info(f"{'='*80}\n")
                break
            else:
                logger.warning(f"[{self.name}] ❌ FAILED! Accuracy {accuracy_score}% < {self.min_accuracy_score}%")
                
                if attempt < self.max_validation_attempts:
                    logger.info(f"[{self.name}] 🔄 Retrying with enhanced prompt... (attempt {attempt + 1})")
                    logger.info(f"{'='*80}\n")
                    # Add feedback to improve next attempt
                    self._add_retry_feedback(accuracy_score)
                else:
                    logger.warning(f"[{self.name}] ⚠️ Max attempts reached, accepting best result")
                    logger.info(f"{'='*80}\n")
                    break
        
        # ✅ Generate final summary report
        final_result = self._generate_final_report()
        return final_result

    def _extract_accuracy_score(self, validation_content: str) -> Optional[int]:
        """
        Extract accuracy score from validation report.
        Looks for patterns like:
        - "Accuracy score: 85"
        - "Accuracy: 85%"
        - "Accuracy Score (0–100): 85"
        """
        patterns = [
            r'accuracy\s*score[:\s]*[(\[]?0[-–]100[)\]]?[:\s]*(\d+)',  # "Accuracy score (0-100): 85"
            r'accuracy[:\s]*(\d+)%',  # "Accuracy: 85%"
            r'accuracy[:\s]*(\d+)',   # "Accuracy: 85"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, validation_content, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                logger.debug(f"[{self.name}] Extracted accuracy score: {score}")
                return score
        
        logger.warning(f"[{self.name}] Could not extract accuracy score from validation content")
        return None

    def _add_retry_feedback(self, previous_score: int):
        """
        Add feedback context for retry attempts.
        This enriches the validation prompt with info about previous failure.
        """
        feedback = f"""
PREVIOUS VALIDATION ATTEMPT FEEDBACK:
- Previous accuracy score: {previous_score}%
- Required threshold: {self.min_accuracy_score}%
- Please be MORE THOROUGH in your analysis
- Pay special attention to edge cases and error handling
- Verify ALL functions/modules are covered in the specification
"""
        # Store feedback to be used in next prompt
        if not hasattr(self, 'retry_feedback'):
            self.retry_feedback = []
        self.retry_feedback.append(feedback)

    def _save_attempt_output(self, attempt_num: int, content: str, accuracy_score: Optional[int]):
        """Save each validation attempt to a separate file"""
        output_dir = Path(self.config["get_output_dir"](self.platform))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # ✅ Save attempt-specific file
        attempt_file = output_dir / f"{self.record_id}_validation_attempt_{attempt_num}.md"
        
        # Add header with attempt info
        header = f"""# Validation Attempt {attempt_num}
- Timestamp: {time.strftime("%Y-%m-%d %H:%M:%S")}
- Accuracy Score: {accuracy_score}% {'✅' if accuracy_score and accuracy_score >= self.min_accuracy_score else '❌'}
- Threshold: {self.min_accuracy_score}%

---

"""
        save_to_file(str(attempt_file), header + content)
        logger.info(f"[{self.name}] 💾 Saved attempt {attempt_num} to: {attempt_file}")

    def _generate_final_report(self) -> Any:
        """
        Generate comprehensive final report including all attempts.
        Returns the BEST attempt (highest accuracy) or last attempt.
        """
        output_dir = Path(self.config["get_output_dir"](self.platform))
        
        # Find best attempt
        best_attempt = max(
            self.validation_attempts,
            key=lambda x: x['accuracy_score'] if x['accuracy_score'] else 0
        )
        
        # ✅ Generate summary report
        summary = f"""# Validation Summary Report
Record ID: {self.record_id}
Platform: {self.platform.upper()}
Job ID: {self.job_id}

## Validation Attempts Summary

Total Attempts: {len(self.validation_attempts)}
Accuracy Threshold: {self.min_accuracy_score}%

"""
        
        for attempt in self.validation_attempts:
            status = "✅ PASSED" if attempt['passed_threshold'] else "❌ FAILED"
            score = f"{attempt['accuracy_score']}%" if attempt['accuracy_score'] else "N/A"
            summary += f"""
### Attempt {attempt['attempt_number']} {status}
- Timestamp: {attempt['timestamp']}
- Accuracy Score: {score}
- Processing Time: {attempt['processing_time']:.2f}s
- Status: {'Passed threshold' if attempt['passed_threshold'] else 'Below threshold'}
"""
        
        best_score = f"{best_attempt['accuracy_score']}%" if best_attempt['accuracy_score'] else "N/A"
        summary += f"""
## Final Decision

**Best Attempt: #{best_attempt['attempt_number']}**
- Accuracy Score: {best_score}
- Status: {'✅ Meets requirements' if best_attempt['passed_threshold'] else '⚠️ Below threshold (best available)'}

---

"""
        
        # ✅ Save summary report
        summary_file = output_dir / f"{self.record_id}_validation_SUMMARY.md"
        full_summary = summary + "\n\n# Detailed Validation Report\n\n" + best_attempt['result'].content
        save_to_file(str(summary_file), full_summary)
        logger.info(f"[{self.name}] 📊 Saved summary report: {summary_file}")
        
        # ✅ Save final validation (best attempt)
        final_file = output_dir / f"{self.record_id}_validation.md"
        save_to_file(str(final_file), best_attempt['result'].content)
        logger.info(f"[{self.name}] ✅ Saved final validation: {final_file}")
        
        # ✅ Log to CSV with all attempts info
        job_info = {
            "job_id": self.job_id,
            "platform": self.platform,
            "llm_model_name": self.model,
            "llm_processing_time": sum(a['processing_time'] for a in self.validation_attempts),
            "overall_processing_time": sum(a['processing_time'] for a in self.validation_attempts),
            "prompt_name": f"validation_{self.platform}_fs",
            "prompt_template": "inline_validation_prompt_with_retry",
            "unit": self.record_id,
            "input": "source_code + functional_spec",
            "output_type": "validation_report_final",
            "output_file": str(final_file),
            "validation_attempts": len(self.validation_attempts),
            "best_accuracy": best_attempt['accuracy_score'],
            "passed_threshold": best_attempt['passed_threshold'],
        }
        
        job_csv_file_name = output_dir / "job_details.csv"
        write_job_data_to_csv(job_data=job_info, file_name=str(job_csv_file_name))
        logger.info(f"[{self.name}] 📝 Updated job CSV: {job_csv_file_name}")
        
        logger.info(f"\n{'='*80}")
        logger.info(f"[{self.name}] 🎯 FINAL VALIDATION COMPLETE")
        logger.info(f"  Total Attempts: {len(self.validation_attempts)}")
        logger.info(f"  Best Accuracy: {best_score}")
        logger.info(f"  Files Saved:")
        logger.info(f"    - Summary: {summary_file}")
        logger.info(f"    - Final: {final_file}")
        for i in range(1, len(self.validation_attempts) + 1):
            logger.info(f"    - Attempt {i}: {output_dir / f'{self.record_id}_validation_attempt_{i}.md'}")
        logger.info(f"{'='*80}\n")
        
        return best_attempt['result']

    def run_validation_chunked(self) -> Any:
        """Validate by chunking source code and comparing each chunk against full spec"""
        logger.info(f"[{self.name}] [{self.platform.upper()}] "
                    f"Running chunked validation")
        
        code_chunks = self.chunker.chunk_code(self.source_code)
        
        logger.info(f"[{self.name}] [{self.platform.upper()}] "
                    f"Source code split into {len(code_chunks)} chunk(s)")
        
        all_validations = []
        
        for chunk in code_chunks:
            logger.info(f"[{self.name}] [{self.platform.upper()}] "
                        f"📝 Validating chunk {chunk['chunk_id']}")
            
            original_code = self.source_code
            self.source_code = chunk['content']
            
            chunk_validation = self.run_validation()
            
            all_validations.append({
                'chunk_id': chunk['chunk_id'],
                'tokens': chunk['tokens'],
                'validation': chunk_validation.content
            })
            
            self.source_code = original_code
        
        logger.info(f"[{self.name}] [{self.platform.upper()}] "
                    f"📝 Merging {len(code_chunks)} validation reports...")
        merged_validation = self._merge_validation_reports(all_validations)
        
        return merged_validation

    def _merge_validation_reports(self, validations):
        """Merge multiple validation reports into one comprehensive report"""
        
        merge_prompt = f"""
You are a senior validation engineer consolidating multiple validation reports.

You have received {len(validations)} validation reports, each comparing a chunk of source code against the full functional specification.

Your task: Create ONE comprehensive validation report that:
1. Combines all findings across chunks
2. Provides overall completeness and accuracy scores (IMPORTANT: Must include numerical scores!)
3. Lists all missing/incorrect points found across all chunks
4. Removes redundant findings
5. Provides consolidated actionable suggestions

CRITICAL: You MUST include clear numerical scores in this format:
- Completeness score (0–100): [number]
- Accuracy score (0–100): [number]

Validation Reports to Merge:
"""
        
        for val_info in validations:
            merge_prompt += f"\n\n## Validation Report for Chunk {val_info['chunk_id']} ({val_info['tokens']} tokens)\n"
            merge_prompt += val_info['validation']
        
        merge_prompt += """

Generate the final consolidated validation report with:
1. **Overall Assessment** - Single unified summary
2. **Correct Coverage** - Combined list of correctly described behaviors
3. **Missing or Incorrect Points** - Combined list (remove duplicates)
4. **Completeness / Accuracy Scores** - Overall scores for the entire codebase (MUST BE NUMERICAL!)
5. **Detailed Findings** - Consolidated findings across all chunks
6. **Actionable Suggestions** - Unified list of improvements
"""
        
        messages = [
            {"role": "system", "content": UNIVERSAL_VALIDATION_PROMPT},
            {"role": "user", "content": merge_prompt}
        ]
        
        start_time = time.time()
        response = self.call_model(messages, max_tokens=16000)
        end_time = time.time()
        
        # Note: We don't save here - this is just returning the merged content
        # Saving happens in the main execute loop via _save_attempt_output
        
        return response

    def build_prompt(self) -> Dict[str, str]:
        system_message = UNIVERSAL_VALIDATION_PROMPT

        platform_context = {
            "mainframe": "COBOL programs",
            "sas": "SAS programs and macros",
            "java": "Java classes and methods",
        }
        code_type = platform_context.get(self.platform, "source code")

        # Define element types based on platform
        platform_elements = {
            "mainframe": {
                "primary": "COBOL paragraphs/sections",
                "secondary": "COBOL variables",
                "data": "file/dataset references"
            },
            "sas": {
                "primary": "macros/PROCs",
                "secondary": "DATA steps",
                "data": "datasets"
            },
            "java": {
                "primary": "methods",
                "secondary": "class members",
                "data": "object references"
            }
        }
        elements = platform_elements.get(self.platform, platform_elements["mainframe"])

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
   
   FOR EACH ITEM FOUND, USE THIS EXACT FORMAT:
   
   **Missing Elements:**
   - `[Element Name]` ([Type: {elements['primary']}/{elements['secondary']}/{elements['data']}]) - Brief description of what it does in source code
   
   **Incorrect Descriptions:**
   - `[Element Name]` ([Type]) - What spec says vs What code actually does
   
   SPECIFICALLY CHECK:
   • All {elements['primary']} in source code
   • All {elements['secondary']} in source code  
   • All {elements['data']} referenced in source code
   • List EACH missing/incorrect element by NAME
   
   Example format:
   - `calculate_total` (macro) - Computes sum of expenses, **MISSING** from spec
   - `DATA step line 45` (DATA step) - Creates temp_output dataset, **MISSING** from spec
   - `sales_data` (dataset) - Input dataset referenced in PROC SORT, **NOT MENTIONED** in spec
   - `validate_records` (macro) - Spec says "validates dates" but code validates dates AND amounts

4. **Completeness / Accuracy Scores** (CRITICAL - MUST BE INCLUDED!)
   - Completeness score (0–100): [provide numerical score]
   - Accuracy score (0–100): [provide numerical score]

5. **Detailed Findings**
   
   Create a table with ALL {elements['primary']} and {elements['secondary']} found in source:
   
   | Element Name | Type | In Source? | In Spec? | Correct? | Notes |
   |--------------|------|------------|----------|----------|-------|
   | example_macro | Macro | ✅ | ❌ | N/A | Not documented |
   | process_data | DATA step | ✅ | ✅ | ⚠️ | Partial - missing error handling |
   
   List EVERY {elements['primary']}, {elements['secondary']}, and critical {elements['data']} from source code.

6. **Actionable Suggestions**
   - Specific improvements with element names
   - Example: "Add documentation for `calculate_totals` macro (lines 120-145)"
   - Example: "Correct description of `sales_data` dataset - spec says it has 5 columns but code shows 8"

Return everything as clean markdown. BE SPECIFIC with element names and line numbers where possible.
""".strip()

        # ✅ Add retry feedback if available
        if hasattr(self, 'retry_feedback') and self.retry_feedback:
            user_message += "\n\n" + "\n".join(self.retry_feedback)

        formatted_user_message = user_message.format(
            source_code=self.source_code or "",
            functional_spec=self.functional_spec or "",
        )
        
        input_size = len(formatted_user_message)
        logger.warning(f"📊 Validation Input: {input_size:,} chars (~{input_size//4:,} tokens)")

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
        
        output_size = len(response_content)
        logger.warning(f"📊 Validation Output: {output_size:,} chars (~{output_size//4:,} tokens)")

        # Note: Individual attempt saving happens in execute() via _save_attempt_output
        # We just return the response here
        
        return response


def validate_with_llm(
    job_id: str,
    record_id: str,
    base_dir: str,
    source_code: str,
    functional_spec: str,
    platform: str = "mainframe",
    min_accuracy_score: int = 75,  # ✅ NEW: Configurable threshold
) -> Dict:
    """
    Convenience wrapper to call ValidationAgent with retry logic.
    """
    agent = ValidationAgent(min_accuracy_score=min_accuracy_score)
    return agent.execute(
        job_id=job_id,
        record_id=record_id,
        base_dir=base_dir,
        source_code=source_code,
        functional_spec=functional_spec,
        platform=platform,
    )


# 3. **Missing or Incorrect Points**
   
#    List EACH missing element using this format:
#    - `[Name]` ([Type: macro/DATA step/PROC step/dataset/variable]) - What it does, **STATUS**
   
#    REQUIRED: Check ALL macros, DATA steps, PROC steps, datasets, and macro variables.
#    Use actual names from source code. No generic descriptions.
   
#    Example:
#    - `calc_metrics` (macro) - Computes monthly KPIs, **MISSING** from spec
#    - `input_sales` (dataset) - Primary input with 12 columns, **NOT DOCUMENTED** in spec
#    - `PROC SORT line 89` (PROC step) - Sorts by date+region, **MISSING** from spec
