from deep_translator import GoogleTranslator
from gtts import gTTS


class Translator:
    def __init__(self, audio_dir):
        self.translator = GoogleTranslator(source="auto", target="es")
        self.audio_dir = audio_dir

    def generate_audio(self, text, filename):
        tts = gTTS(text=text, lang="en", tld="us")
        tts.save(filename)
        print(f"Audio generado: {filename}")

    def translate_to_spanish(self, phrase):
        translation = self.translator.translate(phrase)
        return translation
