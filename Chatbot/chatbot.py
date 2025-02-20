import streamlit as st
from PIL import Image
import time
# import numpy as np
# import random
from groq import Groq


message_back = """
<style>
.stAppHeader {display : none;}
.st-emotion-cache-h4xjwg {display : none;}
.e10jh26i0 {display : none;}
header {visibility : hidden;}
#chatbot {visibility : visible; width : 100%; font-size : 2.5rem; margin : 0; text-align : center; font-weight : 100; position : fixed; top : 0; left : 50%; transform : translate(-50%,0); z-index : 1; background-color : black;}
.st-emotion-cache-w9jsfw {color : black;}
.e1v02oy80 {color : white;}
.st-emotion-cache-janbn0 {background-color : rgba(139, 139, 139, 0.78); box-shadow : inset 4px 4px 10px 0 rgba(0,0,0, 0.1), inset -4px -4px 10px 0 rgba(0,0,0, 0.1); border : 1.5px solid rgba(255,255,255,0.5)}
.st-emotion-cache-4oy321 {background-color : rgb(48, 50, 48); box-shadow : inset 2px 2px 8px 0 rgba(0,0,0, 0.1), inset -2px -2px 8px 0 rgba(0,0,0, 0.1); border : 1.5px solid rgba(255,255,255,0.5)}
.stAlertContainer {padding : 4px 6px 4px 6px; width : fit-content;}
.e1obcldf2 {padding : 0 7px 0 7px; position : relative; left : 50%; transform : translate(-50%,0); border : 0.2px solid white; background-color : rgb(225, 225, 225); color : black; box-shadow : inset 1px 1px 10px 0 rgba(0, 0, 0, 0.2), inset -1px -1px 10px 0 rgba(0, 0, 0, 0.2); margin-bottom : 5px;}
.st-emotion-cache-atejua p {font-size : 0.9em;} 
.e1obcldf2:hover {color : white; background-color : rgb(77, 77, 77); border : 0.2px solid white; transition : 0.2s; box-shadow : inset 1px 1px 10px 0 rgba(0, 0, 0, 0.2), inset -1px -1px 10px 0 rgba(0, 0, 0, 0.2);}
.e1obcldf2:focus:not(:active) {color : white; background-color : rgb(64, 64, 64); border : 0.2px solid rgb(177, 177, 177);}
.e121c1cl3 {display : none;}
div[data-testid=stToast] {position : fixed; bottom:10px; right:50%; transform:translate(50%,0); background-color:rgb(69, 69, 69);color:white;}
</style>   
"""
st.markdown(message_back,unsafe_allow_html = True)

avatar_ai = Image.open('Ai_avatar.png')
prompt = st.chat_input("What is up?")
st.title("Chatbot")
time.sleep(0.4)
st.chat_message("assistant",avatar = avatar_ai).text("Hey there! I'm WIAN - What's In A Name 👋")
time.sleep(0.4)
st.chat_message("assistant",avatar = avatar_ai).text("What's on your mind today?")


client = Groq(api_key = st.secrets["GROQ_API_KEY"])
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-70b-8192"


if "messages" not in st.session_state :     # Initializing the messages history
    st.session_state.messages = [{'role' : 'user', 'content' : 'The developer of this chatbot has given you the name WIAN - What\'s In A Name.'}]

# if "responses" not in st.session_state :     # Initializing the response history
#     st.session_state.responses = []    



avatar_img = Image.open('vector.png')
for message in st.session_state.messages : 
    if message['role'] == 'user':
        if message['content'] != "The developer of this chatbot has given you the name WIAN - What\'s In A Name.":
            st.chat_message(message['role'],avatar = avatar_img).text(message['content'])
    else : 
        st.chat_message(message['role'],avatar = avatar_ai).text(message['content'])    



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



def write_response(res) :
    for letter in res:
        yield letter + ""
        time.sleep(0.018)
        

if prompt :
    time.sleep(0.1)
    st.session_state.messages.append({"role" : "user",'content' : prompt})
    st.chat_message("user",avatar = avatar_img).text(prompt)

    # response = np.random.randn(1)
    # with st.chat_message("assistant"):
    #     response = st.write_stream(response_generator())    # Writing one letter at a time, in the chat_message section of Assistant
    time.sleep(0.08)
    with st.chat_message("assistant",avatar = avatar_ai):
        try:
            stream = client.chat.completions.create(    
                model = st.session_state["groq_model"],
                messages = [
                    {"role" : m["role"], "content" : m["content"]} for m in st.session_state.messages
                ]
            )
            response = st.write_stream(write_response(stream.choices[0].message.content))   
            st.session_state.messages.append({"role" : "assistant","content" : stream.choices[0].message.content})
        except Exception as e :
            st.error("⚠️ Oops! Something went wrong...")     
            st.session_state.messages.append({"role" : "assistant","content" : "⚠️ Something went wrong"})      

if st.button("Clear Chat"):
    if st.session_state.messages == [{'role' : 'user', 'content' : 'The developer of this chatbot has given you the name WIAN - What\'s In A Name.'}]:
        st.toast("Nothing to clear")       
    else:
        st.toast("Clearing the chat...")          
    time.sleep(0.08)
    st.session_state.clear()
    st.rerun()