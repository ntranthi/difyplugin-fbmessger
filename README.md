# Facebook Messenger Plugin for Dify

This plugin enables integration between Dify and Facebook Messenger, allowing you to receive messages from Facebook Messenger and send responses back.

## Setup

1. Create a Facebook Page and Facebook App if you haven't already
2. Get your Page Access Token from Facebook Developer Console
3. Set up a webhook in your Facebook App settings
4. Configure the plugin in Dify with the following settings:
   - `page_access_token`: Your Facebook Page Access Token
   - `verify_token`: A secret token of your choice for webhook verification

## Configuration

The plugin requires two configuration values:

1. `page_access_token`: The access token for your Facebook page (obtained from Facebook Developer Console)
2. `verify_token`: A verification token of your choice that will be used to verify webhook subscriptions

## Webhook URL

The webhook endpoint will be available at:
```
https://dify.agrisung.xyz/fb-webhook
```

## Features

- Receives messages from Facebook Messenger
- Verifies webhook subscriptions
- Sends messages back to users on Facebook Messenger
- Handles text messages (can be extended to handle other message types)

## Usage

1. Configure the plugin in Dify with your Facebook credentials
2. Set up the webhook URL in your Facebook App settings
3. Use the verify token you configured when setting up the webhook
4. The plugin will automatically handle incoming messages and can send responses back

## Development

To extend the plugin's functionality, you can modify the `app.py` file to:
- Add support for different message types
- Implement custom message processing logic
- Add error handling
- Implement rate limiting
- Add support for additional Facebook Messenger features

## Error Handling

The plugin includes basic error handling and will return appropriate error messages if:
- Webhook verification fails
- Message processing fails
- API calls to Facebook fail 