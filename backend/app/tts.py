import os
import aiohttp
from xml.sax.saxutils import escape
from dotenv import load_dotenv

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

def build_ssml(text: str, gender: str, name: str) -> bytes:
    ssml = f"""
    <speak version='1.0' xml:lang='pt-BR'>
        <voice xml:lang='pt-BR' xml:gender='{gender}' name='{name}'>{escape(text)}</voice>
    </speak>"""
    return ssml.encode("utf-8")

async def azure_text_to_speech_stream(ssml: bytes):
    if not AZURE_ENDPOINT or not AZURE_KEY:
        raise ValueError("AZURE_ENDPOINT ou AZURE_KEY não definidos")

    headers = {
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-48khz-96kbitrate-mono-mp3",
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Accept": "*/*"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(AZURE_ENDPOINT, headers=headers, data=ssml) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Azure TTS request failed: {response.status}, {error_text}")
            async for chunk in response.content.iter_any():
                yield chunk
