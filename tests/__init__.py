import pytest
from report import app

@pytest.fixture
def client():
    client = app.test_client()
    yield client