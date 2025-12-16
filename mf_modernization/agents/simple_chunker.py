from typing import List, Dict
from loguru import logger

class SimpleChunker:
    """Dead simple code chunker. Just splits at token boundaries with overlap."""
    
    def __init__(self, max_tokens=5000):
        self.max_tokens = max_tokens
    
    def estimate_tokens(self, text: str) -> int:
        """Simple: ~4 chars = 1 token"""
        return len(text) // 4
    
    def chunk_code(self, code: str) -> List[Dict]:
        """Split code into chunks. Returns list of {chunk_id, content, tokens}"""
        
        total_tokens = self.estimate_tokens(code)
        
        # If fits, return as-is
        if total_tokens <= self.max_tokens:
            logger.info(f"✅ Single chunk ({total_tokens:,} tokens)")
            return [{'chunk_id': 0, 'content': code, 'tokens': total_tokens}]
        
        # Need to chunk
        logger.warning(f"⚠️ Chunking: {total_tokens:,} → {self.max_tokens:,} per chunk")
        
        lines = code.split('\n')
        chunks = []
        chunk_id = 0
        current_chunk = []
        current_tokens = 0
        
        for line in lines:
            line_tokens = self.estimate_tokens(line + '\n')
            
            # Save chunk if adding this line exceeds limit
            if current_tokens + line_tokens > self.max_tokens and current_chunk:
                chunks.append({
                    'chunk_id': chunk_id,
                    'content': '\n'.join(current_chunk),
                    'tokens': current_tokens
                })
                
                # 20% overlap for context
                overlap = len(current_chunk) // 5
                current_chunk = current_chunk[-overlap:] if overlap > 0 else []
                current_tokens = self.estimate_tokens('\n'.join(current_chunk))
                chunk_id += 1
            
            current_chunk.append(line)
            current_tokens += line_tokens
        
        # Last chunk
        if current_chunk:
            chunks.append({
                'chunk_id': chunk_id,
                'content': '\n'.join(current_chunk),
                'tokens': current_tokens
            })
        
        logger.info(f"✅ Created {len(chunks)} chunks")
        return chunks
