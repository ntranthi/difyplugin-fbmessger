from typing import Dict, Any, Optional
import requests
from pydantic import BaseModel, Field
import logging

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