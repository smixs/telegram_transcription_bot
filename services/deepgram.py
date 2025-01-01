from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource
)
from models.transcription import TranscriptionResult, Word
import aiohttp

class DeepgramService:
    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)

    async def download_file(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def transcribe_audio(self, file_url: str) -> TranscriptionResult:
        audio_data = await self.download_file(file_url)
        
        # Расширенные опции транскрипции
        options = PrerecordedOptions(
            smart_format=True,  # Умное форматирование чисел, дат, телефонов
            punctuate=True,     # Автоматическая пунктуация
            paragraphs=True,    # Разделение на параграфы
            language="ru",      # Русский язык
            model="nova-2"      # Самая точная модель
        )

        # Создаем payload для транскрипции
        payload = {
            "buffer": audio_data,
            "mimetype": "audio/ogg"
        }
        
        # Отправляем запрос
        response = self.client.listen.rest.v("1").transcribe_file(
            payload,
            options
        )

        # Получаем результаты
        result = response.results.channels[0].alternatives[0]
        
        # Конвертируем слова в наш формат
        words = [
            Word(
                word=w.word,
                start=w.start,
                end=w.end,
                confidence=w.confidence
            )
            for w in result.words
        ]

        return TranscriptionResult(
            text=result.transcript,
            confidence=result.confidence,
            words=words,
            language="ru"
        )
