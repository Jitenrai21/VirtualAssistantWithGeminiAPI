import os
from dotenv import load_dotenv
import streamlit as st
import pyttsx3
import speech_recognition as sr
import datetime
import google.generativeai as genai

load_dotenv()
genai.configure()