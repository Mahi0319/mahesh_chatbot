import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mahesh AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# 3. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(124, 58, 237, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 95% 5%,
                rgba(37, 99, 235, 0.14),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #07080d 0%,
                #0b0d14 50%,
                #080a10 100%
            );

        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 25px;
        padding-bottom: 100px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0d0f17 0%,
                #090b11 100%
            );

        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #f8fafc !important;
        letter-spacing: -0.025em;
    }

    p {
        color: #94a3b8;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 19, 28, 0.72);

        border: 1px solid rgba(255, 255, 255, 0.08);

        border-radius: 20px;

        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.20),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;

        min-height: 42px;

        background: rgba(255, 255, 255, 0.035) !important;

        color: #e2e8f0 !important;

        border: 1px solid rgba(255, 255, 255, 0.09) !important;

        border-radius: 11px !important;

        font-weight: 600 !important;

        transition:
            transform 0.18s ease,
            background 0.18s ease,
            border-color 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        background: rgba(124, 58, 237, 0.14) !important;

        border-color: rgba(139, 92, 246, 0.45) !important;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background: #11131b !important;

        border: 1px solid rgba(255, 255, 255, 0.09) !important;

        border-radius: 10px !important;

        color: #f8fafc !important;
    }


    /* ========================================================
       SLIDER
       ======================================================== */

    div[data-testid="stSlider"] label {
        color: #cbd5e1 !important;
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    div[data-testid="stChatMessage"] {
        border-radius: 18px;

        margin-bottom: 12px;

        padding: 8px 12px;
    }

    div[data-testid="stChatMessage"] p {
        color: #e2e8f0;

        line-height: 1.75;

        font-size: 15px;
    }

    div[data-testid="stChatMessage"] code {
        background: rgba(255, 255, 255, 0.07);

        border-radius: 6px;

        padding: 2px 6px;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    div[data-testid="stChatInput"] > div {
        background: #11131b !important;

        border: 1px solid rgba(255, 255, 255, 0.10) !important;

        border-radius: 18px !important;

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.30);
    }

    div[data-testid="stChatInput"] textarea {
        background: transparent !important;

        color: #f8fafc !important;

        border: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.025);

        border: 1px solid rgba(255, 255, 255, 0.07);

        border-radius: 14px;

        padding: 12px 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.025);

        border: 1px solid rgba(255, 255, 255, 0.07);

        border-radius: 12px;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-color: rgba(255, 255, 255, 0.07) !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "response_style" not in st.session_state:
    st.session_state.response_style = "Professional"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.4


# ============================================================
# 5. GROQ CLIENT
# ============================================================

@st.cache_resource
def get_groq_client(api_key):
    return Groq(api_key=api_key)


# ============================================================
# 6. SYSTEM PROMPT
# ============================================================

def get_system_prompt(style):

    if style == "Friendly":

        style_instruction = """
        Be friendly, natural and conversational.
        Explain difficult concepts using simple language.
        """

    elif style == "Concise":

        style_instruction = """
        Be concise and direct.
        Give the important information without unnecessary repetition.
        """

    else:

        style_instruction = """
        Be professional, accurate and well structured.
        Give useful explanations and examples when appropriate.
        """

    return f"""
You are Mahesh AI, a professional AI assistant.

{style_instruction}

General instructions:

1. Answer the user's actual question.
2. Do not invent information.
3. If you are uncertain, clearly say so.
4. Use Markdown when it improves readability.
5. Use headings and bullet points when useful.
6. For programming questions, provide clean and correct code.
7. Explain programming concepts clearly.
8. Do not unnecessarily repeat the user's question.
9. Keep the conversation natural.
10. Remember the context of the current conversation.
"""


# ============================================================
# 7. STREAM GROQ RESPONSE
# ============================================================

def get_streaming_response():

    client = get_groq_client(GROQ_API_KEY)

    api_messages = [
        {
            "role": "system",
            "content": get_system_prompt(
                st.session_state.response_style
            ),
        }
    ]

    api_messages.extend(
        st.session_state.messages
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=api_messages,
        temperature=st.session_state.temperature,
        max_completion_tokens=2048,
        stream=True,
    )

    for chunk in response:

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:
            yield content


# ============================================================
# 8. ERROR MESSAGE
# ============================================================

def show_api_error(error):

    error_text = str(error)

    if "401" in error_text or "authentication" in error_text.lower():

        st.error(
            "❌ Groq authentication failed. "
            "Please check your GROQ_API_KEY."
        )

    elif "429" in error_text:

        st.error(
            "⚠️ Groq rate limit reached. "
            "Please wait a moment and try again."
        )

    elif "model" in error_text.lower():

        st.error(
            "❌ The selected Groq model is unavailable."
        )

    elif "api key" in error_text.lower():

        st.error(
            "❌ Groq API key is missing or invalid."
        )

    else:

        st.error(
            "❌ Something went wrong while generating the response."
        )

        with st.expander("Technical Details"):
            st.code(error_text)


