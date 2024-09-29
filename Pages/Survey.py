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
/* Button Container Styling */
.stButton, .button-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center; /* Center the buttons horizontally */
    gap: 1rem; /* Space between buttons */
    margin-bottom: 20px; /* Add spacing below the buttons */
}

/* Button Styling */
.stButton button, .styled-button {
    padding: 14px 24px; /* Increased padding for a more substantial button */
    font-size: 16px;
    font-weight: 500; /* Slightly thicker font for better readability */
    border: none;
    border-radius: 8px; /* Softer corner radius for modern look */
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease; /* Smooth transition and slight animation */
    width: calc(100% / 5 - 1rem); /* 5 buttons per row with dynamic resizing */
    min-width: 150px; /* Minimum width to prevent too small buttons */
    max-width: 200px; /* Max width for larger screens */
    box-sizing: border-box;
    background-color: #f5f5f5; /* Light background for neutral look */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Soft shadow for depth */
    height:100px;
}

/* Button Hover Effect */
.stButton button:hover, .styled-button:hover {
    background-color: #4CAF50; /* Highlight color on hover */
    color: #fff; /* Text color change */
    transform: scale(1.05); /* Slight zoom effect */
    box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4); /* More prominent shadow on hover */
}

/* Active Button Effect */
.stButton button:active, .styled-button:active {
    transform: scale(1); /* Reset zoom on click */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Reduced shadow on click */
}



/* Main Content Area Styling */
.main .block-container {
    max-width: 1000px; /* Increase max width for larger screens */
    padding: 2rem 1.5rem; /* Adjust padding for better spacing */
    margin: 0 auto; /* Center the main content */
    background-color: #f9f9f9; /* Light background for main area */
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* Light shadow for main content */
}

/* Responsive Button Styling */
@media (max-width: 768px) {
    .stButton button, .styled-button {
        width: calc(100% / 2 - 1rem); /* 2 buttons per row on smaller screens */
        min-width: 120px; /* Adjust minimum width for smaller screens */
    }
}

@media (max-width: 480px) {
    .stButton button, .styled-button {
        width: 100%; /* Full-width buttons on extra small screens */
        margin-bottom: 10px; /* Space between full-width buttons */
    }
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