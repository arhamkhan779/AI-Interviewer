from gtts import gTTS
from io import BytesIO

class TextToSpeech:
    def __init__(self):
        pass
        
    def convert_to_audio(self,text):
        try:
            tts = gTTS(text=text, lang='en')
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            return audio_bytes
        
        except Exception as e:
            raise e