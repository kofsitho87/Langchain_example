import streamlit as st
import requests
import json
# from streamlit_chat import message

model = "llama2:13b"
# model = "llama2"
# model = "mistral"
# model = "openhermes"

def request_chat(prompt):
  # API endpoint
  url = 'http://localhost:11434/api/generate'
  # url = 'http://localhost:11434/api/chat'

  # Request payload
  payload = {
      'model': model,
      'prompt': prompt,
      # "messages": [{
      #     "role": "user",
      #     "content": prompt
      # }],
      "stream": True
  }

  # Making a POST request
  response = requests.post(url, json=payload, stream=True)
  return response

st.title("ChatBot")

st.header("🤖Dan's ChatBot (Demo)")
 
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?", disabled=False):
    # st.chat_input(disabled=True)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = request_chat(prompt)
        for raw_rsvp in response.iter_lines():
            # print("##1", raw_rsvp)
            if raw_rsvp:
                rsvp = json.loads(raw_rsvp)
                content = rsvp["response"]
                # content = rsvp["message"]["content"]
                full_response += (content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})



