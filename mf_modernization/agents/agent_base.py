# agents/agent_base.py

from openai import OpenAI
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv
from .agent_config import load_config
import json 
import requests

# ✨ NEW: LangChain imports
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

config = load_config()

class LLMResponse:
    def __init__(self, content):
        self.content = content

class AgentBase(ABC):
    def __init__(self, name, provider, model="default", max_retries=2, verbose=True):
        self.name = name
        self.provider = provider
        self.max_retries = max_retries
        self.verbose = verbose
        
        # ✅ Route to appropriate client based on provider
        if provider == "gemma12b":
            # Old custom Gemma12b server
            self.client = None
            self.client_type = "custom"
            self.model = config[provider].get('model', 'gemma12b')
            
        elif provider in ["gemma3:12b", "ollama"]:
            # ✨ NEW: LangChain Ollama client
            base_url = config[provider]['base_url']
            model_name = config[provider]['model'] if model == "default" else model
            
            self.client = Ollama(
                model=model_name,
                base_url=base_url
            )
            self.client_type = "langchain_ollama"
            self.model = model_name
            
        else:
            # OpenAI SDK for Google, OpenAI, etc.
            self.client = OpenAI(
                base_url=config[provider]['base_url'], 
                api_key=config[provider]['api_key']
            )
            self.client_type = "openai_sdk"
            if model == "default": 
                self.model = config[provider]['model']
            else:
                self.model = model
        
        logger.info(f"[{self.name}] Initialized: provider={provider}, model={self.model}, client={self.client_type}")
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_model(self, messages, temperature=0.7, max_tokens=150):
        logger.debug(f"[{self.name}] Calling Model: {self.model}")
        
        # ✅ Route based on client type
        if self.client_type == "custom":
            return self._call_gemma12b_server(messages, temperature, max_tokens)
        elif self.client_type == "langchain_ollama":
            return self._call_langchain_ollama(messages, temperature, max_tokens)
        elif self.client_type == "openai_sdk":
            return self._call_openai_compatible(messages, temperature, max_tokens)
        else:
            raise Exception(f"Unknown client type: {self.client_type}")
    
    def _call_openai_compatible(self, messages, temperature=0.7, max_tokens=150):
        """Call any OpenAI-compatible API (Google Gemini, OpenAI, etc.)"""
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] 🔧 Sending to {self.provider} [{self.model}]")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                
                logger.debug(f"[{self.name}] Raw response: {response.model_dump_json(indent=2)}")
                
                reply = response.choices[0].message
                
                if self.verbose:
                    logger.info(f"[{self.name}] ✅ Received: {len(reply.content)} chars\n")
                
                return reply
                
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error: {e}. Retry {retries}/{self.max_retries}")
                if retries >= self.max_retries:
                    raise Exception(f"[{self.name}] Failed after {self.max_retries} retries: {e}")
        
        raise Exception(f"[{self.name}] Failed after {self.max_retries} retries")
    
    def _call_langchain_ollama(self, messages, temperature=0.7, max_tokens=150):
        """✨ NEW: Call Ollama via LangChain (gemma3, ollama providers)"""
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] 🔧 Sending to {self.provider} via LangChain [{self.model}]")
                
                # Convert messages to LangChain format
                system_prompt = ""
                user_prompt = ""
                
                for msg in messages:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    
                    if role == 'system':
                        system_prompt = content
                    elif role == 'user':
                        user_prompt += content + "\n"
                
                # Build LangChain prompt template
                if system_prompt:
                    prompt_template = ChatPromptTemplate.from_messages([
                        ('system', system_prompt),
                        ('human', '{prompt}')
                    ])
                else:
                    prompt_template = ChatPromptTemplate.from_messages([
                        ('human', '{prompt}')
                    ])
                
                # Create chain: prompt -> llm -> parser
                chain = prompt_template | self.client | StrOutputParser()
                
                # Invoke the chain
                response_text = chain.invoke({'prompt': user_prompt.strip()})
                
                if self.verbose:
                    logger.info(f"[{self.name}] ✅ Received: {len(response_text)} chars\n")
                
                # Return in same format as other methods
                return LLMResponse(content=response_text)
                
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error: {e}. Retry {retries}/{self.max_retries}")
                if retries >= self.max_retries:
                    raise Exception(f"[{self.name}] Failed after {self.max_retries} retries: {e}")
        
        raise Exception(f"[{self.name}] Failed after {self.max_retries} retries")
    
    def _call_gemma12b_server(self, messages, temperature=0.7, max_tokens=150):
        """Call your OLD custom Gemma12b server (different API format)"""
        # Convert messages to single prompt
        prompt_parts = []
        for msg in messages:
            if msg.get('role') == 'system':
                prompt_parts.insert(0, msg.get('content', ''))
            else:
                prompt_parts.append(msg.get('content', ''))
        prompt = "\n\n".join(prompt_parts)
        
        # Build request
        base_url = config[self.provider].get('base_url', 'http://10.144.25.48:8087')
        endpoint = config[self.provider].get('endpoint', '/message/gemma12b')
        url = f"{base_url}{endpoint}"
        
        payload = {
            "user_message": prompt,
            "sender_id": "",
            "prompt": []
        }
        
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] 🔧 Sending to OLD Gemma12b server")
                
                response = requests.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=600
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data.get('content', '')
                    
                    if self.verbose:
                        logger.info(f"[{self.name}] ✅ Received: {len(content)} chars\n")
                    
                    return LLMResponse(content=content)
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")
                
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error: {e}. Retry {retries}/{self.max_retries}")
                if retries >= self.max_retries:
                    raise Exception(f"[{self.name}] Failed: {e}")
        
        raise Exception(f"[{self.name}] Failed after {self.max_retries} retries")
