from openai import OpenAI
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv
from .agent_config import load_config
import json 
import requests

load_dotenv()
config = load_config()

class LLMResponse:
    def __init__(self, content):
        self.content = content

class AgentBase(ABC):
    def __init__(self, name, provider, model="default", max_retries=1, verbose=True):
        self.name = name
        self.provider = provider
        
        # ✅ Only initialize OpenAI client for compatible providers
        if provider in ["google", "openai", "ollama"]:
            self.client = OpenAI(
                base_url=config[provider]['base_url'], 
                api_key=config[provider]['api_key']
            )
        elif provider == "gemma12b":
            self.client = None  # Use requests directly
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
        if model == "default": 
            self.model = config[provider]['model']
        else:
            self.model = model
            
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_model(self, messages, temperature=0.7, max_tokens=150):
        logger.debug(f"[{self.name}] Calling Model: {self.model}")
        retries = 0
        
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] Sending to Model [{self.model}]")
                
                # ✅ Route to appropriate handler
                if self.provider == "gemma12b":
                    response = self._call_gemma12b(messages, temperature, max_tokens)
                else:
                    response = self._call_openai_compatible(messages, temperature, max_tokens)
                
                if self.verbose:
                    logger.info(f"[{self.name}] Received response")
                
                return response
                
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error: {e}. Retry {retries}/{self.max_retries}")
        
        raise Exception(f"[{self.name}] Failed after {self.max_retries} retries")

    def _call_openai_compatible(self, messages, temperature, max_tokens):
        """Handle OpenAI-compatible providers"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        logger.debug(f"[{self.name}] Raw response: {response.model_dump_json(indent=2)}")
        return response.choices[0].message

    def _call_gemma12b(self, messages, temperature, max_tokens):
        """Handle gemma12b custom API"""
        # Convert messages to single prompt
        prompt = self._messages_to_prompt(messages)
        
        payload = {
            "user_message": prompt,
            "sender_id": "",
            "prompt": []
        }
        
        logger.debug(f"[{self.name}] Gemma12b payload: {json.dumps(payload, indent=2)}")
        
        # Call API
        base_url = config["gemma12b"]["base_url"]
        endpoint = config["gemma12b"]["endpoint"]
        url = f"{base_url}{endpoint}"
        
        response = requests.post(url=url, json=payload, timeout=120)
        response.raise_for_status()
        
        content = response.json()['content']
        logger.debug(f"[{self.name}] Gemma12b response: {content[:200]}...")
        
        return LLMResponse(content=content)

    def _messages_to_prompt(self, messages):
        """Convert OpenAI format to single prompt string"""
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            prompt_parts.append(f"{role}: {content}")
        return "\n\n".join(prompt_parts)
