import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def auth_client(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()
    client.login(username="testuser", password="testpass")
    return client
