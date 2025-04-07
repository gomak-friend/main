from flask import Flask, request, redirect
import requests
import base64
import urllib.parse

app = Flask(__name__)

# Client ID와 Secret , Spotify에 등록한 URI 입력
CLIENT_ID = 'e880c6a80bf24f1180cdd6859fb1e082'
CLIENT_SECRET = '58fb23b83d33402ba028d4812586cb64'
REDIRECT_URI = 'http://localhost:8080/callback'

# 로그인 유도
@app.route('/')
def login():
    scope = 'user-read-private user-read-email'
    auth_url = 'https://accounts.spotify.com/authorize'
    query = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': 'true'
    }
    return redirect(f"{auth_url}?{urllib.parse.urlencode(query)}")

# 로그인 성공 후 redirect → 토큰 요청
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()

    return f"""
    Access Token: {token_info.get('access_token')}<br>
    Refresh Token: {token_info.get('refresh_token')}<br>
    Expires In: {token_info.get('expires_in')}초
    """

if __name__ == '__main__':
    app.run(port=8080)
