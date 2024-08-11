import pymupdf
from openai import OpenAI, OpenAIError
from pathlib import Path 
import os
import re

os.environ.get("OPENAI_API_KEY")
client = OpenAI()

def clean_tts(text):
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'\b(CONTENTS|Chapter|Section)\b.*?\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^\w\s.,!?-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = '. '.join(sentence.capitalize() for sentence in text.split('. '))
    text = re.sub(r'([a-z])\s([A-Z])', r'\1. \2', text)
    return text

def scrape_pdf(path):
    corpus = ""
    doc = pymupdf.open(path)
    for page in doc:
        corpus += page.get_text()
    corpus = clean_tts(corpus)
    return corpus

def tts(oai_model, oai_voice, oai_input):
    speech_file_path = Path(__file__).parent / "speech.wav"
    try:
        response = client.audio.speech.create(
            model=oai_model,
            voice=oai_voice,
            input=oai_input
        )   
        response.stream_to_file(speech_file_path)
        return True
    except OpenAIError as e:
        print(f"Error: An API error occurred: {str(e)}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
    return False

def main():
    pdf_path = input("Enter the path to your PDF file: ")
    text_inp = scrape_pdf(pdf_path)
    token_count = len(text_inp)
    print("Character count:", token_count)
    print("\nEstimated cost of TTS (tts-1): $", token_count * 0.000015)
    print("\nEstimated cost of TTS (tts-1-hd): $", token_count * 0.00003)

    while True:
        model_choice = input("\nChoose the TTS model (1 for tts-1, 2 for tts-1-hd): ")
        if model_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    oai_model = "tts-1" if model_choice == '1' else "tts-1-hd"
    
    voice_options = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    print("\nAvailable voices:", ", ".join(voice_options))
    print("For more information about the voices, visit:\nhttps://platform.openai.com/docs/guides/text-to-speech/quickstart")

    while True:
        oai_voice = input("\nChoose a voice from the options above: ").lower()
        if oai_voice in voice_options:
            break
        print("Invalid voice. Please choose from the available options.")

    print(f"\nGenerating TTS with model {oai_model} and voice {oai_voice}...")
    tts(oai_model, oai_voice, text_inp)
    print("TTS generation complete. Audio saved as 'speech.wav'.")

if __name__ == "__main__":
    main()