import chainlit as cl
from PIL import Image
import io
from agent.claude_agent import ClaudeAgent

agent = ClaudeAgent()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming chat messages"""
    
    # Handle file attachments
    files_content = ""
    images = []
    
    if message.elements:
        for element in message.elements:
            if element.mime and element.mime.startswith('image/'):
                print(f"Element: {dir(element)}")
                print(f"Content type: {type(element.content)}")
                print(f"Content length: {len(element.content) if element.content else 'None'}")
                
                content = None
                if element.content:
                    content = element.content
                elif element.path:
                    with open(element.path, 'rb') as f:
                        content = f.read()
                
                if content:
                    images.append({
                        "content": content,
                        "mime_type": element.mime
                    })
                    files_content += f"\n\nImage file: {element.name}"
                else:
                    files_content += f"\n\nImage file: {element.name} (failed to load)"
            elif hasattr(element, 'content') and element.content:
                try:
                    files_content += f"\n\nFile: {element.name}\n{element.content.decode('utf-8')}"
                except:
                    files_content += f"\n\nFile: {element.name} (binary content)"
                    
    # Combine message and file content
    full_message = message.content + files_content
    
    # Get conversation history from session
    conversation_history = cl.user_session.get("conversation_history", [])
           
    # Get response from Claude
    response = await agent.get_response(full_message, conversation_history, images)
    
    # Update conversation history
    conversation_history.extend([
        {"role": "user", "content": message.content},
        {"role": "assistant", "content": response}
    ])
    cl.user_session.set("conversation_history", conversation_history)
    
    # Send response
    await cl.Message(content=response).send()

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    cl.user_session.set("conversation_history", [])
    await cl.Message(content="Hello! I'm your AI concierge. How can I help you today?").send()