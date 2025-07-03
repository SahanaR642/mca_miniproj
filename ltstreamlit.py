import streamlit as st
from googletrans import Translator, LANGUAGES

def run_language_translator():
    st.title("Language Translator")

    if 'input_value' not in st.session_state:
        st.session_state.input_value = ""
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""
    if 'detected_language' not in st.session_state:
        st.session_state.detected_language = ""
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "choose language"

    input_value = st.text_area("Enter text", height=120, value=st.session_state.input_value)
    st.session_state.input_value = input_value
    
    language_options = sorted(list(LANGUAGES.values()))
    dest_lang = st.selectbox("Select Language", 
                            options=["choose language"] + language_options,
                            index=0 if st.session_state.selected_language == "choose language" 
                            else language_options.index(st.session_state.selected_language) + 1
                            if st.session_state.selected_language in language_options else 0)
    
    st.session_state.selected_language = dest_lang

    col1, col2 = st.columns(2)
    with col1:
        translate_button = st.button("Detect and Translate")
    with col2:
        clear_button = st.button("Clear")

    if clear_button:
        st.session_state.input_value = ""
        st.session_state.translated_text = ""
        st.session_state.detected_language = ""
        st.session_state.selected_language = "choose language"
        st.experimental_rerun()

    if translate_button:
        if input_value.strip():
            with st.spinner("Translating..."):
                translator = Translator()
                try:
                     # Detect source language
                    detection = translator.detect(input_value)
                    detected_language = detection.lang
                    detected_language_name = LANGUAGES.get(detected_language, "Unknown")
                    st.session_state.detected_language = detected_language_name
                    
                    # Match destination language code
                    dest_language_code = None
                    for code, lang in LANGUAGES.items():
                        if lang.lower() == dest_lang.lower():
                            dest_language_code = code
                            break
                    # Error if no valid language selected
                    if not dest_language_code or dest_lang == "choose language":
                        st.error("Error: Please select a valid destination language.")
                    else:
                        if detected_language == dest_language_code:
                            st.warning("Note: Source and destination languages are the same.")
                       # Perform translation
                        translated = translator.translate(text=input_value, dest=dest_language_code)
                        st.session_state.translated_text = translated.text
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
        else:
            st.warning("Please enter text to translate.")

    if st.session_state.detected_language:
        st.write(f"Detected Language: **{st.session_state.detected_language}**")

    if st.session_state.translated_text:
        st.write("Translated Text:")
        st.text_area("", st.session_state.translated_text, height=150)