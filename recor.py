import streamlit as st
import azure.cognitiveservices.speech as speechsdk

def recognize_from_audio_file(language, file_path):
    try:
        # Creates an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription="key", region="westus")
        speech_config.speech_recognition_language = language

        # Creates an audio config with the specified audio file
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        st.info("Processing audio file: {}".format(file_path))

        # Starts speech recognition, and returns after a single utterance is recognized. The speech recognition
        # is performed asynchronously.
        result = speech_recognizer.recognize_once()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            result_text = "Recognized from file {}: {}".format(file_path, result.text)
            st.success(result_text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            result_text = "No speech could be recognized from file {}: {}".format(file_path, result.no_match_details)
            st.warning(result_text)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            result_text = "Speech Recognition from file {} canceled: {}".format(file_path, cancellation_details.reason)
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                result_text += "\nError details: {}".format(cancellation_details.error_details)
            st.error(result_text)

    except Exception as e:
        st.error(f"An error occurred with file {file_path}: {e}")

st.title("Extract Captions from Recorded Video")
st.write("Upload a recorded video or audio file, select the language, and click the button below to extract captions.")

# Dropdown for language selection
language = st.selectbox("Select Language", ["en-US", "hi-IN"], index=0)

# File uploader for selecting the audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "mp4"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("uploaded_audio_file", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Extract Captions"):
        recognize_from_audio_file(language, "uploaded_audio_file")
