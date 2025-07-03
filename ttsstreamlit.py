import streamlit as st
from gtts import gTTS
from googletrans import Translator
import tempfile
import os

def run_text_to_speech():
    st.title("Text-to-Speech with Translation")

    languages = [
        'English', 'Hindi', 'Kannada', 'Tamil', 'Telugu', 'Bengali', 'Gujarati',
        'Marathi', 'Urdu', 'Punjabi', 'Spanish', 'French', 'German',
        'Chinese (Mandarin)', 'Japanese', 'Russian', 'Arabic'
    ]

    language_map = {
        'English': 'en', 'Hindi': 'hi', 'Kannada': 'kn', 'Tamil': 'ta', 'Telugu': 'te', 'Bengali': 'bn',
        'Gujarati': 'gu', 'Marathi': 'mr', 'Urdu': 'ur', 'Punjabi': 'pa', 'Spanish': 'es', 'French': 'fr',
        'German': 'de', 'Chinese (Mandarin)': 'zh-CN', 'Japanese': 'ja', 'Russian': 'ru', 'Arabic': 'ar'
    }

    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""

    text = st.text_area("Enter text here", value=st.session_state.input_text, height=200)
    st.session_state.input_text = text

    selected_language = st.selectbox("Translate & Speak in", languages)

    col1, col2 = st.columns(2)
    play_button = col1.button("Translate & Play")
    clear_button = col2.button("Clear")

    if clear_button:
        st.session_state.input_text = ""
        st.rerun()  # Updated from deprecated st.experimental_rerun()

    if play_button:
        if text.strip() == "":
            st.warning("Please enter text to convert to speech!")
        else:
            with st.spinner("Translating and generating audio..."):
                language_code = language_map.get(selected_language, 'en')

                translator = Translator()
                try:
                    translated = translator.translate(text, dest=language_code)
                    translated_text = translated.text
                except Exception as e:
                    st.error(f"Translation failed: {e}")
                    return

                st.markdown(f"### Translated Text in {selected_language}:")
                st.text_area("Translated Text", value=translated_text, height=150, key="translated_output")

                try:
                    tts = gTTS(text=translated_text, lang=language_code, slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                        tts.save(tmp_file.name)
                        # Read the file and display it
                        with open(tmp_file.name, 'rb') as audio_file:
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/mp3')
                        
                        # Clean up the temporary file
                        try:
                            os.unlink(tmp_file.name)
                        except:
                            pass
                            
                except Exception as e:
                    st.error(f"Text-to-Speech failed: {e}")
                    return

                st.success(f"Translation and speech in {selected_language} complete.")