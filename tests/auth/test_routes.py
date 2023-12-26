import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from src.users.exceptions import UsernameTaken


@pytest.mark.asyncio
async def test_register_user(client: TestClient) -> None:
    resp = await client.post(
        "/users",
        json={
            "username": "test_user",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json["details"]["username"] == "test_user"


@pytest.mark.asyncio
async def test_register_username_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.auth import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_username", fake_getter)

    resp = await client.post(
        "/users",
        json={
            "username": "test_user",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_json["msg"] == UsernameTaken.DETAIL


@pytest.mark.asyncio
async def test_user_login(client: TestClient) -> None:
    resp = await client.post(
        "/auth/token",
        json={
            "username": "test_user",
            "password": "123Aa!",
        },
    )

    resp_json = resp.json()
    access_token = resp_json["details"]["access_token"]

    resp = await client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["details"]["username"] == "test_user"


@pytest.mark.asyncio
async def test_blocked_refresh_token_after_refresh(client: TestClient) -> None:
    resp = await client.post(
        "/auth/token",
        json={
            "username": "test_user",
            "password": "123Aa!",
        },
    )

    resp_json = resp.json()
    refresh_token = resp_json["details"]["refresh_token"]

    resp = await client.post(
        "/auth/token/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert resp.status_code == status.HTTP_200_OK

    resp = await client.post(
        "/auth/token/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert resp.status_code != status.HTTP_200_OK


@pytest.mark.asyncio
async def test_user_logout(client: TestClient) -> None:
    resp = await client.post(
        "/auth/token",
        json={
            "username": "test_user",
            "password": "123Aa!",
        },
    )

    resp_json = resp.json()
    access_token = resp_json["details"]["access_token"]
    refresh_token = resp_json["details"]["refresh_token"]

    resp = await client.post(
        "/auth/token/logout",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "refresh_token": refresh_token,
        }
    )

    assert resp.status_code == status.HTTP_200_OK
