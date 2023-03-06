# wordshop

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Project Overview
wordshop is powered by OpenAI’s GPT-3. You can generate content with few words you input in either voice/speech or text!

## [Use App](https://wordshop.streamlit.app/)

# App Demo

## Description
GPT-3; a Large Language Model (LLM for short) is available to the public, with accessibility using OpenAI’s APIs. As a result, since its release, OpenAI’s GPT-3 has been leveraged in over 300 applications/products. (source: [here](https://openai.com/blog/gpt-3-apps/)).

GPT-3 takes a text input as a prompt and performs the task of text completion by predicting one token at a time. What makes GPT-3 special is the scale at which it was built, possessing nearly 175B parameters.

The GPT-3 model expects a text prompt as an input.

I made "wordshop" a two- option thing. Voice/Speech & Direct Text. 

However, if to begin with speech, it's important to first convert speech to text and then feed the transcribed text as input to the GPT-3 model.

This is how GPT-3 model works 👇👇
![First screenshot](assets/img1.gif)

![Second screenshot](assets/img2.gif)


Visualization of GPT-3 generating natural language texts. (Credit: [Jay Alammar](https://jalammar.github.io/how-gpt3-works-visualizations-animations/))

To generate audio transcription, I used AssemblyAI’s speech-to-text transcription API.

The high-level workflow of the application is demonstrated in the image below:

## Prerequisites


## App Use
To use voice option:
Click on "Start Recording" to start and "Stop" to stop the recording. Then, wait for the app to process your voice and return the generated content.
Uttering a few words is enough to do the magic.
Examples are following prompt to GPT-3: " Can you generate for me a content on ... " , "A short story on ... ", “Think about the existence of Life outside Earth.”
