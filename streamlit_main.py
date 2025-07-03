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

    # Elegant Official Style Theme
    st.markdown("""
        <style>
        html, body, .stApp {
            background-color: #fbfbfb;
            color: #212529;
            font-family: "Segoe UI", sans-serif;
        }

        .stSidebar {
            background-color: #062249;
        }

        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5,
        .stSidebar h6, .stSidebar p, .stSidebar div {
            color: #ffffff !important;
        }

        .stButton > button {
            background-color: #062249;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 15px;
        }

        .stButton > button:hover {
            background-color: #0b5ed7;
        }

        .stSelectbox > div > div,
        .stTextInput > div > input,
        .stTextArea > div > textarea {
            background-color: #6fa0c8;
            color: #212529;
            border: 1px solid #ced4da;
            border-radius: 6px;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1a1a1a;
        }

        .css-1v3fvcr, .css-1d391kg {
            background-color: transparent !important;
        }
        .block-recognised {
            background: #e8f4ff;
            border: 1px solid #b6dcff;
            padding: 12px;
            border-radius: 6px;
            font-size: 0.95rem;
            white-space: pre-wrap;
            color: #000;
        }

        .block-translated {
           background: #e7ffe8;
           border: 1px solid #b9ffbb;
           padding: 12px;
           border-radius: 6px;
           font-size: 0.95rem;
           white-space: pre-wrap;
           color: #000;
         }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Language Tools")
    
    # Remove the image reference since it may not exist
    # st.sidebar.image("img1.jpg", width=300)

    task = st.sidebar.selectbox(
        "Choose your task",
        ["Language Translator", "Text-to-Speech", "Speech-to-Text"]
    )

    with st.sidebar.expander("About", expanded=False):
        st.write("""
        This application provides various language tools:
        - **Language Translator**: Translate text between different languages
        - **Text-to-Speech**: Convert text to spoken audio in different languages
        - **Speech-to-Text**: Convert spoken language to text (upload audio files)
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
        st.error("Please check the console for more details.")

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main()