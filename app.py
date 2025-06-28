import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import get_channel, get_channel_datails, get_video_stats

st.set_page_config(page_title="YouTube Analytics",page_icon=':bar_chart:',layout="wide")
st.title("YouTube Analytics Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)
channel_name = st.text_input("Name of channel")
if channel_name:
    channel_id,channel_response = get_channel(channel_name)
    channel_details = get_channel_datails(channel_response)
    title = channel_details['title']
    if hasattr(title, 'iloc'):
        title = title.iloc[0]

    channel_details['views'] = channel_details['views'].astype(int)
    channel_details['subscribers'] = channel_details['subscribers'].astype(int)
    channel_details['videos'] = channel_details['videos'].astype(int)
 
    st.subheader(f"Channel: {title}")
    st.subheader(f"Subscriber Count: {channel_details['subscribers']}")
    


    video_details = get_video_stats(channel_id)
    video_details.set_index("upload_date", inplace=True)

    st.subheader("Top 10 Videos and their Views and likes")
    st.write(video_details.nlargest(10, 'views'))
    top_10 = video_details.sort_values(by = 'views',ascending = False).head(10)
    top_10_bar = top_10[['title','views']].set_index('title')
    st.bar_chart(top_10_bar)

    
else:
    st.warning("Please enter channel name.")




