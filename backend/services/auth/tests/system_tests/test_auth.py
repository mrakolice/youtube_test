import json
import pytest
from pathlib import Path

from httpx import AsyncClient


@pytest.fixture
def auth_test_data():
    """Load auth test data."""
    test_data_file = Path(__file__).parent / "json" / "auth_requests.json"
    with open(test_data_file, "r") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, auth_test_data):
    """Test successful user registration."""
    response = await client.post(
        "/api/auth/register",
        json=auth_test_data["register_valid"],
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient, auth_test_data):
    """Test registration with short password."""
    response = await client.post(
        "/api/auth/register",
        json=auth_test_data["register_invalid_short_password"],
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, auth_test_data):
    """Test successful user login."""
    # First, register a user
    register_data = auth_test_data["register_valid"]
    await client.post("/api/auth/register", json=register_data)
    
    # Then, login
    login_data = auth_test_data["login_valid"]
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, auth_test_data):
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/auth/login",
        json=auth_test_data["login_invalid"],
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
