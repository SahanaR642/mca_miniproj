import streamlit as st
import speech_recognition as sr
import pyttsx3
import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import time
import traceback
from googletrans import Translator
from pydub import AudioSegment

# Language code maps
languages = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Kannada": "kn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN"
}

target_languages = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Arabic": "ar",
    "Bengali": "bn"
}

def SpeakNow(command):
    try:
        voice = pyttsx3.init()
        voice.say(command)
        voice.runAndWait()
    except Exception as e:
        st.error(f"Error speaking text: {str(e)}")

# Convert audio to WAV
def convert_to_wav(file_path):
    wav_path = os.path.splitext(file_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(file_path)
    audio.export(wav_path, format="wav")
    return wav_path

# Recognize and translate
def recognize_and_translate(audio_file, source_lang_code, target_lang_code):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language=source_lang_code)
        st.success(f"Recognized Speech ({source_lang_code}): {text}")

        translator = Translator()
        translated = translator.translate(text, src=source_lang_code.split('-')[0], dest=target_lang_code)
        st.info(f"Translated Text ({translated.dest}): {translated.text}")
        return text, translated.text

    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
        return None, None
    except Exception as e:
        st.error(f"Error during recognition or translation: {str(e)}")
        traceback.print_exc()
        return None, None

# Streamlit UI
def run_speech_to_text():
    st.title("🎤 Speech-to-Text → Translation (Manual Language Selection)")

    # Manual language selections
    source_lang = st.selectbox("Select Source Language:", list(languages.keys()))
    source_lang_code = languages[source_lang]

    target_lang = st.selectbox("Select Target Language:", list(target_languages.keys()))
    target_lang_code = target_languages[target_lang]

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg", "flac", "aac", "m4a", "webm", "wma"])

    st.markdown("### OR Record Audio")
    duration = st.slider("Duration (seconds)", 1, 10, 3)
    record_button = st.button("🎙️ Start Recording")

    audio_path = None

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-4:]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            raw_audio_path = tmp_file.name
        audio_path = convert_to_wav(raw_audio_path)
        st.success("Audio uploaded and converted!")

    elif record_button:
        st.info(f"Recording for {duration} seconds...")
        try:
            sample_rate = 44100
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            st.progress(0)
            for i in range(duration):
                time.sleep(1)
                st.progress((i + 1) / duration)
            sd.wait()
            audio_path = os.path.join(tempfile.gettempdir(), f"recorded_{int(time.time())}.wav")
            wav.write(audio_path, sample_rate, recording)
            st.success("Recording complete.")
        except Exception as e:
            st.error(f"Recording failed: {str(e)}")
            return

    if audio_path:
        st.info("Processing audio...")
        original_text, translated_text = recognize_and_translate(audio_path, source_lang_code, target_lang_code)

        if original_text:
            st.markdown(f"### 📝 Recognized Speech ({source_lang})")
            st.code(original_text)

        if translated_text:
            st.markdown(f"### 🌐 Translated Text ({target_lang})")
            st.code(translated_text)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔊 Speak Original"):
                SpeakNow(original_text)
        with col2:
            if st.button("🗣️ Speak Translation"):
                SpeakNow(translated_text)


if __name__ == "__main__":
    run_speech_to_text()
