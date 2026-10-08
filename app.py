import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title='My AI Chat', layout='centered')

st.title("🤖 The Groq Chatbot")
st.write("A fully integrated, memory-enabled AI assistant.")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Configuration")

    user_api_key = st.text_input(
        'Enter the Groq API Key:',
        type='password'
    )

    st.info('Your key is required to wake up the AI Brain')

    # System Prompt / Persona
    persona = st.text_area(
        "System Prompt:",
        value="You are a helpful assistant."
    )

    # Reset button
    if st.button("Reset Chat & Apply Persona"):
        st.session_state.messages = []
        st.rerun()


# ---------------- MEMORY VAULT ----------------
if 'messages' not in st.session_state:
    st.session_state.messages = []


# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages:

    # Don't display the system message in the chat UI
    if msg['role'] != 'system':
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])


# ---------------- CHAT INPUT ----------------
if user_query := st.chat_input('Say something to the AI...'):

    if not user_api_key:
        st.error('Please enter your API key in the sidebar first!')

    else:

        # Store user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_query
        })

        # Display user message
        with st.chat_message('user'):
            st.markdown(user_query)

        # ---------------- SYSTEM PROMPT INJECTOR ----------------
        # Make sure the system prompt is the first message
        if not st.session_state.messages or st.session_state.messages[0]['role'] != 'system':

            st.session_state.messages.insert(
                0,
                {
                    'role': 'system',
                    'content': persona
                }
            )

        # ---------------- INITIALISE AI BRAIN ----------------
        llm = ChatGroq(
            model='openai/gpt-oss-20b',
            temperature=0.7,
            api_key=user_api_key
        )

        # ---------------- GET AI RESPONSE ----------------
        with st.spinner('AI is thinking....'):

            response = llm.invoke(
                st.session_state.messages
            )

            bot_answer = response.content

        # Store assistant response
        st.session_state.messages.append({
            'role': 'assistant',
            'content': bot_answer
        })

        # Display assistant response
        with st.chat_message('assistant'):
            st.markdown(bot_answer)
