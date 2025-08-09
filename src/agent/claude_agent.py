from anthropic import Anthropic
from config.settings import settings
import base64

class ClaudeAgent:
    def __init__(self):
        settings.validate()
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def get_response(self, message: str, conversation_history: list = None, images: list = None) -> str: 
        messages = conversation_history or []
        content = [{"type": "text", "text": message}]
    
        if images:
            for image_data in images:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_data["mime_type"],
                        "data": base64.b64encode(image_data["content"]).decode()
                    }
                })
        
        messages.append({"role": "user", "content": content})
        
        try:
            response = self.client.messages.create(
                model=settings.MODEL_NAME,
                max_tokens=1000,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"