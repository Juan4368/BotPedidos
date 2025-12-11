from flask import json
import pytest
from unittest.mock import MagicMock
from whatsapp_webhook.service.webhook_service import WebhookService
from whatsapp_webhook.infrastructure.web.webhook_controller import WebhookController

@pytest.fixture
def webhook_service():
    return WebhookService()

@pytest.fixture
def webhook_controller(webhook_service):
    return WebhookController(webhook_service)

def test_process_message(webhook_service):
    mock_message = {"text": "Hello, World!"}
    webhook_service.process_message = MagicMock(return_value="Message processed")
    
    response = webhook_service.process_message(mock_message)
    
    assert response == "Message processed"
    webhook_service.process_message.assert_called_once_with(mock_message)

def test_webhook_controller_handle_post(webhook_controller):
    mock_request_data = json.dumps({"text": "Hello, World!"})
    webhook_controller.webhook_service.process_message = MagicMock(return_value="Message processed")
    
    response = webhook_controller.handle_post(mock_request_data)
    
    assert response == "Message processed"
    webhook_controller.webhook_service.process_message.assert_called_once_with(json.loads(mock_request_data))