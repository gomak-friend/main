## 검색어 기반 곡 검색한것 가져오기
## 곡 기본정보 : 이름, 아티스트, 앨범, 인기도 (0~ 100), 출시일

# 파이썬 강제 인코딩
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
import base64

# Client ID랑 Secret 넣기
client_id = 'e880c6a80bf24f1180cdd6859fb1e082'
client_secret = '58fb23b83d33402ba028d4812586cb64'

# Access Token 요청하기
auth_url = 'https://accounts.spotify.com/api/token'
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

headers = {
    'Authorization': f'Basic {auth_header}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'client_credentials'
}

response = requests.post(auth_url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print("Access Token 받아오기 성공")

    # 검색 요청 보내기
    search_url = 'https://api.spotify.com/v1/search'
    params = {
        'q': '등대',       # 검색어
        'type': 'track',
        'limit': 1
    }

    search_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    search_response = requests.get(search_url, headers=search_headers, params=params)

    if search_response.status_code == 200:
        print("검색 성공! 결과는? \n")
        result = search_response.json()
        track = result['tracks']['items'][0]

        # 기본 정보 출력
        album_image_url = track['album']['images'][0]['url']

        print("검색된 인디 음악 정보:")
        print("곡 이름:", track['name'])
        print("아티스트:", track['artists'][0]['name'])
        print("앨범:", track['album']['name'])
        print("출시일:", track['album']['release_date'])
        print("인기도:", track['popularity'])
        print("앨범 커버 이미지:", album_image_url)
        print("Spotify 링크:", track['external_urls']['spotify'])

        # 아티스트 장르
        artist_id = track['artists'][0]['id']
        artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
        artist_response = requests.get(artist_url, headers=search_headers)

        if artist_response.status_code == 200:
            artist_data = artist_response.json()
            genres = artist_data.get('genres', [])
            print("아티스트 장르:", ', '.join(genres) if genres else '장르 정보 없음')
        else:
            print("아티스트 장르 정보 요청 실패:", artist_response.status_code)

    else:
        print("검색 요청 실패:", search_response.status_code)
else:
    print("인증 실패:", response.status_code)

