import json
from typing import Dict, Any
import requests
from pydantic import BaseModel

class FacebookMessenger:
    def __init__(self, config: Dict[str, str]):
        self.page_access_token = config.get('page_access_token')
        self.verify_token = config.get('verify_token')
        self.api_version = 'v18.0'  # Current Facebook API version
        self.base_url = f'https://graph.facebook.com/{self.api_version}'

    def send_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        """Send message to a specific recipient on Facebook Messenger."""
        url = f'{self.base_url}/me/messages'
        params = {'access_token': self.page_access_token}
        data = {
            'recipient': {'id': recipient_id},
            'message': {'text': message_text}
        }
        
        response = requests.post(url, params=params, json=data)
        return response.json()

class WebhookRequest(BaseModel):
    object: str
    entry: list

def webhook(config: Dict[str, str], request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming webhook requests from Facebook Messenger."""
    messenger = FacebookMessenger(config)
    
    # Handle GET requests for webhook verification
    if request_data.get('hub.mode') == 'subscribe':
        if request_data.get('hub.verify_token') == messenger.verify_token:
            return {
                'success': True,
                'message': request_data.get('hub.challenge', '')
            }
        return {
            'success': False,
            'message': 'Invalid verify token'
        }

    try:
        # Parse the incoming webhook data
        webhook_data = WebhookRequest(**request_data)
        
        # Process each entry in the webhook
        for entry in webhook_data.entry:
            if 'messaging' in entry:
                for messaging_event in entry['messaging']:
                    sender_id = messaging_event['sender']['id']
                    
                    # Handle incoming messages
                    if 'message' in messaging_event:
                        # Here you would typically process the message and generate a response
                        # For now, we'll just echo back their message
                        if 'text' in messaging_event['message']:
                            received_text = messaging_event['message']['text']
                            messenger.send_message(sender_id, f"Echo: {received_text}")
        
        return {
            'success': True,
            'message': 'Webhook processed successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error processing webhook: {str(e)}'
        } 