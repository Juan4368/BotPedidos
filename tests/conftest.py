import pytest

@pytest.fixture
def sample_data():
    return {
        "message": "Hello, World!",
        "sender": "1234567890",
        "recipient": "0987654321"
    }