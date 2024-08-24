# pdf-to-tts

## Using OpenAI's tts-01 model and pymupdf to convert PDF text into realistic sounding voice

Requires a paid OpenAI account with a valid API key.<br></br>
Comments and information about pdf-to-tts can be found in the ```pdf-to-tts.ipynb``` notebook, whilst the full code can be found in ```main.py```

[tts-01 Documentation](https://platform.openai.com/docs/guides/text-to-speech)

## To use pdf-to-tts

1. Clone the repo.
2. Create a virtual env in the cloned directory by entering ```python3 -m venv pdf-to-tts```.
3. Activate the venv.
   - macOS: ```source .venv/bin/activate```
   - Windows: ```.venv\Scripts\activate```
4. Install dependencies by running ```pip install -r requirements.txt```
5. Set up your API key as an environment variable. More information can be found [here](https://platform.openai.com/docs/quickstart).
   - For macOS: add ```export OPENAI_API_KEY='your-api-key-here'``` to ~/.zshrc (macOS >10.15) or ~/.bash_profile (earlier than 10.15).
   - For Windows: Advanced System Settings -> Environment Variables -> System Variables -> New.. -> enter OPENAI_API_KEY as the variable name and your API key as the variable value.
   - Alternatively, create a OPENAI_API_KEY.env file in the repo directory and add your API key as ```OPENAI_API_KEY=your-api-key-here```.
6. Add your pdf file to the repo directory.
7. Run pdf-to-tts by entering ```python3 -m main``` into a terminal and follow the on-screen instructions.
