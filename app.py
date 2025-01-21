from text2speach import AzureTextToSpeechProcessor   # Importação para criação de fala
from fastapi import FastAPI, HTTPException           # Importação para servidor 
from fastapi.responses import StreamingResponse
from pydantic import BaseModel                       # Classe base para criar modelos de dados validados e tipados automaticamente
from io import BytesIO                               # Manipular dados binários em memória

# FastAPI app
app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str

@app.post("/synthesize-audio")
def synthesize_audio(request: TTSRequest):
    """
    Endpoint para converter texto em fala usando Azure TTS.

    :param request: JSON contendo o texto e a voz desejada.
    :return: Arquivo de áudio gerado.
    """
    try:
        processor = AzureTextToSpeechProcessor(text=request.text, voice=request.voice)
        audio_data = processor.synthesize_speech()
        audio_stream = BytesIO(audio_data)

        return StreamingResponse(audio_stream, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=output.mp3"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)