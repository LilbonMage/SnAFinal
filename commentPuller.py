import requests
import pandas as pd
import time

API_KEY = 'AIzaSyAoE-J1zBrpIG0l4lpSJnZN4qwvTCjKUk0'  # 🔁 換成你的 API 金鑰
VIDEO_IDS = [
    'kdf3QRXg6jo',
    'TLQitdKrUm8',
    'l56zOTnUFdw',
    'QT7lzdT_6YE',
    's5zW5IHcLi8'
]

def get_comments_for_video(video_id, api_key, max_results=500):
    comments = []
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'
    count = 0

    while url and count < max_results:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Failed to fetch comments for video {video_id}')
            break

        data = response.json()
        for item in data.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'video_id': video_id,
                'author': comment.get('authorDisplayName'),
                'text': comment.get('textDisplay'),
                'like_count': comment.get('likeCount'),
                'published_at': comment.get('publishedAt')
            })
            count += 1
            if count >= max_results:
                break

        next_token = data.get('nextPageToken')
        if next_token:
            url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100&pageToken={next_token}'
            time.sleep(0.5)  # 避免觸發速率限制
        else:
            break

    return comments

# 主程式：處理所有影片
all_comments = []

for vid in VIDEO_IDS:
    print(f'正在抓取影片 {vid} 的留言...')
    video_comments = get_comments_for_video(vid, API_KEY)
    all_comments.extend(video_comments)
    print(f'✔️ 抓到 {len(video_comments)} 筆留言')

# 存成 CSV
df = pd.DataFrame(all_comments)
df.to_csv('youtube_multi_video_comments.csv', index=False, encoding='utf-8-sig')
print(f'🎉 共抓到 {len(df)} 筆留言，已儲存至 youtube_multi_video_comments.csv')
