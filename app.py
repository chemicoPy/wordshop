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

inp = st.text_area(
        "Write your text here!", max_chars=2000, height=150
    )
