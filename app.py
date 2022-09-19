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

# disable warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title('Job Recommender System')
st.subheader("Navigate to side bar to see project info")
st.subheader("See below for options")


hide_streamlit_style = '''
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
'''
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



inp = st.text_area(
        "Write your text here!", max_chars=2000, height=150
    )
