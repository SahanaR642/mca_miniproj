import streamlit as st
import speech_recognition as sr
import os
import tempfile
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

# Convert audio to WAV
def convert_to_wav(file_path):
    try:
        wav_path = os.path.splitext(file_path)[0] + "_converted.wav"
        audio = AudioSegment.from_file(file_path)
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        st.error(f"Error converting audio: {str(e)}")
        return None

# Recognize and translate
def recognize_and_translate(audio_file, source_lang_code, target_lang_code):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text1 = recognizer.recognize_google(audio, language=source_lang_code)
        st.success(f"Recognized Speech ({source_lang_code}):")
        st.markdown(f"<div class='block-recognised'>{text1}</div>", unsafe_allow_html=True)

        translator = Translator()
        translated = translator.translate(text1, src=source_lang_code.split('-')[0], dest=target_lang_code)
        text = translated.text

        st.info(f"Translated Text ({translated.dest}): ")
        st.markdown(f"<div class='block-recognised'>{text}</div>", unsafe_allow_html=True)

        return text1, text 

    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
        return None, None
    except Exception as e:
        st.error(f"Error during recognition or translation: {str(e)}")
        traceback.print_exc()
        return None, None

# Streamlit UI
def run_speech_to_text():
    st.title("🎤 Speech-to-Text → Translation")
    
    # Show warning about cloud limitations
    st.warning("⚠️ Note: Live recording is not available in cloud deployment. Please upload audio files instead.")

    # Manual language selections
    source_lang = st.selectbox("Select Source Language:", list(languages.keys()))
    source_lang_code = languages[source_lang]

    target_lang = st.selectbox("Select Target Language:", list(target_languages.keys()))
    target_lang_code = target_languages[target_lang]

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg", "flac", "aac", "m4a"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            raw_audio_path = tmp_file.name
        
        # Convert to WAV if needed
        if uploaded_file.name.endswith('.wav'):
            audio_path = raw_audio_path
        else:
            audio_path = convert_to_wav(raw_audio_path)
        
        if audio_path:
            st.success("Audio uploaded and processed!")
            st.info("Processing audio...")
            original_text, translated_text = recognize_and_translate(audio_path, source_lang_code, target_lang_code)

            if original_text:
                st.markdown(f"### 📝 Recognized Speech ({source_lang})")
                st.code(original_text)

            if translated_text:
                st.markdown(f"### 🌐 Translated Text ({target_lang})")
                st.code(translated_text)
            
            # Cleanup
            try:
                os.unlink(raw_audio_path)
                if audio_path != raw_audio_path:
                    os.unlink(audio_path)
            except:
                pass

if __name__ == "__main__":
    run_speech_to_text()