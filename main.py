import os
from dotenv import load_dotenv
import streamlit as st
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('rate', 150)

def sptext():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.write('Listening...')
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            st.write('Recognizing...')
            data = recognizer.recognize_google(audio)
            st.write(f'Recognized: {data}')
            return data.lower()
    except sr.UnknownValueError:
        st.write("Couldn't understand the message.")
        return ""
    except sr.RequestError as e:
        st.write(f'Error: {e}')
        return ""
    except Exception as e:
        st.write(f'An Error Occurred: {e}')
        return ""

def speechtx(text):
    try:
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except RuntimeError as e:
        st.write(f'Error: {e}')

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    full_response = ""
    for chunk in response:
        full_response += chunk.text
    return full_response

st.set_page_config(page_title='Voice Assistant Jarvis with GEMINI API')
st.header('Voice Assistant Jarvis')

# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

mode = st.radio('Select Interaction Mode:', ('Voice', "Text"))

if mode == 'Voice':
    if st.button('Ask Jarvis'):
        speechtx('Hello, I am Jarvis active for your command!')
        voice_input = sptext()
        if voice_input:
            st.write(f'You: {voice_input}')
            response = get_gemini_response(voice_input)
            speechtx(response)
            st.write(f'Jarvis: {response}')

elif mode == 'Text':
    input_text = st.text_input('You: ', key='text_input')
    if st.button('Ask'):
        response = get_gemini_response(input_text)
        st.write(f'Bot: {response}')