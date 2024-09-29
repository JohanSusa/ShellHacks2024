import streamlit as st
import requests
import google.generativeai as genai
import os

# @authors Johan Susa, Mauro Angelini, Richard Chong, and William_Guerrero


# To declare variable as an environment variable, run command below (recommended for security purposes

# export API_KEY=<YOUR_API_KEY>


# api_key = "AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw"

genai.configure(api_key="AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw")

st.title("Being Human")
st.subheader("Conquer social anxiety at any level")

model = genai.GenerativeModel("gemini-1.5-flash")

# response = model.generate_content("How to beat my social anxiety? in 5 paragraphs")
# st.write(response.text)

# write statement below in terminal to run web app
# streamlit run main.py


prompt_extreme_anxiety = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                          'nonexistent level of social skills. separate each challenge with a "#". Also do not number '
                          'the challenges.')

prompt_severe_anxiety = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                         'low level of social skills. separate each challenge with a "#". Also do not number '
                         'the challenges.')

prompt_mod_anxiety = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                      'medium level of social skills. separate each challenge with a "#". Also do not number '
                      'the challenges.')

prompt_mild_anxiety = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                       'high level of social skills. separate each challenge with a "#". Also do not number '
                       'the challenges.')

prompt_no_anxiety = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                     'extremely high/proficient level of social skills. separate each challenge with a "#". Also do '
                     'not number the challenges.')

list1 = [prompt_extreme_anxiety, prompt_severe_anxiety, prompt_mod_anxiety, prompt_mild_anxiety, prompt_no_anxiety]

for i in range(5):
    response = model.generate_content(list1[i])
    print(response.text)
