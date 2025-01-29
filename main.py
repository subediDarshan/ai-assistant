import speech_recognition as sr
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import streamlit as st


load_dotenv()

geminiApi = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=geminiApi)
model = genai.GenerativeModel("gemini-1.5-flash")


def takeCommand():
    """This function takes command & recognize

    Returns:
        text as query
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query



def gemini(text):
    response = model.generate_content(text)
    return response.text

def say(text):
    tts = gTTS(text, lang='en')
    tts.save('audio.mp3')



def main():
    st.title("Multilingual AI Assistant")

    if (st.button("Talk with Assistant")):
        with st.spinner("Listening..."):
            query = takeCommand()
            response = gemini(query)
            say(response)

            audio_file = open("audio.mp3", "rb")
            audio_bytes = audio_file.read()

            st.text_area(label="Response:", value=response, height=350)
            st.audio(audio_bytes, format='audio/mp3')
            st.download_button(label="Download Speech",
                                data=audio_bytes,
                                file_name="speech.mp3",
                                mime="audio/mp3")


main()





