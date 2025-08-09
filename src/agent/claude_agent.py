from anthropic import Anthropic, APIConnectionError, APITimeoutError, RateLimitError 
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
        except APIConnectionError:
            return "ERROR: Unable to reach Claude API. Please check your internet connection and try again."
        except APITimeoutError:
            return "ERROR: Claude API request timed out. The service might be experiencing high load. Try again in a moment."
        except RateLimitError:
            return "ERROR: Rate limit exceeded. Please wait a moment before sending another message."
        except Exception as e:
            return f"ERROR: Unexpected error occurred: {str(e)}"