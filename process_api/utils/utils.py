def replace_server_url(url, state):
    if '${state.server}' not in url:
        return url

    server_url = state.get('server')
    return url.replace('${state.server}', server_url)