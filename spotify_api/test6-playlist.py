import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

# 액세스 토큰 복사해서 붙여넣기
access_token = 'BQCGll6NHw5lHh_SvzNLIKXT_h3oW2XJq7q2t2jZmS6fCLkvXyOgIwIBJwb3KsI5HMC7g-rGWeM5H2jvt-RjXGTbH6iXd21Wa4pODZmym6sH-Dj_l85cBi_05ss_2Cy5plOAnhQ6UJqyhDS6BMaax3FRReoFYs_Hh8PRUIYpou39ERhJDdsYaVMI1H6IJvvP03odiTPksjArOUA0ALz7XhaVX9hQuS1MfmNBbJD5LrWEREiMgQPYHw'

track_name = 'Love Dive'
artist_name = 'IVE'

def find_playlists_with_track(track_name, artist_name, access_token, max_playlists=10):
    print(f"\n'{track_name}' by {artist_name} 이 포함된 플레이리스트 찾는 중...")

    search_query = f"{track_name} {artist_name}"
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': search_query,
        'type': 'playlist',
        'limit': 20
    }

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        print("플레이리스트 검색 실패:", response.status_code)
        return []

    playlists = response.json().get('playlists', {}).get('items', [])
    matching_playlists = []

    for playlist in playlists[:max_playlists]:
        if not playlist:
            continue

        playlist_id = playlist.get('id')
        playlist_name = playlist.get('name')
        owner = playlist.get('owner', {}).get('display_name', 'unknown')
        playlist_url = playlist.get('external_urls', {}).get('spotify')

        if not playlist_id:
            continue

        # 플레이리스트 내 트랙 확인
        track_check_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        track_resp = requests.get(track_check_url, headers=headers)

        if track_resp.status_code != 200:
            continue

        track_items = track_resp.json().get('items', [])
        for item in track_items:
            track = item.get('track')
            if not track:
                continue

            name = track.get('name', '').lower()
            artists = [a.get('name', '').lower() for a in track.get('artists', [])]

            if track_name.lower() in name and artist_name.lower() in ' '.join(artists):
                matching_playlists.append({
                    'name': playlist_name,
                    'owner': owner,
                    'url': playlist_url
                })
                break

    return matching_playlists


# 실행
playlists = find_playlists_with_track(track_name, artist_name, access_token)

# 결과 출력
print("\n곡이 포함된 플레이리스트:")
if playlists:
    for p in playlists:
        print(f"- {p['name']} (by {p['owner']}) - {p['url']}")
else:
    print("곡이 포함된 플레이리스트를 찾을 수 없어요.")
