# Dify Python Plugin Template

A template for creating Python plugins for Dify. This template provides a basic structure and implementation that you can build upon for your specific use case.

## Features

- Robust error handling and logging
- Request validation using Pydantic
- Configurable retry mechanism for API calls
- Type hints for better code maintainability
- Example processing logic

## Configuration

The plugin requires the following configuration:

### Required Settings
- `api_key` (secret): API key for authentication

### Optional Settings
- `max_retries` (number): Maximum number of retry attempts for API calls (default: 3)

## API Endpoints

### POST /process

Main endpoint for processing requests.

#### Request Format
```json
{
    "input_text": "Text to process",
    "parameters": {
        "optional_param1": "value1",
        "optional_param2": "value2"
    }
}
```

#### Response Format
```json
{
    "success": true,
    "message": "Request processed successfully",
    "data": {
        "input_length": 123,
        "processed_text": "PROCESSED TEXT",
        "parameters_received": {
            "optional_param1": "value1",
            "optional_param2": "value2"
        }
    }
}
```

## Error Handling

The plugin includes comprehensive error handling:
- Input validation errors
- API request failures with retry mechanism
- General exception handling

## Development

### Prerequisites
- Python 3.10 or higher
- pip for package management

### Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Testing
To test the plugin locally:
1. Configure your API key in the Dify dashboard
2. Send a test request to the /process endpoint

### Extending the Plugin
To extend the plugin's functionality:
1. Add new configuration parameters in `config.yaml`
2. Extend the `ProcessRequest` model in `app.py` for new input fields
3. Add new processing logic in the `PluginService` class
4. Update error handling as needed

## Best Practices

1. Always validate input data using Pydantic models
2. Use type hints for better code maintainability
3. Implement proper error handling and logging
4. Keep configuration flexible using the config.yaml file
5. Follow Python PEP 8 style guidelines

## Security Considerations

1. Never log sensitive information
2. Use environment variables or secrets for sensitive configuration
3. Validate and sanitize all input data
4. Implement rate limiting when necessary
5. Use HTTPS for all external API calls

## Support

For questions and support, please open an issue in the repository or contact the Dify support team. 