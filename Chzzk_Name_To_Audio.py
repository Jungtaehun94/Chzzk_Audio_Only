import streamlit as st
import requests,m3u8,json

def get_stream_url(username='룩삼오피셜'):
    req_result = requests.get(f"https://api.chzzk.naver.com/service/v1/search/channels?keyword={username}")
    channelId = req_result.json()['content']['data'][0]['channel']['channelId']
    if channelId:
        content = requests.get(f"https://api.chzzk.naver.com/service/v2/channels/{channelId}/live-detail").json()['content']
        live_status = content['status']
        if live_status == "OPEN":
            video_m3u8 = json.loads(content['livePlaybackJson'])['media'][0]['path']
            playlists = m3u8.load(video_m3u8)
            return playlists.media[1].base_uri+playlists.media[1].uri
        else:
            print(f'{username}은 방송 중이 아닙니다.')
    else:
        print(f'{username}을 찾지 못했습니다.')

st.title("Stream Finder")
username = st.text_input("Enter Twitch username:")

if username:
    stream_url = get_stream_url(username)

    if stream_url:
        st.success("Stream found:")
        st.write(stream_url)
    else:
        st.error("Stream not found.")