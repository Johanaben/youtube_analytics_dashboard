import streamlit as st
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

    subs = channel_details['subscribers']
    if hasattr(subs, 'iloc'):
        subs = subs.iloc[0]
    st.subheader(f"Channel: {title}")
    st.subheader(f"Subscriber Count: {subs}")
    


    video_details = get_video_stats(channel_id)

    video_details.set_index("upload_date", inplace=True)

    st.subheader("View Count Over Time")
    st.line_chart(video_details['views'])


    st.subheader("Views and Likes Over Time")
    st.line_chart(video_details[['views', 'likes']])
else:
    st.warning("Please enter channel name.")




