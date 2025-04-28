# streamlit_app.py
import streamlit as st
from bedrock_bot import BedrockRAGBot

# Initialize bot outside tabs so it persists across navigation
bot = BedrockRAGBot()

# Page configuration
st.set_page_config(page_title="Bedrock RAG Chat", layout="wide")

# Apply empty (white) background
st.markdown(
    """
    <style>
    .stApp {background-color: lightblue;}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
tabs = ["Chat", "Settings"]
selected_tab = st.sidebar.radio("Navigation", tabs)

# Common chat interface
def chat_interface():
    st.header("AI Chat with Bedrock RAG Bot")
    user_input = st.text_input("Your question:", key="input")
    if st.button("Send", key="send"):
        with st.spinner("Thinking..."):
            response = bot.rag_query(user_input)
        st.text_area("Response", value=response, height=200)

# Render based on selected tab
if selected_tab == "Chat":
    chat_interface()
elif selected_tab == "Settings":
    st.header("Settings")
    api_key = st.text_input("AWS API Key", value=bot.api_key or "", type="password")
    region = st.text_input("AWS Region", value=bot.region)
    model_id = st.text_input("Model ID", value=bot.model_id)
    if st.button("Update Settings"):
        bot.update_credentials(api_key, region)
        bot.model_id = model_id
        st.success("Settings updated!")