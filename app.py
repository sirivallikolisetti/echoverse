import streamlit as st
import pyttsx3
import tempfile
import os
import time

from backend import query_ibm_granite  # Optional if you want to use backend rewriting

st.set_page_config(page_title="EchoVerse", layout="centered")

st.title("🎙 EchoVerse: AI-Powered Audiobook Creation")
st.markdown("Transform your text into immersive audio with a tone of your choice.")

st.subheader("Step 1: Input Your Text")
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
    if not text_input.strip():
        st.warning("The uploaded file is empty.")
        text_input = ""
else:
    text_input = st.text_area("Or paste your story, article, or notes here:")

st.subheader("Step 2: Choose a Narration Tone")
tone = st.selectbox(
    "Select a tone to rewrite your text for better emotion and expression",
    ["Neutral", "Suspenseful", "Inspiring", "Funny", "Serious"]
)

st.subheader("📄 Original Text")
st.write(text_input if text_input else "Waiting for your input...")

generate_button = st.button("✨ Generate Rewritten Text & Audio")

def rewrite_text_with_tone(text, tone):
    # Local rewriting option
    if tone == "Neutral":
        return text
    elif tone == "Suspenseful":
        return text + "\n\nThe silence grew louder... a shadow crept closer."
    elif tone == "Inspiring":
        return text + "\n\nAnd just like that, they rose beyond limits."
    elif tone == "Funny":
        return text + "\n\nOops! Even AI needs a laugh sometimes."
    elif tone == "Serious":
        return text + "\n\nThis was no joke. Every word mattered."
    return text

def generate_audio(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)

        voices = engine.getProperty('voices')
        if voices:
            # Let’s use a voice name that works on Windows, e.g. "Zira" or fallback first voice
            selected_voice = None
            for voice in voices:
                if "zira" in voice.name.lower():
                    selected_voice = voice.id
                    break
            if not selected_voice:
                selected_voice = voices[0].id
            engine.setProperty('voice', selected_voice)
        else:
            st.warning("No TTS voices found on your system.")
            return None

        # Use a fixed filename in temp folder for Windows compatibility
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "echoverse_audio.wav")

        if os.path.exists(audio_path):
            os.remove(audio_path)

        engine.save_to_file(text, audio_path)
        engine.runAndWait()

        # Wait to ensure file is written
        time.sleep(1)

        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            raise RuntimeError("Audio file was not created successfully.")

        return audio_path

    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

if generate_button:
    if not text_input.strip():
        st.warning("Please upload or enter some text first.")
    else:
        with st.spinner("🔄 Rewriting your text..."):
            # Use local rewriting or backend API
            # rewritten_text = rewrite_text_with_tone(text_input, tone)

            # Uncomment below to use Hugging Face backend instead:
            # prompt = f"<|system|>Rewrite the following text in a {tone} tone.<|user|>\n{text_input}<|assistant|>\n"
            # rewritten_text = query_ibm_granite(prompt)

            # For now, use local rewriting
            rewritten_text = rewrite_text_with_tone(text_input, tone)

        st.subheader("📝 Rewritten Text")
        st.write(rewritten_text)

        with st.spinner("🎧 Generating audio..."):
            audio_path = generate_audio(rewritten_text)

        if audio_path:
            st.subheader("🔊 Listen to the Narration")
            st.audio(audio_path, format="audio/wav")

            with open(audio_path, "rb") as f:
                st.download_button(
                    label="📥 Download Audio",
                    data=f,
                    file_name="echoverse_audio.wav",
                    mime="audio/wav",
                )
        else:
            st.error("Audio generation failed.")

st.markdown("---")
st.caption("Made with ❤ by EchoVerse Team • Powered by Streamlit and pyttsx3")