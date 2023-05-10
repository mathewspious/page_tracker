import pytest
import unittest.mock
from page_tracker.app import app

@pytest.fixture
def https_clinet():
    return app.test_client()

@unittest.mock.patch("page_tracker.app.redis")
def test_should_call_redis_incr(mock_redis, https_clinet):
    #Given
    mock_redis.return_value.incr.return_value = 5

    #When
    response = https_clinet.get("/")

    #Then
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    mock_redis.return_value.incr.assert_called_once_with("page_views")
