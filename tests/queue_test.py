import asyncio
import pytest
from src.queue import TrackQueue
from src.dataclasses import Track


@pytest.fixture
def test_event_loop():
    """Create and set an event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


def test_track_queue_initialization(tmp_path):
    """Test if the TrackQueue initializes correctly."""
    queue_path = tmp_path / "queue.pkl"
    track_queue = TrackQueue(str(queue_path))
    assert track_queue.queue_path == str(queue_path)
    track_queue.empty()


async def test_put_track(tmp_path):
    """Test that items can be added to the queue."""
    queue_path = tmp_path / "queue.pkl"
    track_queue = TrackQueue(str(queue_path))
    mock_track = Track(1, "test_name", "test_author")
    track_queue.put(mock_track)
    assert not track_queue.empty()


async def test_get_track(tmp_path):
    """Test that items can be retrieved correctly from the queue."""
    queue_path = tmp_path / "queue.pkl"
    track_queue = TrackQueue(str(queue_path))
    mock_track = Track(1, "test_name", "test_author")
    track_queue.put(mock_track)
    retrieved_track = track_queue.get()
    assert retrieved_track == mock_track
