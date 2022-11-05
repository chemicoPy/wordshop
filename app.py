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
from settings import WAVE_OUTPUT_FILE
from io import BytesIO
from time import sleep
import math
from pathlib import Path

# Desiging & implementing changes to the standard streamlit UI/UX
st.set_page_config(page_icon="img/icon_2.jpg")    #Logo
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)

# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

# disable warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

   
assembly_auth_key = st.secrets["assembly_apikey"]
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
openai.api_key = OPENAI_APIKEY

assembly_auth_key_key = os.getenv("assembly_auth_key")
st.write(OPENAI_APIKEY)
st.write(assembly_auth_key_key)

headers = {
    'authorization': assembly_auth_key, 
    'content-type': 'application/json',
}

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

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
    
    st.sidebar.markdown(
            """
     ----------
    ## Project Overview
    wordshop is a project powered by OpenAI’s GPT-3. You can generate content with few words you input in either voice/speech or text!.
    """)    

    st.sidebar.markdown(
           """
    ----------
    ## How to use app:
    
    To use voice option 
    1. Click on "Start Recording" to start and "Stop" to stop the recording. 
    2. Then, wait for the app to process your voice and return the generated content. 
    3. Uttering a few words is enough to do the magic. 
    4. Examples are following prompt to GPT-3: 1. Can you generate for me a content on ... , 2. A short story on ... , 3. Think about the existence of Life outside Earth.
    -----------
    To use Direct text option
    ----------
    """)
    
    # preview app demo
    demo = st.sidebar.checkbox('App Demo')
    if demo == 1:
       st.sidebar.video('https://res.cloudinary.com/victorogunjobi/video/upload/v1657021658/Text-Speech-Analytic%20app/app_demo_rq2dpx.mp4', format='mp4')
    
    st.sidebar.markdown(

    """

    -----------

    # Let's connect

 
    [![Victor Ogunjobi](https://img.shields.io/badge/Author-@VictorOgunjobi-gray.svg?colorA=gray&colorB=dodgergreen&logo=github)](https://www.github.com/chemicopy)

    [![Victor Ogunjobi](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logoColor=white)](https://www.linkedin.com/in/victor-ogunjobi-a761561a5/)

    [![Victor Ogunjobi](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=gray)](https://twitter.com/chemicopy_)

    """)
    
    st.image('img/icon.png')  # Banner in the app
    st.subheader("Navigate to side bar to see full project info")
    st.markdown('Summary: Generate content with few words you input with text or voice-control  - powered by Artificial Intelligence (OpenAI GPT-3)! Implemented by '
        '[Victor Ogunjobi](https://www.linkedin.com/in/victor-ogunjobi-a761561a5/) - '
        'view project source code on '
        '[GitHub](https://github.com/chemicoPy/wordshop)')
    st.write('\n')  # add spacing
    st.subheader("Using voice option to generate content")   
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)
    
    #st.write(parent_dir) #./app/wordshop/input.wav
   
    #st_audiorec()
    val = st_audiorec()
    
    if isinstance(val, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):
            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(
                b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()

        # wav_bytes contains audio data in format to be further processed
        # display audio data as received on the Python side
        #st.audio(wav_bytes, format='audio/wav')
        
    #model = whisper.load_model("base")
    #result = model.transcribe("audio.mp3")
    #st.write(result["text"])
                
    #file_path = "./wordshop/app/$0"
   
    
 # This is where i stopped; next thing to do is to know the path whatever is being recorded is saved and integrate it below:

    #st_audiorec(file_path)

    #upload_url = upload_to_assemblyai(file_path)
    #st.write('Prompt uploaded to AssemblyAI')

    #transcription_id = transcribe(upload_url)
    #st.write('Prompt Sent for Transcription to AssemblyAI')

    #prompt = get_transcription_result(transcription_id)

    #st.write('Prompt Transcribed...Sending to GPT-3')
    #st.info(prompt)

    #gpt_output = call_gpt3(prompt)

    #st.write('Response Received from GPT-3')
    #st.success(gpt_output)
    

    st.button('Using voice: Generate content NOW!')
    
    st.subheader('\nOR using text option to generate content\n')
            
    st.write("\n")  # add spacing
    
    ex_names = [
        "In a shocking finding, scientists discovered a herd of unicorns living in a remote, previously unexplored valley, in the Andes Mountains. Even more surprising to the researchers was the fact that the unicorns spoke perfect English.",
        "The ancient people of Arcadia achieved oustanding cultural and technological developments. Below we summarise some of the highlights of the Acadian society.",
        """Tweet: "I hate it when my phone battery dies."
Sentiment: Negative
###
Tweet: My day has been 👍.
Sentiment: Positive
###
Tweet: This is the link to the article.
Sentiment: Neutral
###
Tweet: This new movie started strange but in the end it was awesome.
Sentiment:""",
        """Q: Fetch the departments that have less than five people in it.\n
A: SELECT DEPARTMENT, COUNT(WOKRED_ID) as "Number of Workers" FROM Worker GROUP BY DEPARTMENT HAVING COUNT(WORKED_ID) < 5;\n
###\n
Q: Show all departments along with the number of people in each department\n
A: SELECT DEPARTMENT, COUNT(DEPARTMENT) as "Number of Workers" FROM Worker GROUP BY DEPARTMENT;\n
###\n
Q: Show the last record of the Worker table\n
A: SELECT * FROM Worker ORDER BY LAST_NAME DESC LIMIT 1;\n
###\n
Q: Fetch the three max salaries from the Worker table;\n
A:""",
    ]

    inp = st.text_area(
        "Write your text here!", max_chars=2000, height=150
    )
    
    try:
        rec = ex_names.index(inp)
   
    except ValueError:
        rec = 0

    with st.beta_expander("Generation options..."):
        length = st.slider(
            "Choose the length of the generated texts (in tokens)",
            2,
            1024,
            512 if rec < 2 else 50,
            10,
        )
        temp = st.slider(
            "Choose the temperature (higher - more random, lower - more repetitive). For full content generation, it's recommended to use a higher value like 0.8. And for the code generation or sentence classification prompts, it's recommended to use a lower value, like 0.35",
            0.0,
            1.5,
            1.0 if rec < 2 else 0.35,
            0.05,
        )

    #response = None

    def aicontent(query):
        response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=query,
        temperature=temp,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    
        if 'choices' in response:
            if len(response['choices']) >0:
                st.write(response['choices'][0]['text'])
                #answer = response['choices'][0]['text']
            else:
                st.write('Oh, sorry ! i admit i failed this !')
 
        
    with st.form(key="inputs"):
        submit_button = st.form_submit_button(label="Using text: Generate content NOW!")

        if submit_button:
            aicontent(inp)
            
            
    
    #st.button('Using text: Generate content NOW!')
    

if __name__ == '__main__':
    main()
