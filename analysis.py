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
    params = params = {
    "part":"snippet",
    "q": name,
    "type":"channel",
    "key": api_key
    }
    response = requests.get(url,params=params).json()
    print(response)

    if not response.get('items'):
        raise ValueError(f"No channel found for: {name}")
    
    try:
        channel_id = response['items'][0]['id']['channelId']
    except (IndexError, KeyError):
        raise ValueError("Channel ID could not be extracted from API response.")
    

    ch_url = 'https://www.googleapis.com/youtube/v3/channels'
    ch_params = {
        "part": "statistics,snippet",
        "id": channel_id,    
        "key": api_key       
    }
    ch_response = requests.get(ch_url,params=ch_params).json()
    return channel_id,ch_response

def get_channel_datails(ch_response):
    try:
        data = ch_response['items'][0]
        title = data['snippet']['title']
        country = data['snippet'].get('country', 'Unknown')
        tot_view = int(data['statistics']['viewCount'])
        sub_count = int(data['statistics']['subscriberCount'])
        vid_count = int(data['statistics']['videoCount'])

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

    search_response = requests.get(search_url, params=search_params).json()
    video_ids = [item['id']['videoId'] for item in search_response.get('items',[])]
    
    if not video_ids:
        print("No videos found ")
        return pd.DataFrame()

    videos_url = 'https://www.googleapis.com/youtube/v3/videos'
    videos_params = {
        'part': 'snippet,statistics',
        'id': ','.join(video_ids),
        'key': api_key
    }
    videos_response = requests.get(videos_url, params=videos_params).json()

    video_data = []

    if 'items' not in videos_response:
        print("No items in video stats response:", videos_response)
        return pd.DataFrame()

    for item in videos_response['items']:
        video_data.append({
            'title': item['snippet']['title'],
            'upload_date': item['snippet']['publishedAt'],
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0))
        })

    df_videos = pd.DataFrame(video_data)

    if not df_videos.empty:
        df_videos['upload_date'] = pd.to_datetime(df_videos['upload_date'])
    return df_videos





