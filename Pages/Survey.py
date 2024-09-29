import streamlit as st
import google.generativeai as genai

#API key "AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw"
genai.configure(api_key="AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw")
model = genai.GenerativeModel("gemini-1.5-flash")

# Questions and their corresponding button labels
questions = {
    "How do you feel when meeting new people?": ["Very uncomfortable", "Uncomfortable", "Neutral", "Comfortable", "Very comfortable"],
    "How do you feel about speaking in front of others or giving a presentation?": ["Very uncomfortable", "Uncomfortable", "Neutral", "Comfortable", "Very comfortable"],
    "Do you ever experience physical symptoms (e.g., sweating, shaking, or a racing heart) in social situations?": ["Always", "Often", "Sometimes", "Rarely", "Never"],
    "How do you feel when attending social events like parties or networking events?": ["Very uncomfortable", "Uncomfortable", "Neutral", "Comfortable", "Very comfortable"],
    "I find it easy to read social cues, like body language and tone of voice.": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
    "I find it easy to share personal stories or experiences in a group.": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
    "I feel comfortable asking strangers for help (e.g., directions, advice).": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
    "I feel comfortable in social situations where I might not know many people.": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
    "I feel confident initiating conversations in work or professional settings.": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
    "I find it easy to make and maintain eye contact during conversations.": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
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
#hours spend 2
def get_gemini_response(score):
    try:
        prompt = ""
        if 10 <= score <= 17:
            prompt = "Give me a random 1-2 sentence social challenge for someone with extreme social anxiety."
        elif 18 <= score <= 25:
            prompt = "Give me a random 1-2 sentence social challenge for someone with severe social anxiety."
        elif 26 <= score <= 33:
            prompt = "Give me a random 1-2 sentence social challenge for someone with moderate social anxiety."
        elif 34 <= score <= 41:
            prompt = "Give me a random 1-2 sentence social challenge for someone with mild social anxiety."
        else:
            prompt = "Give me a random 1-2 sentence social challenge for someone with no social anxiety."

        # Fetch response from the API
        #hours spend (3)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error fetching challenge: {e}")
        return "Could not retrieve a challenge. Please try again later."

# Add custom CSS for button styling
st.markdown("""
    <style>
    .button-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;  /* Adjust the gap between buttons */
        justify-content: center;
    }
    .styled-button {
        padding: 12px 24px;  /* Slightly increase padding to make buttons wider */
        font-size: 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
    }
    .styled-button:hover {
        background-color: #4CAF50; /* Change to desired hover color */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Your Social Challenge Journey")

# progress bar
progress = st.progress(st.session_state.current_question_index / len(questions))

# Function to handle button clicks and update the score & question index
def handle_button_click(option):
    score = questions[current_question].index(option) + 1
    st.session_state.score += score
    st.session_state.current_question_index += 1

# Assessment and Challenge sections combined into one main area
#hours spend (4)
with st.container():  # Enclose both sections in a single container

    if st.session_state.current_question_index < len(questions):
        current_question, options = list(questions.items())[st.session_state.current_question_index]

        # Chat-like interaction
        with st.chat_message("assistant"):
            st.markdown(current_question)

        # Button interaction with callback
        with st.chat_message("user"):
            cols = st.columns([1] * len(options))
            for i, option in enumerate(options):
                with cols[i]:
                    st.button(option, key=f"button_{option}", on_click=handle_button_click, args=(option,))

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

            # Fetch a new challenge immediately
            with st.spinner('Fetching a new challenge...'):
                st.session_state.current_challenge = get_gemini_response(st.session_state.score)

        st.subheader("Completed Challenges:")
        st.write(st.session_state.completed_challenges)

# restart the quiz (outside the main container)
if st.button("Restart"):
    st.session_state.score = 0
    st.session_state.completed_challenges = []
    st.session_state.current_challenge = None
    st.session_state.current_question_index = 0