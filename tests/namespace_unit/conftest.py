import pytest


@pytest.fixture(autouse=True)
def _reset_between_tests():
    """These tests need no Factorio server; override the server reset."""
    yield
