"""The client's constructor contract."""

from monosurf import MonosurfClient


def test_api_host_defaults_to_mono_surf():
    """Without an explicit host the client talks to the public API."""
    assert MonosurfClient("key").api_host == "https://api.mono.surf"


def test_api_host_can_be_overridden_and_loses_its_trailing_slash():
    """Another API server is addressed through the constructor, not by poking the attribute."""
    assert MonosurfClient("key", api_host="https://pay.example.test/").api_host == "https://pay.example.test"
