import requests
import math
from langdetect import detect

class KrishiMitraTranslator:
    """Handles all translation between Marathi and English using Sarvam API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai"
        
        # Try different header formats
        self.headers = None
        self._find_working_headers()
        
        # Language codes for Sarvam API
        self.lang_codes = {
            'en': 'en-IN',
            'mr': 'mr-IN'
        }
        
        # Sarvam has a 1000 character limit - using 950 to be safe
        self.max_chars = 950
    
    def _find_working_headers(self):
        """Test which header format works with Sarvam API"""
        test_headers = [
            {"api-subscription-key": self.api_key, "Content-Type": "application/json"},
            {"API-Subscription-Key": self.api_key, "Content-Type": "application/json"},
            {"x-api-key": self.api_key, "Content-Type": "application/json"},
            {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        ]
        
        test_url = f"{self.base_url}/translate"
        test_payload = {
            "input": "test",
            "source_language_code": "en-IN",
            "target_language_code": "mr-IN"
        }
        
        for headers in test_headers:
            try:
                response = requests.post(test_url, json=test_payload, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Found working header: {list(headers.keys())[0]}")
                    self.headers = headers
                    return
            except:
                continue
        
        print("⚠️ Using default header format")
        self.headers = {"api-subscription-key": self.api_key, "Content-Type": "application/json"}
    
    def detect_language(self, text):
        """Check if query is Marathi or English"""
        try:
            lang = detect(text)
            return 'mr' if lang == 'mr' else 'en'
        except:
            # Fallback: check for Devanagari characters (Marathi script)
            for char in text:
                if ord(char) >= 0x0900 and ord(char) <= 0x097F:
                    return 'mr'
            return 'en'
    
    def split_into_chunks(self, text, max_length):
        """Split text into chunks of max_length characters while preserving structure"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += '\n\n' + para
                else:
                    current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # If any chunk is still too long, split by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= max_length:
                final_chunks.append(chunk)
            else:
                sentences = chunk.replace('. ', '.||').replace('? ', '?||').replace('! ', '!||').split('||')
                temp_chunk = ""
                for sentence in sentences:
                    if len(temp_chunk) + len(sentence) + 2 <= max_length:
                        if temp_chunk:
                            temp_chunk += '. ' + sentence
                        else:
                            temp_chunk = sentence
                    else:
                        if temp_chunk:
                            final_chunks.append(temp_chunk)
                        temp_chunk = sentence
                if temp_chunk:
                    final_chunks.append(temp_chunk)
        
        return final_chunks
    
    def translate(self, text, source_lang, target_lang):
        """Translate text using Sarvam AI with automatic chunking for long text"""
        if not text or text.strip() == "":
            return text
        
        if len(text) <= self.max_chars:
            return self._translate_single(text, source_lang, target_lang)
        
        chunks = self.split_into_chunks(text, self.max_chars)
        translated_chunks = []
        
        for chunk in chunks:
            translated = self._translate_single(chunk, source_lang, target_lang)
            translated_chunks.append(translated)
        
        return '\n\n'.join(translated_chunks)
    
    def _translate_single(self, text, source_lang, target_lang):
        """Translate a single chunk of text"""
        url = f"{self.base_url}/translate"
        
        source = self.lang_codes.get(source_lang, f"{source_lang}-IN")
        target = self.lang_codes.get(target_lang, f"{target_lang}-IN")
        
        payload = {
            "input": text,
            "source_language_code": source,
            "target_language_code": target
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('translated_text', text)
            else:
                return f"[Translation Failed] {text}"
        except Exception as e:
            return f"[Translation Error] {text}"