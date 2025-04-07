# 아티스트 장르 기반으로 곡 10개 검색 + 기본 정보 출력

import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests

# Access Token: 브라우저에서 복사한 값 붙여넣기
access_token = 'BQDBaUk_mXxzXAp7AHP430oiZY5zEnGI6SVyfAgwn0MM-p3r0VVRs1mEGuofAuTMawXufivLZRWFJp1nCl7pit10lHzen-l90EFxhWV__i9FB7_gpJc0Wi5MJRebEPTYdaTQemfZJHt28MxfctW8vX382ml7vjlNPOS1SFk7KO6bxBLq0njsrbOvQrNjfv-H1MhV52zLfYSPaoGWP-zQGYH8ZKB_ZalKuq33LGzK3QHc3TKKkZaDWA'

# 검색할 장르
genre_name = 'k-pop'  # 예: 'indie', 'folk', 'korean pop' 등 (지원되는 장르만!)

# Spotify 검색 API (장르 기반)
search_url = 'https://api.spotify.com/v1/search'
params = {
    'q': f'genre:"{genre_name}"',
    'type': 'track',
    'limit': 10
}

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(search_url, headers=headers, params=params)

if response.status_code == 200:
    print(f" '{genre_name}' 장르 기반 곡 검색 결과:\n")
    results = response.json()
    tracks = results['tracks']['items']

    for i, track in enumerate(tracks, 1):
        name = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        release = track['album']['release_date']
        popularity = track['popularity']
        spotify_url = track['external_urls']['spotify']
        album_image_url = track['album']['images'][0]['url']
        
        print(f"[{i}] {name}")
        print(f" 아티스트: {artist}")
        print(f" 앨범: {album}")
        print(f" 출시일: {release}")
        print(f" 인기도: {popularity}")
        print(f" 앨범 커버 이미지: {album_image_url}")
        print(f" Spotify 링크: {spotify_url}\n")

else:
    print("검색 요청 실패:", response.status_code)
