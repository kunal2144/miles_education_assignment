import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.cache import cache
from logs.models import UserActivityLog

@pytest.mark.django_db
def test_user_activity_model_creation():
    user = User.objects.create_user(username="testuser", password="password")
    log = UserActivityLog.objects.create(
        user=user,
        action="LOGIN",
        metadata={"ip": "127.0.0.1"}
    )
    assert log.user == user
    assert log.action == "LOGIN"
    assert log.status == "PENDING"

@pytest.mark.django_db
class TestUserActivityAPI:

    @pytest.fixture
    def setup_user(self):
        user = User.objects.create_user(username="tester", password="pass123")
        return user

    @pytest.fixture
    def auth_client(self, setup_user):
        client = APIClient()
        client.login(username="tester", password="pass123")
        return client

    def test_create_log(self, auth_client):
        res = auth_client.post("/api/logs/", {
            "action": "LOGIN",
            "metadata": {"device": "mobile"}
        }, format='json')
        assert res.status_code == 201
        assert res.data['action'] == "LOGIN"

    def test_get_logs(self, auth_client):
        auth_client.post("/api/logs/", {
            "action": "LOGIN"
        }, format='json')
        res = auth_client.get("/api/logs/")
        assert res.status_code == 200
        assert len(res.data) == 1

    def test_patch_status(self, auth_client):
        res = auth_client.post("/api/logs/", {
            "action": "LOGIN"
        }, format='json')
        log_id = res.data['id']
        patch_res = auth_client.patch(f"/api/logs/{log_id}/", {
            "status": "DONE"
        }, format='json')
        assert patch_res.status_code == 200
        assert "Updated to DONE" in patch_res.data['status']

@pytest.mark.django_db
def test_cache_works(auth_client):
    cache.clear()
    auth_client.post("/api/logs/", {"action": "LOGIN"})
    res1 = auth_client.get("/api/logs/")
    res2 = auth_client.get("/api/logs/")
    assert res1.data == res2.data