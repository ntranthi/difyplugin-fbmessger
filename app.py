from typing import Dict, Any, Optional, List
import requests
from pydantic import BaseModel, Field
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessRequest(BaseModel):
    """Model for incoming process requests"""
    input_text: str = Field(..., description="Input text to process")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Optional parameters")

class PluginService:
    """Main service class for the plugin"""
    def __init__(self, config: Dict[str, Any]):
        """Initialize the plugin service with configuration"""
        self.api_key = config.get('api_key')
        self.max_retries = int(config.get('max_retries', 3))
        logger.info("Plugin service initialized with max_retries: %d", self.max_retries)

    def _make_api_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make an API request with retry logic"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(endpoint, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    logger.error("API request failed after %d attempts: %s", self.max_retries, str(e))
                    raise
                logger.warning("API request attempt %d failed: %s", attempt + 1, str(e))
        
        return {"error": "Max retries exceeded"}

    def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the incoming request"""
        try:
            # Validate request data
            request = ProcessRequest(**request_data)
            
            # Log the incoming request
            logger.info("Processing request with input: %s", request.input_text)

            # Example processing logic
            processed_data = {
                "input_length": len(request.input_text),
                "processed_text": request.input_text.upper(),
                "parameters_received": request.parameters
            }

            return {
                "success": True,
                "message": "Request processed successfully",
                "data": processed_data
            }

        except Exception as e:
            logger.error("Error processing request: %s", str(e))
            return {
                "success": False,
                "message": f"Error processing request: {str(e)}",
                "data": {}
            }

def process(config: Dict[str, Any], request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for the plugin"""
    service = PluginService(config)
    return service.process_request(request_data)

class MessageEvent(BaseModel):
    """Model for Facebook message event"""
    sender: Dict[str, str]
    recipient: Dict[str, str]
    timestamp: int
    message: Dict[str, Any]

class Entry(BaseModel):
    """Model for Facebook webhook entry"""
    id: str
    time: int
    messaging: List[Dict[str, Any]]

class WebhookEvent(BaseModel):
    """Model for Facebook webhook event"""
    object: str
    entry: List[Entry]

class FacebookMessenger:
    """Facebook Messenger API handler"""
    def __init__(self, config: Dict[str, str]):
        self.page_access_token = config.get('page_access_token')
        self.verify_token = config.get('verify_token')
        self.api_version = config.get('api_version', 'v18.0')
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
        
    def verify_webhook(self, mode: str, token: str, challenge: str) -> Dict[str, Any]:
        """Verify webhook subscription"""
        if mode == 'subscribe' and token == self.verify_token:
            return {
                'success': True,
                'message': challenge
            }
        return {
            'success': False,
            'message': 'Invalid verify token'
        }

    def send_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        """Send message to Facebook Messenger"""
        url = f'{self.base_url}/me/messages'
        
        data = {
            'recipient': {'id': recipient_id},
            'message': {'text': message_text}
        }
        
        params = {'access_token': self.page_access_token}
        
        try:
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            return {
                'success': True,
                'message': 'Message sent successfully',
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send message: {str(e)}',
                'data': {}
            }

def webhook(config: Dict[str, str], request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Facebook Messenger webhook"""
    messenger = FacebookMessenger(config)
    
    # Handle webhook verification
    if 'hub.mode' in request_data:
        mode = request_data.get('hub.mode')
        token = request_data.get('hub.verify_token')
        challenge = request_data.get('hub.challenge')
        return messenger.verify_webhook(mode, token, challenge)
    
    try:
        # Parse webhook event
        event = WebhookEvent(**request_data)
        
        if event.object != 'page':
            return {
                'success': False,
                'message': 'Invalid event object type',
                'data': {}
            }
        
        responses = []
        # Process each entry in the webhook event
        for entry in event.entry:
            for messaging_event in entry.messaging:
                if 'message' in messaging_event and 'text' in messaging_event['message']:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    
                    # Process the message (you can customize this part)
                    response_text = f"Echo: {message_text}"
                    
                    # Send response back to Facebook
                    response = messenger.send_message(sender_id, response_text)
                    responses.append(response)
        
        return {
            'success': True,
            'message': 'Webhook processed successfully',
            'data': {'responses': responses}
        }
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {
            'success': False,
            'message': f'Error processing webhook: {str(e)}',
            'data': {}
        } 