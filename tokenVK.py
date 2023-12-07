from urllib.parse import urlencode


APP_ID = ''
OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
params = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
     'display': 'page',
     'scope': 'status,photos',
     'response_type': 'token'
 }
oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'
print(oauth_url)