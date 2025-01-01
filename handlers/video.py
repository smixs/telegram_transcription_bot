from aiogram import Router, F
from aiogram.types import Message
from services.deepgram import DeepgramService
from utils.formatting import format_transcription
from config.config import config
from loguru import logger
import traceback

router = Router()
deepgram_service = DeepgramService(config.DEEPGRAM_API_KEY)

@router.message(F.video_note)
async def handle_video_note(message: Message):
    processing_msg = await message.reply("🎥 Обрабатываю видео-кружок...")
    
    try:
        file = await message.bot.get_file(message.video_note.file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file.file_path}"
        
        logger.debug(f"Processing video note. File URL: {file_url}")
        
        result = await deepgram_service.transcribe_audio(file_url)
        formatted_text = format_transcription(result)
        await processing_msg.edit_text(formatted_text)
        
    except Exception as e:
        error_msg = f"❌ Ошибка при обработке:\n\n{str(e)}\n\nTraceback:\n{''.join(traceback.format_exc())}"
        logger.error(error_msg)
        await processing_msg.edit_text(error_msg)

@router.message(F.video)
async def handle_video(message: Message):
    processing_msg = await message.reply("🎬 Обрабатываю видео...")
    
    try:
        file = await message.bot.get_file(message.video.file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file.file_path}"
        
        logger.debug(f"Processing video. File URL: {file_url}")
        
        result = await deepgram_service.transcribe_audio(file_url)
        formatted_text = format_transcription(result)
        await processing_msg.edit_text(formatted_text)
        
    except Exception as e:
        error_msg = f"❌ Ошибка при обработке:\n\n{str(e)}\n\nTraceback:\n{''.join(traceback.format_exc())}"
        logger.error(error_msg)
        await processing_msg.edit_text(error_msg)
