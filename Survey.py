import streamlit as st

total_score = 0

st.title('Survey')

if 'question_number' not in st.session_state:
    st.session_state.question_number = 1

def show_question_1():
    st.subheader("Question 1")
    st.slider("How do you feel when meeting new people? (1 = Very Uncomfortable, 5 = Very Comfortable)", value=3, min_value=1, max_value=5 )
    if st.button("Next"):
        st.session_state.question_number = 2



def show_question_2():
    st.subheader("Question 2")
    st.slider("How do you feel about speaking in front of others or giving a presentation? (1 = Very Uncomfortable, 5 = Very Comfortable)", value=3, min_value=1, max_value=5)
    if st.button("Next"):
        st.session_state.question_number = 3


def show_question_3():
    st.subheader("Question 3")
    st.write("Question 3: What is your favorite food?")


if st.session_state.question_number == 1:
    show_question_1()
elif st.session_state.question_number == 2:
    show_question_2()
elif st.session_state.question_number == 3:
    show_question_3()

