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


assembly_auth_key = "c30c21034f994fdca6a21ee77b49a25a"

openai.api_key = "sk-p999HAfj6Cm1bO00SXgJc7kFxvFPtQ1KBBWrqSOU"

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
   
   st.image('img/icon.png')  # Banner in the app
   st.markdown('Generate content with few words you input with text or voice-control  - powered by Artificial Intelligence (OpenAI GPT-3)! Implemented by '
        '[Victor Ogunjobi](https://www.linkedin.com/in/victor-ogunjobi-a761561a5/) - '
        'view project source code on '
        '[GitHub](https://github.com/chemicoPy/wordshop)')
   st.write('\n')  # add spacing
            
   parent_dir = os.path.dirname(os.path.abspath(__file__))
   build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
   st_audiorec = components.declare_component("st_audiorec", path=build_dir)

   #st_audiorec()
   st_audiorec()

   st.button('Using voice: Generate content NOW!')
    
   st.subheader('\nOR Enter text below\n')
            
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
            "Choose the temperature (higher - more random, lower - more repetitive). For the code generation or sentence classification promps it's recommended to use a lower value, like 0.35",
            0.0,
            1.5,
            1.0 if rec < 2 else 0.35,
            0.05,
        )

   response = None
    
    
   st.button('Using text: Generate content NOW!')

            
   file_path = "input.wav"

# This is where i stopped; next thing to do is to know the path whatever is being recorded is saved and integrate it below:

   st_audiorec(file_path)

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
