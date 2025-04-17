from gtts import gTTS
import os

def text_to_voice(summary, filename="summary.mp3"):
    tts = gTTS(summary)
    tts.save(filename)
    return filename
