import os  # Imports the os module to interact with the operating system (used for environment variables)
from dotenv import load_dotenv  # Imports load_dotenv to load environment variables from a .env file
import streamlit as st  # Imports Streamlit library for creating web-based UI
import pyttsx3  # Imports pyttsx3 library for text-to-speech conversion
import speech_recognition as sr  # Imports speech_recognition library for speech-to-text conversion
import google.generativeai as genai  # Imports Google's generative AI library for AI responses

load_dotenv()  # Loads environment variables from .env file (like API keys)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  # Configures the Google AI API with the API key from environment variables

model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Creates a generative model instance using gemini-1.5-pro-latest
chat = model.start_chat(history=[])  # Initializes a chat session with empty history

engine = pyttsx3.init()  # Initializes the text-to-speech engine
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Sets the voice to the first available voice
engine.setProperty('rate', 150)  # Sets the speech rate to 150 words per minute

def sptext():  # Defines a function to convert speech to text
    recognizer = sr.Recognizer()  # Creates a Recognizer instance for speech recognition
    try:  # Starts a try block to handle potential errors
        with sr.Microphone() as source:  # Opens the microphone as an audio source
            st.write('Listening...')  # Displays "Listening..." in the Streamlit app
            recognizer.adjust_for_ambient_noise(source)  # Adjusts for background noise
            audio = recognizer.listen(source, timeout=5)  # Listens for audio input with a 5-second timeout
            st.write('Recognizing...')  # Displays "Recognizing..." in the Streamlit app
            data = recognizer.recognize_google(audio)  # Uses Google Speech Recognition to convert audio to text
            st.write(f'Recognized: {data}')  # Displays the recognized text
            return data.lower()  # Returns the recognized text in lowercase
    except sr.UnknownValueError:  # Handles case where speech couldn't be understood
        st.write("Couldn't understand the message.")  # Displays error message
        return ""  # Returns empty string
    except sr.RequestError as e:  # Handles API request errors
        st.write(f'Error: {e}')  # Displays the specific error
        return ""  # Returns empty string
    except Exception as e:  # Handles any other unexpected errors
        st.write(f'An Error Occurred: {e}')  # Displays the error message
        return ""  # Returns empty string

def speechtx(text):  # Defines a function to convert text to speech
    try:  # Starts a try block to handle potential errors
        engine.say(text)  # Queues the text to be spoken
        engine.runAndWait()  # Processes the speech queue and waits for completion
        engine.stop()  # Stops the speech engine
    except RuntimeError as e:  # Handles runtime errors during speech
        st.write(f'Error: {e}')  # Displays the error message

def get_gemini_response(question):  # Defines a function to get AI response from Gemini
    response = chat.send_message(question, stream=True)  # Sends the question to Gemini API, gets streaming response
    full_response = ""  # Initializes an empty string to store the complete response
    for chunk in response:  # Iterates through response chunks (streaming)
        full_response += chunk.text  # Concatenates each chunk to build full response
    return full_response  # Returns the complete response

st.set_page_config(page_title='Voice Assistant Jarvis with GEMINI API')  # Sets the Streamlit page title
st.header('Voice Assistant Jarvis')  # Displays a header in the Streamlit app

# if 'chat_history' not in st.session_state:  # Checks if chat_history exists in session state (commented out)
#     st.session_state['chat_history'] = []  # Initializes chat_history as empty list (commented out)

mode = st.radio('Select Interaction Mode:', ('Voice', "Text"))  # Creates a radio button for mode selection

if mode == 'Voice':  # Checks if Voice mode is selected
    if st.button('Ask Jarvis'):  # Creates a button that triggers voice interaction
        speechtx('Hello, I am Jarvis active for your command!')  # Speaks a welcome message
        voice_input = sptext()  # Captures voice input from user
        if voice_input:  # Checks if voice input was successfully captured
            st.write(f'You: {voice_input}')  # Displays user's input
            response = get_gemini_response(voice_input)  # Gets AI response from Gemini
            speechtx(response)  # Speaks the AI response
            st.write(f'Jarvis: {response}')  # Displays the AI response

elif mode == 'Text':  # Checks if Text mode is selected
    input_text = st.text_input('You: ', key='text_input')  # Creates a text input field
    if st.button('Ask'):  # Creates a button to submit text query
        response = get_gemini_response(input_text)  # Gets AI response from Gemini
        st.write(f'Jarvis: {response}')  # Displays the AI response