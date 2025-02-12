import streamlit as st
import os
from dotenv import load_dotenv
import groq
import time

# Load environment variables
load_dotenv()

# Get Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Groq API key is missing! Please set it in your environment variables.")
    st.stop()

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Streamlit app config
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("Chatbot (Groq)")

# Function to get response from Groq with streaming
def get_response_stream(user_query, chat_history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # Append chat history
    for message in chat_history:
        role = "user" if message["role"] == "Human" else "assistant"
        messages.append({"role": role, "content": message["content"]})

    # Add user query
    messages.append({"role": "user", "content": user_query})

    # Stream response from Groq API
    response_stream = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        top_p=1.0,
        stream=True  # Enable streaming
    )

    for chunk in response_stream:
        time.sleep(0.1)
        yield chunk.choices[0].delta.content or ""  # Stream content

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "AI", "content": "Hello, I am a bot. How can I help you?"}
    ]

# Display chat history
for message in st.session_state.chat_history:
    role = "AI" if message["role"] == "AI" else "User"
    with st.chat_message(role):
        st.write(message["content"])

# User input
user_query = st.chat_input("Type your message here...")
if user_query:
    # Store user message
    st.session_state.chat_history.append({"role": "Human", "content": user_query})
    
    with st.chat_message("User"):
        st.markdown(user_query)

    # Create AI message placeholder for streaming
    with st.chat_message("AI"):
        response_container = st.empty()  # Placeholder for streaming response
        response_text = ""

        for chunk in get_response_stream(user_query, st.session_state.chat_history):
            response_text += chunk
            response_container.markdown(response_text)  # Update UI dynamically

    # Store AI response in chat history
    st.session_state.chat_history.append({"role": "AI", "content": response_text})
