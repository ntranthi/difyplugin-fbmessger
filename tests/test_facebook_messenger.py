import pytest
from app import FacebookMessenger, WebhookEvent

def test_verify_webhook():
    config = {
        'page_access_token': 'test_token',
        'verify_token': 'test_verify_token'
    }
    messenger = FacebookMessenger(config)
    
    # Test successful verification
    result = messenger.verify_webhook('subscribe', 'test_verify_token', 'test_challenge')
    assert result['success'] is True
    assert result['message'] == 'test_challenge'
    
    # Test failed verification
    result = messenger.verify_webhook('subscribe', 'wrong_token', 'test_challenge')
    assert result['success'] is False
    assert result['message'] == 'Invalid verify token'

def test_webhook_event_validation():
    valid_event = {
        'object': 'page',
        'entry': [{
            'id': '123',
            'time': 1458692752478,
            'messaging': [{
                'sender': {'id': 'user123'},
                'recipient': {'id': 'page123'},
                'timestamp': 1458692752478,
                'message': {'text': 'test message'}
            }]
        }]
    }
    
    # Test valid event
    event = WebhookEvent(**valid_event)
    assert event.object == 'page'
    assert len(event.entry) == 1
    assert event.entry[0].id == '123'
    
    # Test invalid event
    with pytest.raises(Exception):
        WebhookEvent(**{'object': 'invalid', 'entry': []})

def test_send_message(mocker):
    config = {
        'page_access_token': 'test_token',
        'verify_token': 'test_verify_token'
    }
    messenger = FacebookMessenger(config)
    
    # Mock the requests.post call
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'message_id': '123'}
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.post', return_value=mock_response)
    
    result = messenger.send_message('user123', 'test message')
    assert result['success'] is True
    assert 'message_id' in result['data'] 