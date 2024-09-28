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
response = model.generate_content("How to beat my social anxiety?")
st.write(response.text)


# write statement below in terminal to run web app
# streamlit run main.py