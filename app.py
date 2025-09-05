from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from pydub import AudioSegment
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio_file = request.files["audio_data"]
    raw_audio_path = f"temp_{uuid.uuid4()}.webm"
    wav_audio_path = f"temp_{uuid.uuid4()}.wav"

    # Save WebM temporarily
    audio_file.save(raw_audio_path)

    # Convert WebM to WAV using pydub
    audio = AudioSegment.from_file(raw_audio_path, format="webm")
    audio.export(wav_audio_path, format="wav")

    # Transcribe WAV
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="hi")

    translator = Translator()
    translated_text = translator.translate(text, dest="en").text

    # Convert translated text to English speech
    speech = gTTS(text=translated_text, lang="en")
    audio_output_path = f"static/{uuid.uuid4()}.mp3"
    speech.save(audio_output_path)

    # Cleanup
    os.remove(raw_audio_path)
    os.remove(wav_audio_path)

    return jsonify({
        "transcribed": text,
        "translated": translated_text,
        "audio_url": "/" + audio_output_path
    })


if __name__ == "__main__":
    app.run(debug=True)
