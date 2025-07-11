from googleapiclient.discovery import build
import pandas as pd
import requests
import os
from dotenv import load_dotenv
if os.getenv("ENV") != "production":
    load_dotenv()

api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not set")

def get_channel(name):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
    "part":"snippet",
    "q": name,
    "type":"channel",
    "key": api_key
    }
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching channel: {e}")
        raise

    if 'error' in data:
        print(f"YouTube API error: {data['error']}")
        raise ValueError(f"YouTube API error: {data['error']}")

    if not data.get('items'):
        print(f"No channel found for: {name}. Response: {data}")
        raise ValueError(f"No channel found for: {name}")
    
    try:
        channel_id = data['items'][0]['id']['channelId']
    except (IndexError, KeyError):
        print(f"Channel ID could not be extracted. Response: {data}")
        raise ValueError("Channel ID could not be extracted from API response.")

    ch_url = 'https://www.googleapis.com/youtube/v3/channels'
    ch_params = {
        "part": "statistics,snippet",
        "id": channel_id,
        "key": api_key
    }
    ch_response = requests.get(ch_url, params=ch_params)
    try:
        ch_response.raise_for_status()
        ch_data = ch_response.json()
    except Exception as e:
        print(f"Error fetching channel details: {e}")
        raise
    if 'error' in ch_data:
        print(f"YouTube API error: {ch_data['error']}")
        raise ValueError(f"YouTube API error: {ch_data['error']}")
    return channel_id, ch_data

def get_channel_datails(ch_response):
    try:
        if 'error' in ch_response:
            print(f"YouTube API error: {ch_response['error']}")
            return pd.DataFrame()
        data = ch_response['items'][0]
        title = data['snippet'].get('title', 'Unknown')
        country = data['snippet'].get('country', 'Unknown')
        tot_view = int(data['statistics'].get('viewCount', 0))
        sub_count = int(data['statistics'].get('subscriberCount', 0))
        vid_count = int(data['statistics'].get('videoCount', 0))

        channel_stats = {
            'title': title,
            'country': country,
            'views': tot_view,
            'subscribers': sub_count,
            'videos': vid_count
        }
        df = pd.DataFrame([channel_stats])
        return df
    except (IndexError, KeyError, ValueError) as e:
        print("Error extracting channel details:", e)
        print(f"Channel response: {ch_response}")
        return pd.DataFrame()

def get_video_stats(channel_id):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 50,
        'order': 'date',     # This is important to filter videos by date
        'type': 'video',
        'key': api_key
    }

    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
    except Exception as e:
        print(f"Error fetching video list: {e}")
        return pd.DataFrame()

    if 'error' in search_data:
        print(f"YouTube API error: {search_data['error']}")
        return pd.DataFrame()

    video_ids = [item['id']['videoId'] for item in search_data.get('items', []) if 'id' in item and 'videoId' in item['id']]
    if not video_ids:
        print(f"No videos found. Response: {search_data}")
        return pd.DataFrame()

    videos_url = 'https://www.googleapis.com/youtube/v3/videos'
    videos_params = {
        'part': 'snippet,statistics',
        'id': ','.join(video_ids),
        'key': api_key
    }
    try:
        videos_response = requests.get(videos_url, params=videos_params)
        videos_response.raise_for_status()
        videos_data = videos_response.json()
    except Exception as e:
        print(f"Error fetching video stats: {e}")
        return pd.DataFrame()

    if 'error' in videos_data:
        print(f"YouTube API error: {videos_data['error']}")
        return pd.DataFrame()

    video_data = []
    if 'items' not in videos_data:
        print("No items in video stats response:", videos_data)
        return pd.DataFrame()

    for item in videos_data['items']:
        try:
            video_data.append({
                'title': item['snippet'].get('title', 'Unknown'),
                'upload_date': item['snippet'].get('publishedAt', ''),
                'views': int(item['statistics'].get('viewCount', 0)),
                'likes': int(item['statistics'].get('likeCount', 0))
            })
        except Exception as e:
            print(f"Error extracting video data: {e}, item: {item}")

    df_videos = pd.DataFrame(video_data)
    if not df_videos.empty and 'upload_date' in df_videos:
        df_videos['upload_date'] = pd.to_datetime(df_videos['upload_date'], errors='coerce')
    return df_videos





