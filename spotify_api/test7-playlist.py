import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

# Access Token 복사해서 붙여넣기
access_token = 'BQCGll6NHw5lHh_SvzNLIKXT_h3oW2XJq7q2t2jZmS6fCLkvXyOgIwIBJwb3KsI5HMC7g-rGWeM5H2jvt-RjXGTbH6iXd21Wa4pODZmym6sH-Dj_l85cBi_05ss_2Cy5plOAnhQ6UJqyhDS6BMaax3FRReoFYs_Hh8PRUIYpou39ERhJDdsYaVMI1H6IJvvP03odiTPksjArOUA0ALz7XhaVX9hQuS1MfmNBbJD5LrWEREiMgQPYHw'

# 수록곡 기본 정보 출력 함수
def print_track_info(track, index=None):
    name = track.get('name')
    artists = ', '.join([a.get('name') for a in track.get('artists', [])])
    album = track.get('album', {}).get('name')
    release = track.get('album', {}).get('release_date')
    popularity = track.get('popularity')
    spotify_url = track.get('external_urls', {}).get('spotify')

    if index is not None:
        print(f"[{index}] {name}")
    else:
        print(f"- {name}")
    print(f"아티스트: {artists}")
    print(f"앨범: {album}")
    print(f"출시일: {release}")
    print(f"인기도: {popularity}")
    print(f"Spotify 링크: {spotify_url}\n")

# 플레이리스트 검색
def search_playlists_by_keyword(keyword, access_token, limit=10):
    url = "https://api.spotify.com/v1/search"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'q': keyword,
        'type': 'playlist',
        'limit': limit
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("플레이리스트 검색 실패:", response.status_code)
        return []

    return response.json().get('playlists', {}).get('items', [])

# 플레이리스트 ID로 트랙 목록 가져오기
def get_playlist_tracks(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("트랙 가져오기 실패:", response.status_code)
        return []

    return [item['track'] for item in response.json().get('items', []) if item.get('track')]

# 실행 흐름
keyword = input("검색할 키워드를 입력하세요: ").strip()

playlists = search_playlists_by_keyword(keyword, access_token, limit=15)

if not playlists:
    print("해당 키워드를 포함한 플레이리스트를 찾을 수 없어요.")
else:
    print(f"\n'{keyword}'가 포함된 플레이리스트 {len(playlists)}개 찾음:\n")
    for i, pl in enumerate(playlists, 1):
        if not pl:
            continue

        name = pl.get('name', '제목 없음')
        owner_info = pl.get('owner')
        owner_name = owner_info.get('display_name') if owner_info else 'unknown'
        print(f"[{i}] {name} (by {owner_name})")

    try:
        selected = int(input("\n보고 싶은 플레이리스트 번호를 선택하세요: ").strip()) - 1

        if 0 <= selected < len(playlists):
            selected_playlist = playlists[selected]
            playlist_id = selected_playlist.get('id')
            playlist_name = selected_playlist.get('name')
            owner = selected_playlist.get('owner', {}).get('display_name', 'unknown')

            print(f"\n선택한 플레이리스트: {playlist_name} (by {owner})")
            tracks = get_playlist_tracks(playlist_id, access_token)

            print(f"\n총 수록곡 {len(tracks)}개:\n")
            for i, track in enumerate(tracks, 1):
                print_track_info(track, i)
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")
