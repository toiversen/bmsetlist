import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

songs_dict = pd.read_csv('song_list.csv', header=None, index_col=0, squeeze=True).to_dict()
for k, v in songs_dict.items():
    t = datetime.strptime(v, '%M:%S')
    songs_dict[k] = timedelta(minutes=t.minute, seconds=t.second)


def get_total_time(setlist: list, songs_dict: dict) -> timedelta:
    """
    :param setlist: Randomly chosen songs
    :param songs_dict: All songs dict with durations
    :return: Total setlist duration
    """
    play_times = [songs_dict[k] for k in setlist]
    return sum(play_times, start=timedelta(0))


st.title('BAND-MAID')
st.header('Random Setlist Generator')

with st.form('song_input_form'):
    serving_songs = st.number_input('Number of songs', min_value=1, max_value=len(songs_dict))
    song_sub = st.form_submit_button('OK')
    if song_sub:
        setlist = random.sample(songs_dict.keys(), serving_songs)
        total_time = get_total_time(setlist, songs_dict)
        col1, col2, col3 = st.columns(3)
        with col2:
            for i in setlist:
                st.text(i)
            st.text('----------')
            st.write(f'Total serving time {total_time}')
