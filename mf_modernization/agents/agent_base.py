# agents/agent_base.py

import requests
from requests.exceptions import Timeout, ConnectionError
from loguru import logger
import time

class AgentBase:
    def __init__(self, name, provider="ollama", model="llama3.2", max_retries=2, verbose=True):
        self.name = name
        self.provider = provider
        self.model = model
        self.max_retries = max_retries
        self.verbose = verbose
    
    def call_model(self, messages, temperature=0.7, max_tokens=4000):
        """Call LLM with correct payload format for Gemma server"""
        
        # ✅ Convert messages to single prompt string
        prompt = self._messages_to_prompt(messages)
        
        # ✅ VERIFY: Build payload exactly like your working invoke_llm()
        if self.provider == "gemma12b" or self.provider == "gemma":
            payload = {
                "user_message": prompt,
                "sender_id": "",
                "prompt": []
            }
            url = "http://10.144.25.48:8087/message/gemma12b"
        else:
            # For other providers
            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            url = f"http://someotherserver/{self.provider}"
        
        # ✅ DEBUG: Print EXACT payload being sent
        logger.info(f"[{self.name}] 🔧 Calling {self.provider}")
        logger.info(f"  URL: {url}")
        logger.info(f"  Prompt length: {len(prompt)} chars")
        logger.info(f"  Payload keys: {list(payload.keys())}")  # ✅ VERIFY THIS
        logger.info(f"  Payload: {str(payload)[:200]}")  # ✅ PRINT ACTUAL PAYLOAD
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"[{self.name}] 📤 Attempt {attempt}/{self.max_retries}")
                
                start_time = time.time()
                
                # ✅ Make the request
                response = requests.post(
                    url,
                    json=payload,  # ✅ Sending correct format
                    timeout=1000
                )
                
                elapsed = time.time() - start_time
                
                logger.info(f"[{self.name}] 📥 Response in {elapsed:.2f}s")
                logger.info(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # ✅ Your server returns {"content": "..."}
                    if 'content' in result:
                        content = result['content']
                        logger.info(f"  ✅ Got content: {len(content)} chars")
                        return type('obj', (object,), {'content': content})()
                    else:
                        logger.error(f"  ❌ No 'content' field. Response: {result}")
                        raise Exception("No 'content' in response")
                else:
                    logger.error(f"  ❌ Status {response.status_code}")
                    logger.error(f"  Body: {response.text[:500]}")
                    
                    if attempt < self.max_retries:
                        time.sleep(5)
                        continue
                    raise Exception(f"Server error {response.status_code}")
                
            except Timeout:
                logger.error(f"[{self.name}] ⏱️ Request timeout after 1000s")
                logger.error(f"  Server is processing but taking too long")
                if attempt < self.max_retries:
                    logger.info(f"  Retrying in 10s...")
                    time.sleep(10)
                else:
                    raise Exception(f"[{self.name}] Timeout after {self.max_retries} attempts")
            
            except ConnectionError as e:
                logger.error(f"[{self.name}] 🔌 CONNECTION FAILED")
                logger.error(f"  Error: {str(e)[:200]}")
                logger.error(f"  This means:")
                logger.error(f"    - Server at {url} is DOWN or UNREACHABLE")
                logger.error(f"    - Network connectivity issue")
                logger.error(f"    - Firewall blocking connection")
                
                if attempt < self.max_retries:
                    logger.info(f"  Waiting 10s and retrying...")
                    time.sleep(10)
                else:
                    logger.error(f"  ❌ CRITICAL: Cannot connect to LLM server!")
                    logger.error(f"  ❌ Please check:")
                    logger.error(f"     1. Is Gemma server running on 10.144.25.48:8087?")
                    logger.error(f"     2. Can you ping 10.144.25.48?")
                    logger.error(f"     3. Try: curl http://10.144.25.48:8087/message/gemma12b")
                    raise Exception(f"[{self.name}] Cannot connect to server at {url}")
            
            except Exception as e:
                logger.error(f"[{self.name}] ❌ Error: {str(e)[:200]}")
                if attempt < self.max_retries:
                    time.sleep(5)
                else:
                    raise Exception(f"[{self.name}] Failed: {str(e)[:200]}")
        
        raise Exception(f"[{self.name}] Failed after {self.max_retries} retries")
    
    def _messages_to_prompt(self, messages):
        """
        Convert messages array to single prompt string.
        
        Matches your original invoke_llm() format.
        """
        prompt_parts = []
        
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            if role == 'system':
                # System message first
                prompt_parts.insert(0, content)
            else:
                # User message
                prompt_parts.append(content)
        
        # Join with double newline
        final_prompt = "\n\n".join(prompt_parts)
        
        return final_prompt
