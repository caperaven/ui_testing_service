import pytest
from process_api.utils.utils import replace_server_url


@pytest.mark.asyncio
async def test_url_state_server_no_change():
    state = {}
    url = 'http://localhost:8001/api/v1/processes'
    new_url = replace_server_url(url, state)
    assert new_url == 'http://localhost:8001/api/v1/processes'


@pytest.mark.asyncio
async def test_url_state_server_with_change():
    state = {'server': 'http://localhost:8000'}
    url = '${state.server}/api/v1/processes'
    new_url = replace_server_url(url, state)
    assert new_url == 'http://localhost:8000/api/v1/processes'
