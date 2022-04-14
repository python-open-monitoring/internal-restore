import pprint

import pytest

from consumer import methods


@pytest.mark.asyncio
async def test_restore():
    # pytest -s
    """
    {
        "message":"test message",
        "monitor_id":"443",
        "source":"test",
        "username":"test"
    }

    """
    json_rq = {"monitor_id": "2", "monitor_name": "ya.ru", "monitor_host": "ya.ru", "monitor_port": "443"}
    pprint.pprint(json_rq)
    result = await methods.monitor(json_rq)
    assert result
