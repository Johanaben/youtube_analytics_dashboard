import streamlit as st

st.set_page_config(page_title="Spotify Dashboard",layout="centered")
st.header("Spotify API: Rhythm and Trends ")
st.subheader("Aim of the project")
st.write("It all started with me noticing something strange with my monthly spotify analytics."\
         " For one particular month, it showed that my **slowest** and **fastest** song were the **exact same track** — lowest BPM and highest BPM at once." \
"This weird glitch led down a rabbit hole." \
"This project is a result of that curiosity fueled by my love for music theory and my growing interest in the world of data science.")
st.markdown("<h3>What is the average BPM across genres?<br>Does it vary across genres?</h3>",unsafe_allow_html = True)
st.subheader("Does BPM always mean fast paced?")
st.subheader("The nuances: A little music theory lesson")