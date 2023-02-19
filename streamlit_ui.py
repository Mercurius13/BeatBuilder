
Save New Duplicate & Edit Just Text Twitter
# generate a boilerplate streamlit app with text fields for text prompt, a slider for duration, and a button to generate music
import streamlit as st
import requests
import time
import openai
openai.api_key = "your-api-key-here"
openai.organization = "organisation_id"
import random

st.title("BeatBuilder")
prompt = st.text_input("Enter text prompt")
duration = st.slider("Enter duration of music in seconds", 1, 90)
if st.button("Generate Music") and (prompt and duration != ""):
    # generate music with all prompts

    with st.spinner('Generating music...'):
        #play audio
        r = requests.post('https://api-b2b.mubert.com/v2/TTMRecordTrack', json={
            "method": "TTMRecordTrack",
            "params":
                {
                    "text": prompt,
                    "pat": "public-access-token-here",
                    "mode": "loop",
                    "duration": duration,
                    "bitrate": "128"
                }
        })
        response = r.json()
       # print(response)

        url = response['data']
        url = url['tasks']
        url = url[0]['download_link']

        # print(url)
        theme=random.choice(['surrealism','3D illustration','3D illustration','Geometric','Retro','Realism'])
        dall_e_prompt = f"an album cover for a {prompt} music in {theme} style"
        response2 = openai.Image.create(
            prompt=dall_e_prompt,  # TODO: this is input
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
            'prompt': f'Give me a song name for {prompt} music and a made up artist',  #
            'max_tokens': 12,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)
        song_name = (response.json()['choices'][0]['text'])
        print('Prompt: ', prompt)
        print('Tags: ', tags)
        print('Duration: ', duration)
        print('Dall-E prompt: ', dall_e_prompt)
        print('Song name: ', song_name)
        time.sleep(7)
    st.header(song_name)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image_url, width=200)
    with col2:
        st.audio(url, format="audio/mp3")