# ============================================================
# 9. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 Mahesh AI")

    st.caption(
        "Professional Groq-powered AI assistant"
    )

    st.divider()

    # API status

    if GROQ_API_KEY:

        st.success("● Groq API Connected")

    else:

        st.error("● Groq API Key Missing")

    st.write("")

    # New chat

    if st.button(
        "＋  New Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    # Settings

    st.markdown("### ⚙️ AI Settings")

    response_style = st.selectbox(
        "Response Style",
        [
            "Professional",
            "Friendly",
            "Concise",
        ],
        index=[
            "Professional",
            "Friendly",
            "Concise",
        ].index(
            st.session_state.response_style
        ),
    )

    st.session_state.response_style = response_style

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.temperature),
        step=0.1,
    )

    st.session_state.temperature = temperature

    st.divider()

    # Model

    st.markdown("### 🤖 Model")

    st.write("GPT-OSS 120B")

    st.caption(
        "Fast inference powered by Groq"
    )

    st.divider()

    # Statistics

    st.markdown("### 📊 Chat Stats")

    st.metric(
        "Messages",
        len(st.session_state.messages),
    )

    st.write("")

    # Download

    if st.session_state.messages:

        conversation = []

        for message in st.session_state.messages:

            if message["role"] == "user":

                role = "YOU"

            else:

                role = "MAHESH AI"

            conversation.append(
                f"{role}:\n{message['content']}"
            )

        conversation_text = (
            "\n\n"
            + "\n\n".join(conversation)
            + "\n"
        )

        st.download_button(
            label="⬇ Download Conversation",
            data=conversation_text,
            file_name="mahesh_ai_conversation.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# 10. MAIN HEADER
# ============================================================

st.title("🤖 Mahesh AI")

st.caption(
    "Your intelligent AI assistant for coding, learning, "
    "projects, research and everyday questions."
)

if GROQ_API_KEY:

    st.success(
        "● ONLINE  •  GROQ AI  •  GPT-OSS 120B"
    )

else:

    st.warning(
        "● OFFLINE  •  Add your GROQ_API_KEY to the .env file"
    )


# ============================================================
# 11. WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown("### What can I help you with?")

    st.caption(
        "Choose an example or type your own question below."
    )

    col1, col2 = st.columns(2)

    # Programming

    with col1:

        with st.container(border=True):

            st.markdown("### 💻 Programming")

            st.caption(
                "Explain Python OOP with a simple example."
            )

            programming_clicked = st.button(
                "Try Example →",
                key="programming_example",
                use_container_width=True,
            )

    # Learning

    with col2:

        with st.container(border=True):

            st.markdown("### 🧠 Learning")

            st.caption(
                "Explain Artificial Intelligence in simple words."
            )

            learning_clicked = st.button(
                "Try Example →",
                key="learning_example",
                use_container_width=True,
            )

    col3, col4 = st.columns(2)

    # Projects

    with col3:

        with st.container(border=True):

            st.markdown("### 🚀 Projects")

            st.caption(
                "Give me innovative Python project ideas."
            )

            projects_clicked = st.button(
                "Try Example →",
                key="projects_example",
                use_container_width=True,
            )

    # Interview

    with col4:

        with st.container(border=True):

            st.markdown("### 📚 Interview")

            st.caption(
                "Start a Python technical interview."
            )

            interview_clicked = st.button(
                "Try Example →",
                key="interview_example",
                use_container_width=True,
            )


else:

    # Define variables so they always exist

    programming_clicked = False
    learning_clicked = False
    projects_clicked = False
    interview_clicked = False


# ============================================================
# 12. DETERMINE NEW PROMPT
# ============================================================

new_prompt = None

if programming_clicked:

    new_prompt = (
        "Explain Python OOP in simple words "
        "with a practical example."
    )

elif learning_clicked:

    new_prompt = (
        "Explain Artificial Intelligence "
        "in simple words with a real-world example."
    )

elif projects_clicked:

    new_prompt = (
        "Give me 5 innovative Python project ideas "
        "suitable for a 3rd year CSE student."
    )

elif interview_clicked:

    new_prompt = (
        "Act as an experienced Python interviewer. "
        "Start a beginner-level technical interview. "
        "Ask me one question at a time."
    )


# ============================================================
# 13. DISPLAY EXISTING CONVERSATION
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        # IMPORTANT:
        # "user" is a valid Streamlit avatar type.

        with st.chat_message(
            "user",
            avatar="user",
        ):

            st.markdown(
                message["content"]
            )

    elif message["role"] == "assistant":

        # IMPORTANT:
        # "assistant" is a valid Streamlit avatar type.

        with st.chat_message(
            "assistant",
            avatar="assistant",
        ):

            st.markdown(
                message["content"]
            )


# ============================================================
# 14. CHAT INPUT
# ============================================================

chat_prompt = st.chat_input(
    "Message Mahesh AI..."
)

if chat_prompt:

    new_prompt = chat_prompt.strip()


# ============================================================
# 15. PROCESS NEW PROMPT
# ============================================================

if new_prompt:

    if not GROQ_API_KEY:

        st.error(
            "❌ Groq API key is missing. "
            "Please configure your .env file."
        )

    elif not new_prompt.strip():

        st.warning(
            "Please enter a message."
        )

    else:

        # ----------------------------------------------------
        # Add user message
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": new_prompt,
            }
        )

        # ----------------------------------------------------
        # Display user message
        # ----------------------------------------------------

        with st.chat_message(
            "user",
            avatar="user",
        ):

            st.markdown(
                new_prompt
            )

        # ----------------------------------------------------
        # Generate AI response
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="assistant",
        ):

            response_area = st.empty()

            complete_response = ""

            try:

                for token in get_streaming_response():

                    complete_response += token

                    response_area.markdown(
                        complete_response + "▌"
                    )

                # Final response

                response_area.markdown(
                    complete_response
                )

                # Save assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": complete_response,
                    }
                )

            except Exception as error:

                # Remove user message if API failed

                if (
                    st.session_state.messages
                    and st.session_state.messages[-1]["role"]
                    == "user"
                ):

                    st.session_state.messages.pop()

                show_api_error(error)


# ============================================================
# 16. FOOTER
# ============================================================

st.divider()

st.caption(
    "Mahesh AI  •  Powered by Groq  •  Built with Python + Streamlit"
)