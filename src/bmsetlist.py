import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta


@st.cache(ttl=3600, allow_output_mutation=True)
def get_song_list() -> dict:
    """
    Read song_list.csv
    Generate timedelta for dict values
    :return: songs as dict
    """
    songs = pd.read_csv('song_list.csv', header=None, index_col=0, squeeze=True).to_dict()
    for k, v in songs.items():
        t = datetime.strptime(v, '%M:%S')
        songs[k] = timedelta(minutes=t.minute, seconds=t.second)
    return songs


def get_total_time(generated_setlist: list, available_songs: dict) -> timedelta:
    """
    :param generated_setlist: Randomly chosen songs
    :param available_songs: All songs dict with durations
    :return: Total setlist duration
    """
    play_times = [available_songs[song] for song in generated_setlist]
    play_times.append(timedelta(minutes=6))  # Omajinai Time
    play_times.append(timedelta(minutes=2))  # Maid Waltz
    return sum(play_times, start=timedelta(0))


st.title('BAND-MAID')
st.header('Random Setlist Generator')
songs_dict = get_song_list()
with st.form('song_input_form'):
    serving_songs = st.number_input('Number of songs', min_value=1, max_value=len(songs_dict))
    song_sub = st.form_submit_button('OK')
    if song_sub:
        setlist = random.sample(list(songs_dict.keys()), serving_songs)
        total_time = get_total_time(setlist, songs_dict)
        col1, col2, col3 = st.columns(3)
        with col2:
            setlist.insert(0, "Maid Waltz")  # Always start with Maid Waltz
            ot = random.randint(1, len(setlist))
            setlist.insert(ot, "Omajinai Time")  # Insert Omajinai Time
            for i in setlist:
                st.text(i)
            st.text('----------')
            st.write(f'Total serving time {total_time}')
