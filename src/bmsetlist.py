import streamlit as st
import random
from datetime import timedelta
from songs import song_list


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
with st.form('song_input_form'):
    serving_songs = st.number_input('Number of songs', min_value=1, max_value=len(song_list))
    song_sub = st.form_submit_button('PO!')
    if song_sub:
        setlist = random.sample(list(song_list.keys()), serving_songs)
        total_time = get_total_time(setlist, song_list)
        col1, col2, col3 = st.columns(3)
        with col2:  # Center on screen
            setlist.insert(0, "Maid Waltz")  # Always start with Maid Waltz
            ot = random.randint(1, len(setlist))  # Random spot for Omajinai Time
            setlist.insert(ot, "Omajinai Time")  # Insert Omajinai Time
            for i in setlist:
                st.text(i)
            st.text('----------')
            st.write(f'Total serving time {total_time}')
