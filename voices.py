import os

from dotenv import load_dotenv

load_dotenv()
from pathlib import Path
from openai import OpenAI
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Today is a wonderful day to build something people love!"
)

response.stream_to_file(speech_file_path)