# agents/agent_base.py

from openai import OpenAI
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv
from .agent_config import load_config
import json 
from ollama import Client
import requests
import time

# Load environment variables
load_dotenv()

config = load_config()

#To standardize the LLM Response, used for Ollama LLM Invocation.
class LLMResponse:
    def __init__(self, content):
        self.content = content

#Base Agent Class
class AgentBase(ABC):
    def __init__(self, name, provider, model="default", max_retries=2, verbose=True):
        self.name = name
        self.provider=provider
        self.client = OpenAI(base_url=config[provider]['base_url'], api_key=config[provider]['api_key'])
    
        if model=="default": 
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
                    logger.info(f"[{self.name}] Sending messages to Model [{self.model}]:")
                    """ for msg in messages:
                        logger.debug(f"  {msg['role']}: {msg['content']}") """
                #TODO
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                ) 
                reply = response.choices[0].message

                #TODO , for testing purpose, use 2L below when you don't want to invoke LLM for some dummy tests.
                # dummy_content_bytes = "This is the dummy content in bytes."
                # reply = LLMResponse(content=dummy_content_bytes)
                # time.sleep(10)

                if self.verbose:
                    logger.info(f"***********[{self.name}] Received response: {reply} *********\n\n")

                return reply
            except Exception as e:
                logger.info(f"[{self.name}]  Retry {retries}/{self.max_retries}")
                retries += 1
                logger.error(f"[{self.name}] Error during OpenAI call: {e}. Retry {retries}/{self.max_retries}")
        raise Exception(f"[{self.name}] Failed to get response from OpenAI after {self.max_retries} retries.")