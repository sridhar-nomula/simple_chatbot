import streamlit as st
import requests
import time

# Function to send message to Rasa and receive bot response
def send_message_to_rasa(message):
    rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"
    response = requests.post(rasa_endpoint, json={"sender": "user", "message": message})
    return response.json()

# Streamed response generator
def response_generator(message):
    response = send_message_to_rasa(message)
    for r in response:
        yield r['text']
        time.sleep(0.05)


st.title("Personal Bot Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("type your ask here"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        for response_text in response_generator(prompt):
            st.write(response_text)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})