import streamlit as st
import requests
import time
import openai
import random

openai.api_key = "YOUR_API_KEY_HERE"
openai.organization = "YOUR_ORG_HERE"

st.title("BeatBuilder")
prompt = st.text_input("Enter the type of music you want to generate")
duration = st.slider("Enter duration of music in seconds", 1, 90)

if st.button("Generate Music") and (prompt and duration != ""):
    # generate music with all prompts
    with st.spinner('Generating music...'):
        r = requests.post('https://api-b2b.mubert.com/v2/TTMRecordTrack', json={
            "method": "TTMRecordTrack",
            "params":
                {
                    "text": prompt,
                    "pat": "MUBERT_PAT",
                    "mode": "loop",
                    "duration": duration,
                    "bitrate": "128"
                }
        })
        response = r.json()
        # creating music with the mubert api

        url = response['data']
        url = url['tasks']
        url = url[0]['download_link']

        theme = random.choice(['surrealism', '3D illustration', '3D illustration', 'Geometric', 'Retro', 'Realism'])
        dall_e_prompt = f"an album cover for a {prompt} music in {theme} style"
        # using dall-e to generate album cover
        response2 = openai.Image.create(
            prompt=dall_e_prompt,
            n=1,
            size="256x256",
        )
        image_url = response2['data'][0]['url']

        headers = {
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai.api_key}',
        }

        json_data = {
            'model': 'text-davinci-003',
            'prompt': f'Give me a song name for {prompt} music and a made up artist',
            'max_tokens': 12,
        } # using openai to generate song name

        response3 = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)
        song_name = (response3.json()['choices'][0]['text'])
        time.sleep(7)
    st.header(song_name)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image_url, width=200)
    with col2:
        st.audio(url, format="audio/mp3")
