from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .tts import build_ssml, azure_text_to_speech_stream

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice_gender: str
    voice_name: str

@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        ssml = build_ssml(req.text, req.voice_gender, req.voice_name)
        return StreamingResponse(azure_text_to_speech_stream(ssml), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
