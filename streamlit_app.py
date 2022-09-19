import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import re
import string
import os
import openai
import json
import streamlit.components.v1 as components
from io import BytesIO
from time import sleep

# disable warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title('Language Workshop')
st.subheader("Navigate to side bar to see project info")
st.subheader("See below for options")


hide_streamlit_style = '''
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
'''
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

assembly_auth_key = "c30c21034f994fdca6a21ee77b49a25a"

openai.api_key = "sk-p999HAfj6Cm1bO00SXgJc7kFxvFPtQ1KBBWrqSOU"

headers = {
    'authorization': assembly_auth_key, 
    'content-type': 'application/json',
}

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

# STREAMLIT AUDIO RECORDER Instance
val = st_audiorec()
# web component returns arraybuffer from WAV-blob
st.write('Audio data received in the Python backend will appear below this message ...')

if isinstance(val, dict):  # retrieve audio data
    with st.spinner('retrieving audio-recording...'):
        ind, val = zip(*val['arr'].items())
        ind = np.array(ind, dtype=int)  # convert to np array
        val = np.array(val)             # convert to np array
        sorted_ints = val[ind]
        stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
        wav_bytes = stream.read()

        # wav_bytes contains audio data in format to be further processed
        # display audio data as received on the Python side
    st.audio(wav_bytes, format='audio/wav')

def upload_to_assemblyai(file_path):

    def read_audio(file_path):

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(5_242_880)
                if not data:
                    break
                yield data

    upload_response =  requests.post(upload_endpoint, 
                                     headers=headers, 
                                     data=read_audio(file_path))

    return upload_response.json().get('upload_url')


def transcribe(upload_url): 

    json = {"audio_url": upload_url}
    
    response = requests.post(transcription_endpoint, json=json, headers=headers)
    transcription_id = response.json()['id']

    return transcription_id


def get_transcription_result(transcription_id): 

    current_status = "queued"

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

    while current_status not in ("completed", "error"):
        
        response = requests.get(endpoint, headers=headers)
        current_status = response.json()['status']
        
        if current_status in ("completed", "error"):
            return response.json()['text']
        else:
            sleep(10)
            
            
def call_gpt3(prompt):

    response = openai.Completion.create(engine = "text-davinci-001", 
                                        prompt = prompt, max_tokens = 50)
    return response["choices"][0]["text"]

def main():

    st.title("Talking to GPT-3")
    file_path = "input.wav"

    record_audio(file_path)

    upload_url = upload_to_assemblyai(file_path)
    st.write('Prompt uploaded to AssemblyAI')

    transcription_id = transcribe(upload_url)
    st.write('Prompt Sent for Transciption to AssemblyAI')

    prompt = get_transcription_result(transcription_id)

    st.write('Prompt Transcribed...Sending to GPT-3')
    st.info(prompt)

    gpt_output = call_gpt3(prompt)

    st.write('Response Received from GPT-3')
    st.success(gpt_output)




if __name__ == '__main__':
    main()
