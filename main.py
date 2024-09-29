import streamlit as st
import google.generativeai as genai

# API key "AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw"
genai.configure(api_key="AIzaSyCyXkpduy3uFH_gQdJBMJO4pR2ZV3dVDQw")
model = genai.GenerativeModel("gemini-1.5-flash")
#hours spent (3)
# Questions and their corresponding button labels
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
#hours spent (3)

if "score" not in st.session_state:
    st.session_state.score = 0
if "completed_challenges" not in st.session_state:
    st.session_state.completed_challenges = []
if "current_challenge" not in st.session_state:
    st.session_state.current_challenge = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "challenges" not in st.session_state:
    st.session_state.challenges = []
if "num_challenges" not in st.session_state:
    st.session_state.num_challenges = 0
if "previous_score" not in st.session_state:
    st.session_state.previous_score = 0  # Store the previous score when going back

st.title("Your Social Challenge Journey")
#hours spent (3)


# Progress bar
progress = st.progress(st.session_state.current_question_index / len(questions))


# Function to handle button clicks and update the score & question index
def handle_button_click(option):
    score = questions[current_question].index(option) + 1
    st.session_state.previous_score = score
    st.session_state.score += score
    st.session_state.current_question_index += 1


def go_back():
    """Go back to the previous question or challenge"""
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1
        st.session_state.score -= st.session_state.previous_score  # Subtract the previous score


# Assessment and Challenge sections combined into one main area
#hours spent (2)

with st.container():

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
                    st.button(option, key=f"button_{option}_{st.session_state.current_question_index}",
                              on_click=handle_button_click, args=(option,))



# hours spent (4 :C)


    elif st.session_state.current_question_index >= len(questions):
        score = st.session_state.score
        st.write(f"Your social skills score: {score}")

        prompt = ""
        if 10 <= score <= 17:
            prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                      'nonexistent level of social skills. Separate each challenge with a "#". Also do not number '
                      'the challenges.')

        elif 18 <= score <= 25:
            prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                      'low level of social skills. Separate each challenge with a "#". Also do not number '
                      'the challenges.')

        elif 26 <= score <= 33:
            prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                      'medium level of social skills. Separate each challenge with a "#". Also do not number '
                      'the challenges.')

        elif 34 <= score <= 41:
            prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                      'high level of social skills. Separate each challenge with a "#". Also do not number '
                      'the challenges.')

        elif 42 <= score <= 50:
            prompt = ('Give me 15 different but specific 1-2 sentence social challenges for someone with a '
                      'extremely high/proficient level of social skills. Separate each challenge with a "#". Also '
                      'do not number the challenges.')

        if not st.session_state.challenges:
            response = model.generate_content(prompt)
            st.session_state.challenges = [challenge.strip() for challenge in response.text.split('#') if
                                           challenge.strip()]

        st.subheader("Today's Challenge:")
        if st.session_state.current_challenge is None:
            st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]

        st.write(st.session_state.current_challenge)

        # Add Mark as Complete and Skip Challenge buttons
        if st.session_state.num_challenges <= 14:

            if st.button("Mark as Complete", key="complete_button"):
                st.session_state.completed_challenges.append(st.session_state.current_challenge)
                st.session_state.num_challenges += 1
                st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]

            # Add Skip Challenge button
            if st.button("Skip Challenge", key="skip_button"):
                st.session_state.num_challenges += 1
                if st.session_state.num_challenges < len(st.session_state.challenges):
                    st.session_state.current_challenge = st.session_state.challenges[st.session_state.num_challenges]
                else:
                    st.session_state.current_challenge = None

        st.subheader("Completed Challenges:")
        st.write(st.session_state.completed_challenges)
# hours spent (4)

st.markdown("""
   <style>
/* Button Container Styling */
.stButton, .button-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center; /* Center horizontally */
    gap: 1rem; /* Space between buttons works? */
    margin-bottom: 20px; /* ?? */
}

/* Button Styling */
.stButton button, .styled-button {
    padding: 14px 24px; 
    font-size: 16px;
    font-weight: 500; /* Slightly thicker font for better readability */
    border: none;
    border-radius: 8px; 
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
    width: calc(100% / 5 - 1rem); 
    min-width: 150px; 
    max-width: 200px; 
    box-sizing: border-box;
    background-color: #y5f5f5; /* background */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* shadow */
    height:100px;
}

/* Button Hover Effect */
.stButton button:hover, .styled-button:hover {
    background-color: #4CAF50; /* color hover */
    color: #fff; /* Text color change */
    transform: scale(1.05); /* Slight zoom effect */
    box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4); 
}

/* Active Button Effect */
.stButton button:active, .styled-button:active {
    transform: scale(1); /* zoom clikc */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Reduced shadow */
}



/* Main Content Area Styling */
.main .block-container {
    max-width: 1000px; /* Increase max width for larger screens */
    padding: 2rem 1.5rem; 
    margin: 0 auto; 
    background-color: #g9f9f9; 
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* Light shadow content */
}

/* Responsive Button Styling */
@media (max-width: 768px) {
    .stButton button, .stpyled-button {
        width: calc(100% / 2 - 1rem); 
        min-width: 120px; 
    }
}

@media (max-width: 480px) {
    .stButton button, .styled-button {
        width: 100%; 
        margin-bottom: 10px; 
    }
}
</style>
""", unsafe_allow_html=True)
# Align "Back" and "Restart" buttons horizontally and show them only once
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.current_question_index > 0:
        st.button("Back", on_click=go_back, key="back_button")
with col2:
    st.button("Restart", on_click=lambda: (
        setattr(st.session_state, "score", 0),
        setattr(st.session_state, "completed_challenges", []),
        setattr(st.session_state, "current_challenge", None),
        setattr(st.session_state, "current_question_index", 0),
        setattr(st.session_state, "num_challenges", 0),
        setattr(st.session_state, "challenges", [])
    ), key="restart_button")
