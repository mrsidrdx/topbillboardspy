import numpy as np
from PIL import Image
import streamlit as st
from Helper import load_data, summary_poster

stats_df = load_data("./data/df_wclusters.csv")
color_map_df = load_data("./data/color_map_df.csv")

st.set_page_config(page_title="Music Through the Ages", 
                   page_icon=":notes:", 
                   layout='wide')

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------
title_image = Image.open("./plots/AppTitle.jpg")
st.image(title_image)

st.markdown("A Data Geek's take on the question ***'How have music tastes changed through the years?'***")
st.markdown("This app is meant as a playground to explore the dataset. It contains 50 years of \
                    [Billboard's Top 100 Year-End Hot singles]\
                        (https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2020) \
                            clustered by the themes identified in the project.")
#---------------------------------------------------------------#
# SELECT ARTIST AND SETUP DATA
#---------------------------------------------------------------#
sorted_artists = stats_df.groupby('search_artist')['search_query'].count()\
    .sort_values(ascending=False).index

st.markdown("### **Select Artist:**")
select_artist = []

select_artist.append(st.selectbox('', sorted_artists))

#Filter df based on selection
artist_df = stats_df[stats_df['search_artist'].isin(select_artist)]

major_cluster = artist_df.groupby('clusters')['search_query'].count()\
    .sort_values(ascending = False).index[0]

#Setting up color palette dict
color_dict = dict(zip(color_map_df['clusters'], color_map_df['colors']))

col1, col2 = st.beta_columns(2)
    
with col1:
    st.markdown(f"**Total Songs:** {artist_df.shape[0]}")
    st.markdown(f"**Top Song:** " +\
                f"{artist_df.loc[artist_df['track_rank']==np.min(artist_df['track_rank']),'search_query'].values[0]}")
    
with col2:
    st.markdown(f"**Highest Rank:** {np.min(artist_df['track_rank'])}")
    st.markdown(f"**Major Cluster:** {major_cluster}")

st.text("")
#---------------------------------------------------------------#
# CREATE SUMMARY POSTER
#---------------------------------------------------------------#
fig = summary_poster(artist_df, color_dict)
st.write(fig)