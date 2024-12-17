import pytest
import websockets


@pytest.mark.asyncio
async def test_websocket():
    uri = "ws://localhost:5000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server")
        response = await websocket.recv()
        assert "Server received: Hello Server" in response
