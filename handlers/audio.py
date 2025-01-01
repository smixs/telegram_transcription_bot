from aiogram import Router, F
from aiogram.types import Message
from services.deepgram import DeepgramService
from utils.formatting import format_transcription
from config.config import config
from loguru import logger
import traceback

router = Router()
deepgram_service = DeepgramService(config.DEEPGRAM_API_KEY)

@router.message(F.audio)
async def handle_audio(message: Message):
    processing_msg = await message.reply("🎵 Обрабатываю аудиофайл...")
    
    try:
        file = await message.bot.get_file(message.audio.file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file.file_path}"
        
        logger.debug(f"Processing audio file. File URL: {file_url}")
        
        result = await deepgram_service.transcribe_audio(file_url)
        formatted_text = format_transcription(result)
        await processing_msg.edit_text(formatted_text)
        
    except Exception as e:
        error_msg = f"❌ Ошибка при обработке:\n\n{str(e)}\n\nTraceback:\n{''.join(traceback.format_exc())}"
        logger.error(error_msg)
        await processing_msg.edit_text(error_msg)
