import os
import streamlit as st
import google.generativeai as genai

# Load the Gemini API key from environment variables for security
genai.configure(api_key="AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw")
model = genai.GenerativeModel("gemini-1.5-flash")



# Questions and their corresponding slider labels
questions = {
    "How do you feel when meeting new people?": ["Very uncomfortable", "Uncomfortable", "Neutral", "Comfortable",
                                                 "Very comfortable"],
    "How do you feel about speaking in front of others or giving a presentation?": ["Very uncomfortable",
                                                                                    "Uncomfortable", "Neutral",
                                                                                    "Comfortable", "Very comfortable"],
    "Do you ever experience physical symptoms (e.g., sweating, shaking, or a racing heart) in social situations?": [
        "Always", "Often", "Sometimes", "Rarely", "Never"],
    "How do you feel when attending social events like parties or networking events?": ["Very uncomfortable",
                                                                                        "Uncomfortable", "Neutral",
                                                                                        "Comfortable",
                                                                                        "Very comfortable"],
    "I find it easy to read social cues, like body language and tone of voice.": ["Strongly disagree", "Disagree",
                                                                                  "Neutral", "Agree", "Strongly agree"],
    "I find it easy to share personal stories or experiences in a group.": ["Strongly disagree", "Disagree", "Neutral",
                                                                            "Agree", "Strongly agree"],
    "I feel comfortable asking strangers for help (e.g., directions, advice).": ["Strongly disagree", "Disagree",
                                                                                 "Neutral", "Agree", "Strongly agree"],
    "I feel comfortable in social situations where I might not know many people.": ["Strongly disagree", "Disagree",
                                                                                    "Neutral", "Agree",
                                                                                    "Strongly agree"],
    "I feel confident initiating conversations in work or professional settings.": ["Strongly disagree", "Disagree",
                                                                                    "Neutral", "Agree",
                                                                                    "Strongly agree"],
    "I find it easy to make and maintain eye contact during conversations.": ["Strongly disagree", "Disagree",
                                                                              "Neutral", "Agree", "Strongly agree"]
}

# In-memory storage for user data using session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "completed_challenges" not in st.session_state:
    st.session_state.completed_challenges = []
    #adding this to see if challenges will be saved



# check this
if "current_challenge" not in st.session_state:
    st.session_state.current_challenge = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "challenges" not in st.session_state:
    st.session_state.challenges = []
if "num_challenges" not in st.session_state:
    st.session_state.num_challenges = 0

# Function to get a response from the Gemini API using generative AI
# def get_gemini_response(score):
#     global prompt
#     try:
#
#         if 10 <= score <= 17:
#             prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
#                       'nonexistent level of social skills. separate each challenge with a "#". Also do not number '
#                       'the challenges.')
#
#         elif 18 <= score <= 25:
#             prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
#                       'low level of social skills. separate each challenge with a "#". Also do not number '
#                       'the challenges.')
#
#         elif 26 <= score <= 33:
#             prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
#                       'medium level of social skills. separate each challenge with a "#". Also do not number '
#                       'the challenges.')
#
#         elif 34 <= score <= 41:
#             prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
#                       'high level of social skills. separate each challenge with a "#". Also do not number '
#                       'the challenges.')
#
#         elif 42 <= score <= 50:
#             prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
#                       'extremely high/proficient level of social skills. separate each challenge with a "#". Also do '
#                       'not number the challenges.')
#
#
#
#         # Fetch response from the API using the correct method (generate or chat)
#
#         response = model.generate_content(prompt)
#
#         challenges = response.text.split('#')
#         challenges.pop(0)
#
#         st.write(challenges)
#
#         # response = genai.generate(
#         #     model="gemini-1.5-flash",
#         #     prompt=prompt,
#         #     system_instructions=system_instructions
#         # )
#
#         return challenges
#     except Exception as e:
#         st.error(f"Error fetching challenge: {e}")
#         return "Could not retrieve a challenge. Please try again later."


st.title("Your Social Challenge Journey")
# Streamlit app layout

# Show progress bar
progress = st.progress(st.session_state.current_question_index / len(questions))

# Assessment section (one question at a time)
if st.session_state.current_question_index < len(questions):
    current_question, options = list(questions.items())[st.session_state.current_question_index]

    # Chat-like interaction
    with st.chat_message("assistant"):
        st.markdown(current_question)

    # Get user's response using radio buttons
    with st.chat_message("user"):
        selected_option = st.radio("", options, index=2, key=f"question_{st.session_state.current_question_index}")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous") and st.session_state.current_question_index > 0:
            st.session_state.current_question_index -= 1
            st.session_state.score -= options.index(selected_option) + 1  # Adjust score when moving back
    with col2:
        if st.button("Next"):
            #check this
            score = options.index(selected_option)
            st.session_state.score += score
            st.session_state.current_question_index += 1

# Challenge section (after all questions are answered)
elif st.session_state.current_question_index >= len(questions):
    score = st.session_state.score
    st.write(f"Your social skills score: {score}")

    prompt = ""
    if 10 <= score <= 17:
        prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                  'nonexistent level of social skills. separate each challenge with a "#". Also do not number '
                  'the challenges.')

    elif 18 <= score <= 25:
        prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                  'low level of social skills. separate each challenge with a "#". Also do not number '
                  'the challenges.')

    elif 26 <= score <= 33:
        prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                  'medium level of social skills. separate each challenge with a "#". Also do not number '
                  'the challenges.')

    elif 34 <= score <= 41:
        prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                  'high level of social skills. separate each challenge with a "#". Also do not number '
                  'the challenges.')

    elif 42 <= score <= 50:
        prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                  'extremely high/proficient level of social skills. separate each challenge with a "#". Also '
                  'do not number the challenges.')

    if not st.session_state.challenges:
        response = model.generate_content(prompt)
        st.session_state.challenges = [challenge.strip() for challenge in response.text.split('#') if challenge.strip()]

    st.write(st.session_state.challenges)


    # challenges = response.text.split('#')




    # Get or generate a new challenge

    st.subheader("Today's Challenge:")
    if st.session_state.current_challenge is None:
        st.session_state.current_challenge = st.session_state.challenges[0]
        st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]

    st.write(st.session_state.current_challenge)



    #check if thee are more challenges left
    if st.session_state.num_challenges <= 14:


        if st.button("Mark as Complete"):
            # append current challenge to the completed challenges


            # move to the next challenge

            #check if more challenges are available, if not, set a message
            # if st.session_state.num_challenges < len(st.session_state.challenges):
            st.session_state.num_challenges += 1
            st.session_state.completed_challenges.append(st.session_state.current_challenge)
            st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]
            # st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]
                # st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]
        # else:
        #     st.session_state.current_challenge = "You've completed all the challenges!"


# #double check this
    st.subheader("Completed Challenges:")
    st.write(st.session_state.completed_challenges)




# Option to restart the quiz
if st.button("Restart"):
    st.session_state.score = 0
    st.session_state.completed_challenges = []
    st.session_state.current_challenge = None
    st.session_state.current_question_index = 0
