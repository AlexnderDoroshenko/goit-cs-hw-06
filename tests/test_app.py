# TODO: Rework tests for socket implementation add db client tests
import pytest
from aiohttp import web
from app.main import create_app


@pytest.fixture
async def client():
    app = await create_app()
    return await app.test_client()


async def test_home(client):
    resp = await client.get('/')
    assert resp.status == 200
    assert 'Welcome' in await resp.text()


async def test_message(client):
    resp = await client.get('/message')
    assert resp.status == 200
    assert 'Send a message' in await resp.text()
