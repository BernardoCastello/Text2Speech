import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Carrega váriaveis de ambiente do arquivo .env
load_dotenv()



class AzureTextToSpeechProcessor:
    def __init__(self, text: str, voice: str):
        """
        Inicializa o processador de texto para fala.

        :param text: O texto que será convertido em fala.
        :param voice: O nome da voz a ser usada (ex.: "pt-BR-FranciscaNeural").
        """
        self.text = text
        self.voice = voice
        self.subscription_key = os.getenv("Azure_Key")
        self.region = os.getenv("Azure_Region")
        
        # Configuração do serviço
        self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.region)
        self.speech_config.speech_synthesis_voice_name = self.voice

    def synthesize_speech(self, output_filename: str = "azure_audio.mp3") -> bytes:
        """
        Converte o texto em fala e retorna o áudio gerado como bytes.

        :param output_filename: Nome do arquivo onde o áudio será salvo (opcional).
        :return: Bytes do arquivo de áudio gerado.
        """
        # Configuração para salvar o áudio em um arquivo
        audio_config = speechsdk.audio.AudioConfig(filename=output_filename)

        # Configuração do sintetizador
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)

        # Realiza a conversão
        result = speech_synthesizer.speak_text_async(self.text).get()

        # Verifica se houve sucesso ou erro
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with open(output_filename, "rb") as audio_file:
                audio_bytes = audio_file.read()
            return audio_bytes
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_message = f"Erro: {cancellation_details.reason}"
            if cancellation_details.error_details:
                error_message += f" | Detalhes: {cancellation_details.error_details}"
            raise Exception(error_message)
        


