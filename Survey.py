import streamlit as st

st.title('Survey')

st.subheader("Question 1")
x = st.slider("How do you feel when meeting new people? (1 = Very Uncomfortable, 5 = Very Comfortable)", value=3, min_value=1, max_value=5)
result = st.button('Submit', x)

if result:
    st.success('You submitted the task!')
