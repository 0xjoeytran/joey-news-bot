import anthropic
import json
import re
import asyncio
import hashlib
from datetime import datetime, timedelta
from config import CATEGORIES
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Cache in-memory + TTL (24 giờ)
classification_cache = {}
CACHE_TTL = timedelta(hours=24)

def get_cache_key(text: str) -> str:
    """Tạo key cache từ nội dung tin"""
    return hashlib.md5(text[:500].encode('utf-8')).hexdigest()

async def classify_news(text: str):
    """Classifier có Cache - Tiết kiệm token cực mạnh"""
    
    cache_key = get_cache_key(text)
    
    # Kiểm tra cache
    if cache_key in classification_cache:
        cached = classification_cache[cache_key]
        if datetime.now() - cached['timestamp'] < CACHE_TTL:
            print("⚡ Đã lấy từ cache (tiết kiệm token)")
            return cached['result']
    
    try:
        prompt = f"""
Phân loại tin tức sau vào đúng 1 category.

Categories: {list(CATEGORIES.keys())}

Tin: {text[:550]}

Trả về JSON thuần:
{{
    "category": "Tên category chính xác",
    "summary": "Tóm tắt ngắn ≤100 ký tự",
    "emoji": "emoji"
}}
"""

        response = await asyncio.to_thread(
            client.messages.create,
            model="claude-sonnet-4-6",
            max_tokens=220,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw_text = response.content[0].text.strip()
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        json_str = json_match.group(0) if json_match else raw_text
        
        result = json.loads(json_str)
        
        # Lưu vào cache
        classification_cache[cache_key] = {
            'result': result,
            'timestamp': datetime.now()
        }
        
        print("✅ Phân loại mới bởi Claude")
        return result
        
    except Exception as e:
        print(f"⚠️ Lỗi classifier: {e}")
        # Fallback
        fallback = {
            "category": "MACRO - Vĩ Mô",
            "summary": text[:90] + "...",
            "emoji": "📊"
        }
        classification_cache[cache_key] = {'result': fallback, 'timestamp': datetime.now()}
        return fallback
