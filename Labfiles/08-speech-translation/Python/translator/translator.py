# First, in theintegrated terminal, install the Azure AI Speech SDK package by running the command [ pip install azure-cognitiveservices-speech==1.30.0]

from dotenv import load_dotenv
from datetime import datetime
import os

# To use audio input from a file, enter the following command to install a library that you can use to play the audio file: [ pip install playsound==1.3.0]
from playsound import playsound

# Import Namespaces:
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings:
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure Translation:
         translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
         translation_config.speech_recognition_language = 'en-US'
         translation_config.add_target_language('fr')
         translation_config.add_target_language('es')
         translation_config.add_target_language('hi')
         print('Ready to translate from',translation_config.speech_recognition_language)
        
        # Configure Speech:
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)

        # Get User Input:
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                
    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''
    
    # Translate Speech (using the default system microphone for input):
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Speak now...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)

    # Translate Speech (using audio input from a file):
    audioFile = 'station.wav'
    playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)
    
    # Synthesize Translation:
    voices = {
        "fr": "fr-FR-HenriNeural",
        "es": "es-ES-ElviraNeural",
        "hi": "hi-IN-MadhurNeural"
     }
     speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
     speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
     speak = speech_synthesizer.speak_text_async(translation).get()
     if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
         print(speak.reason)

if __name__ == "__main__":
    main()

#  At the end, enter the following command in the integrated terminal to run the program: [python translator.py]
