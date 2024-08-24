import pymupdf
from openai import OpenAI, OpenAIError
from pathlib import Path 
import os
import re
from google.cloud import texttospeech

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

def openai_tts(oai_model, oai_voice, oai_input):
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

def gcp_tts(text, output_file, language_code='en-gb', voice_name='en-GB-Standard-A', ssml_gender='FEMALE'):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender[ssml_gender]
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    try:
        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')
        return True
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return False

def main():
    pdf_path = input("Enter the path to your PDF file: ")
    text_inp = scrape_pdf(pdf_path)
    token_count = len(text_inp)
    print("Character count:", token_count)

    while True:
        tts_choice = input("\nChoose the TTS service (1 for OpenAI, 2 for Google Cloud): ")
        if tts_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    if tts_choice == '1':
        print("\nEstimated cost of TTS (tts-1): $", token_count * 0.000015)
        print("Estimated cost of TTS (tts-1-hd): $", token_count * 0.00003)

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
            print("Invalid choice. Please choose from the available options.")

        success = openai_tts(oai_model, oai_voice, text_inp)
        if success:
            print("TTS conversion completed successfully.")
        else:
            print("TTS conversion failed.")

    else:  # Google Cloud TTS
        print("\nGoogle Cloud TTS selected.")
        
        # Language selection
        language_options = {
            '1': ('en-US', 'English (US)'),
            '2': ('en-GB', 'English (UK)'),
            '3': ('fr-FR', 'French'),
            '4': ('de-DE', 'German'),
            '5': ('es-ES', 'Spanish')
        }
        print("\nAvailable languages:")
        for key, (code, name) in language_options.items():
            print(f"{key}: {name}")

        while True:
            lang_choice = input("Choose a language (1-5): ")
            if lang_choice in language_options:
                language_code = language_options[lang_choice][0]
                break
            print("Invalid choice. Please enter a number between 1 and 5.")

        # Voice selection (simplified for this example)
        voice_name = f'{language_code}-Standard-A'

        # Gender selection
        while True:
            gender_choice = input("\nChoose voice gender (M for Male, F for Female): ").upper()
            if gender_choice in ['M', 'F']:
                ssml_gender = 'MALE' if gender_choice == 'M' else 'FEMALE'
                break
            print("Invalid choice. Please enter M or F.")

        # Output file
        output_file = "gcp_tts_output.mp3"

        success = gcp_tts(text_inp, output_file, language_code, voice_name, ssml_gender)
        if success:
            print(f"TTS conversion completed successfully. Output saved to {output_file}")
        else:
            print("TTS conversion failed.")

if __name__ == "__main__":
    main()