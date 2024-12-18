from googleapiclient.discovery import build
from datetime import datetime
import csv

def get_video_titles(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # チャンネル情報の取得
    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()

    if 'items' not in channel_response or not channel_response['items']:
        print(f"エラー: チャンネルID '{channel_id}' が見つかりません。")
        return []

    # アップロード済み動画のプレイリストIDを取得
    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    video_info = []  # タイトルとURLを格納するリストに変更
    next_page_token = None

    while True:
        # プレイリストアイテムの取得
        playlist_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        # タイトルとビデオIDの抽出
        for video in playlist_response['items']:
            title = video['snippet']['title']
            video_id = video['snippet']['resourceId']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'  # URLの生成
            video_info.append((title, video_url))  # タプルとして追加

        # 次のページがあるかチェック
        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break
    return video_info

# 使用例
if __name__ == "__main__":
    API_KEY = 'Google Cloud PlatformにあるYOUTUBE_API_KEY'
    CHANNEL_ID = 'チャンネル詳細の共有ボタンから探せます'
    video_info = get_video_titles(CHANNEL_ID, API_KEY)
    # CSVファイルとして保存
    with open('video_list.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # ヘッダーの書き込み
        writer.writerow(['No.', 'タイトル', 'URL'])
        # データの書き込み
        for i, (title, url) in enumerate(video_info, 1):
            writer.writerow([i, title, url])

    print("video_list.csvにデータを保存しました。")
