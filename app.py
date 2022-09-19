import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import nltk
#nltk.download()
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import string
import os
import openai
import json
import streamlit as st
import streamlit.components.v1 as components
import requests
import numpy as np 

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


