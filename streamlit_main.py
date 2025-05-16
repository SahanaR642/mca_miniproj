import streamlit as st
from ltstreamlit import run_language_translator  
from ttsstreamlit import run_text_to_speech    
from sststreamlit import run_speech_to_text    

def main():
    st.set_page_config(
        page_title="Language Tools Suite",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #0d6efd;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #0b5ed7;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

  
    st.sidebar.title("Language Tools ")
    st.sidebar.image("img1.jpg", width=300)

    task = st.sidebar.selectbox(
        "Choose your task",
        ["Language Translator", "Text-to-Speech", "Speech-to-Text"]
    )

    with st.sidebar.expander("About", expanded=False):
        st.write("""
        This application provides various language tools:
        - **Language Translator**: Translate text between different languages
        - **Text-to-Speech**: Convert text to spoken audio in different languages
        - **Speech-to-Text**: Convert spoken language to text
        """)

    try:
        if task == "Language Translator":
            run_language_translator()
        elif task == "Text-to-Speech":
            run_text_to_speech()
        elif task == "Speech-to-Text":
            run_speech_to_text()
    except Exception as e:
        st.error(f"An error occurred while running the module: {e}")

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
