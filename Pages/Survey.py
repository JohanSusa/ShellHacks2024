import os
import streamlit as st
import google.generativeai as genai

# Load the Gemini API key from environment variables for security
GEMINI_API_KEY = os.getenv("AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw")
genai.configure(api_key=GEMINI_API_KEY)

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
if "current_challenge" not in st.session_state:
    st.session_state.current_challenge = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# Function to get a response from the Gemini API using generative AI
def get_gemini_response(score):
    try:
        model = genai.models.GenerativeModel("gemini-1.5-flash")
        system_instructions = """You are an AI assistant helping people overcome social anxiety through exposure therapy. 
        The user will provide their score on a social skills assessment ranging from 10 (low) to 50 (high).
        Based on their score, provide a suitable social challenge that is safe, clear, and promotes skill-building. 
        Tailor the challenge to the user's skill level. 
        Ensure the challenge is achievable but slightly pushes their boundaries to encourage growth."""

        # Determine the prompt based on the score range
        if 10 <= score <= 17:
            prompt = "Give me a random 1-2 sentence social challenge for someone with extreme social anxiety."
        elif 18 <= score <= 25:
            prompt = "Give me a random 1-2 sentence social challenge for someone with severe social anxiety."
        elif 26 <= score <= 33:
            prompt = "Give me a random 1-2 sentence social challenge for someone with moderate social anxiety."
        elif 34 <= score <= 41:
            prompt = "Give me a random 1-2 sentence social challenge for someone with mild social anxiety."
        else:  # 42 <= score <= 50
            prompt = "Give me a random 1-2 sentence social challenge for someone with no social anxiety."

        response = model.generate_content(prompt, system_instructions=system_instructions)
        return response.text
    except Exception as e:
        st.error(f"Error fetching challenge: {e}")
        return "Could not retrieve a challenge. Please try again later."


# Streamlit app layout
st.title("Your Social Challenge Journey")

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
            score = options.index(selected_option) + 1
            st.session_state.score += score
            st.session_state.current_question_index += 1

# Challenge section (after all questions are answered)
elif st.session_state.current_question_index >= len(questions):
    score = st.session_state.score
    st.write(f"Your social skills score: {score}")

    # Get or generate a new challenge
    if st.session_state.current_challenge is None:
        with st.spinner('Fetching your challenge...'):
            st.session_state.current_challenge = get_gemini_response(score)

    st.subheader("Today's Challenge:")
    st.write(st.session_state.current_challenge)

    if st.button("Mark as Complete"):
        st.session_state.completed_challenges.append(st.session_state.current_challenge)
        st.session_state.current_challenge = None

    st.subheader("Completed Challenges:")
    st.write(st.session_state.completed_challenges)

# Option to restart the quiz
if st.button("Restart"):
    st.session_state.score = 0
    st.session_state.completed_challenges = []
    st.session_state.current_challenge = None
    st.session_state.current_question_index = 0