from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tts import build_ssml, azure_text_to_speech_stream

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice_gender: str  # "Male" ou "Female"
    voice_name: str    # Ex: "pt-BR-FranciscaNeural"

@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    try:
        ssml = build_ssml(req.text, req.voice_gender, req.voice_name)
        return StreamingResponse(azure_text_to_speech_stream(ssml), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
