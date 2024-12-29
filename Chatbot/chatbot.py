import streamlit as st
from PIL import Image
import time
import numpy as np
import random
from groq import Groq
import json

st.title("Chatbot")
st.chat_message("ai").text("Hey there, I'm WIAN - What's In A Name 👋")

message_back = """
<style>
.stAppHeader {display : none;}
.st-emotion-cache-h4xjwg {display : none;}
.e10jh26i0 {display : none;}
header {visibility : hidden;}
#chatbot {visibility : visible; width : 100%; font-size : 2.5rem; margin : 0; text-align : center; font-weight : 100; position : fixed; top : 0; left : 50%; transform : translate(-50%,0); z-index : 1; background-color : black;}
.st-emotion-cache-w9jsfw {color : black; font-size : 1.1em;}
.e1v02oy80 {color : white;}
.st-emotion-cache-janbn0 {background-color : rgb(115, 115, 115); box-shadow : inset 4px 4px 10px 0 rgba(0,0,0, 0.1), inset -4px -4px 10px 0 rgba(0,0,0, 0.1); border : 1.5px solid rgba(255,255,255,0.5)}
.st-emotion-cache-4oy321 {background-color : rgb(57, 59, 56); box-shadow : inset 2px 2px 8px 0 rgba(0,0,0, 0.1), inset -2px -2px 8px 0 rgba(0,0,0, 0.1); border : 1.5px solid rgba(255,255,255,0.5)}
</style>
"""
st.markdown(message_back,unsafe_allow_html = True)




if "messages" not in st.session_state :     # Initializing the messages history
    st.session_state.messages = []

# if "responses" not in st.session_state :     # Initializing the response history
#     st.session_state.responses = []    
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-70b-8192"



avatar_img = Image.open('../sanjana_vector2.png')
for message in st.session_state.messages : 
    if message['role'] == 'user':
        st.chat_message(message['role'],avatar = avatar_img).text(message['content'])
    else : 
        st.chat_message(message['role']).text(message['content'])    



# def response_generator() :
#     response = random.choice(
#         [
#             "Hello there human!",
#             "Yo, I'm a robot...",
#             "Hey there, how are you?",
#             "Hello! How can I help you today?"
#         ]
#     )
#     for letter in response :
#         yield letter + ""   # Returns one letter at a time
#         time.sleep(0.05)


client = Groq(api_key = st.secrets["GROQ_API_KEY"])


if prompt := st.chat_input("What is up?") :
    st.session_state.messages.append({"role" : "user",'content' : prompt})
    st.chat_message("user",avatar = avatar_img).text(prompt)

    # response = np.random.randn(1)
    # with st.chat_message("assistant"):
    #     response = st.write_stream(response_generator())    # Writing one letter at a time, in the chat_message section of Assistant
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(    
            model = st.session_state["groq_model"],
            messages = [
                {"role" : m["role"], "content" : m["content"]} for m in st.session_state.messages
            ]
        )
        
        st.write(stream.choices[0].message.content)
    st.session_state.messages.append({"role" : "assistant","content" : stream.choices[0].message.content})