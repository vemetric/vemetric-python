"""
Tests for the VemetricClient class
"""

import json
from unittest.mock import Mock, patch

import pytest
import requests
from requests_mock import Mocker

from .client import VemetricClient, UserData

@pytest.fixture
def client():
    return VemetricClient(token="test-token")

@pytest.fixture
def mock_session():
    session = requests.Session()
    session.post = Mock()
    return session

def test_init_without_token():
    with pytest.raises(ValueError, match="token must be provided"):
        VemetricClient(token="")

def test_init_with_custom_host():
    client = VemetricClient(token="test-token", host="https://custom.host")
    assert client._host == "https://custom.host"

def test_init_with_custom_session():
    session = requests.Session()
    client = VemetricClient(token="test-token", session=session)
    assert client._sess == session

def test_track_event_basic(client, mock_session):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_session.post.return_value = mock_response
    
    client._sess = mock_session
    client.track_event("test_event")
    
    mock_session.post.assert_called_once()
    args, kwargs = mock_session.post.call_args
    assert args[0] == "https://hub.vemetric.com/e"
    assert kwargs["headers"]["Token"] == "test-token"
    assert json.loads(kwargs["data"]) == {"name": "test_event"}

def test_track_event_with_all_data(client, mock_session):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_session.post.return_value = mock_response
    
    client._sess = mock_session
    client.track_event(
        "test_event",
        user_identifier="user123",
        event_data={"action": "click"},
        user_data={
        "set": {"name": "Test User"},
        "setOnce": {"first_seen": "2024-01-01"},
        "unset": ["old_property"]
    }
    )
    
    mock_session.post.assert_called_once()
    args, kwargs = mock_session.post.call_args
    assert args[0] == "https://hub.vemetric.com/e"
    assert kwargs["headers"]["Token"] == "test-token"
    assert json.loads(kwargs["data"]) == {
        "name": "test_event",
        "userIdentifier": "user123",
        "customData": {"action": "click"},
        "userData": {
            "set": {"name": "Test User"},
            "setOnce": {"first_seen": "2024-01-01"},
            "unset": ["old_property"]
        }
    }

def test_track_event_empty_name(client):
    with pytest.raises(ValueError, match="event_name must not be empty"):
        client.track_event("")

def test_update_user_basic(client, mock_session):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_session.post.return_value = mock_response
    
    client._sess = mock_session
    client.update_user("user123")
    
    mock_session.post.assert_called_once()
    args, kwargs = mock_session.post.call_args
    assert args[0] == "https://hub.vemetric.com/u"
    assert kwargs["headers"]["Token"] == "test-token"
    assert json.loads(kwargs["data"]) == {"userIdentifier": "user123"}

def test_update_user_with_data(client, mock_session):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_session.post.return_value = mock_response
    
    client._sess = mock_session
    client.update_user(
        "user123",
        user_data={
            "set": {"name": "Test User", "email": "test@example.com"},
            "setOnce": {"first_seen": "2024-01-01"},
            "unset": ["old_property"]
        }
    )
    
    mock_session.post.assert_called_once()
    args, kwargs = mock_session.post.call_args
    assert args[0] == "https://hub.vemetric.com/u"
    assert kwargs["headers"]["Token"] == "test-token"
    assert json.loads(kwargs["data"]) == {
        "userIdentifier": "user123",
        "data": {
            "set": {"name": "Test User", "email": "test@example.com"},
            "setOnce": {"first_seen": "2024-01-01"},
            "unset": ["old_property"]
        }
    }

def test_update_user_empty_identifier(client):
    with pytest.raises(ValueError, match="user_identifier required"):
        client.update_user("")

def test_network_error_handling(client, mock_session):
    mock_session.post.side_effect = requests.RequestException("Connection error")
    
    client._sess = mock_session
    # Should not raise an exception, just log the error
    client.track_event("test_event")

def test_http_error_handling(client, mock_session):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_session.post.return_value = mock_response
    
    client._sess = mock_session
    # Should not raise an exception, just log the error
    client.track_event("test_event") 