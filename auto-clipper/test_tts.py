"""
TTS Test - Test Azure OpenAI Text-to-Speech
Usage: python test_tts.py
"""

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_key = os.getenv("AZURE_OPENAI_API_KEY")
tts_deployment = os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT")

print("=" * 60)
print("  TTS TEST - Azure OpenAI")
print("=" * 60)
print(f"Endpoint: {azure_endpoint}")
print(f"Deployment: {tts_deployment}")
print(f"Key exists: {bool(azure_key)}")
print("-" * 60)

if not azure_endpoint or not azure_key:
    print("ERROR: Missing Azure OpenAI credentials in .env")
    exit(1)

client = OpenAI(
    api_key=azure_key,
    base_url=f"{azure_endpoint.rstrip('/')}/openai/v1"
)

tts_model = tts_deployment or "tts"
test_text = "Hello! This is a test of the TTS system."

print(f"Model: {tts_model}")
print(f"Text: '{test_text}'")
print("-" * 60)

try:
    output_file = "test_tts_output.mp3"
    
    with client.audio.speech.with_streaming_response.create(
        model=tts_model,
        voice="alloy",
        input=test_text
    ) as response:
        response.stream_to_file(output_file)
    
    print(f"SUCCESS! Audio saved to: {output_file}")
    print(f"File size: {Path(output_file).stat().st_size} bytes")
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

print("=" * 60)
