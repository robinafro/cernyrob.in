import speech_recognition as sr
from pydub import AudioSegment
from colorama import Fore

import os, json

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

if not os.path.exists(config_path):
    raise Exception("Config file not found.")

config = json.load(open(config_path))


def transcribe_large_audio(audio_file_path, temp_path="", language=config["default_lang"], chunk_duration_ms=60000):
    temp_chunk = os.path.join(temp_path, "temp_chunk.wav")

    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_file_path)

    num_chunks = len(audio) // chunk_duration_ms + 1

    transcriptions = []

    for i in range(num_chunks):
        start_time = i * chunk_duration_ms
        end_time = (i + 1) * chunk_duration_ms

        chunk = audio[start_time:end_time]

        chunk.export(temp_chunk, format="wav")

        with sr.AudioFile(temp_chunk) as chunk_audio_file:
            chunk_audio_data = recognizer.record(chunk_audio_file)

        try:
            print(f"{Fore.BLUE}Transcribing chunk {i + 1} of {num_chunks}...{Fore.RESET}")
            
            text = recognizer.recognize_google(chunk_audio_data, language=language)
            transcriptions.append(text)

        except sr.UnknownValueError:
            print(f"{Fore.YELLOW}Speech Recognition could not understand chunk {i + 1}.{Fore.RESET}")
        except sr.RequestError as e:
            print(f"{Fore.RED}Could not request results from Speech Recognition service; {e}{Fore.RESET}")

    if os.path.exists(temp_chunk):
        os.remove(temp_chunk)

    return "{}".format(" ".join(transcriptions))