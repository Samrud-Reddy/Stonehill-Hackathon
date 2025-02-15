import speech_recognition as sr
from pydub import AudioSegment

def stt(file):
    audio = AudioSegment.from_file(file, format="webm")
    wav_filename = "converted.wav"
    audio.export(wav_filename, format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        a_data = r.record(source)
        text = r.recognize_google(a_data)
        return text

