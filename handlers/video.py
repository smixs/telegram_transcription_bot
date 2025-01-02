from aiogram import Router, F
from aiogram.types import Message
from services.deepgram import DeepgramService
from utils.formatting import format_transcription
from config.config import config
from loguru import logger
import traceback

router = Router()
deepgram_service = DeepgramService(config.DEEPGRAM_API_KEY)

@router.message(F.video)
async def handle_video(message: Message):
    processing_msg = await message.reply("🎥 Обрабатываю видео...")
    
    try:
        file = await message.bot.get_file(message.video.file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file.file_path}"
        
        logger.debug(f"Processing video file. File URL: {file_url}")
        
        result = await deepgram_service.transcribe_audio(file_url)
        text, reply_markup = format_transcription(result)
        await processing_msg.edit_text(text, reply_markup=reply_markup)
        
    except Exception as e:
        error_msg = f"❌ Ошибка при обработке видео: {str(e)[:200]}..."
        logger.error(f"Full error: {str(e)}\n\nTraceback:\n{''.join(traceback.format_exc())}")
        await processing_msg.edit_text(error_msg)

@router.message(F.video_note)
async def handle_video_note(message: Message):
    processing_msg = await message.reply("🎥 Обрабатываю видео...")
    
    try:
        file = await message.bot.get_file(message.video_note.file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file.file_path}"
        
        logger.debug(f"Processing video note file. File URL: {file_url}")
        
        result = await deepgram_service.transcribe_audio(file_url)
        text, reply_markup = format_transcription(result)
        await processing_msg.edit_text(text, reply_markup=reply_markup)
        
    except Exception as e:
        error_msg = f"❌ Ошибка при обработке видео: {str(e)[:200]}..."
        logger.error(f"Full error: {str(e)}\n\nTraceback:\n{''.join(traceback.format_exc())}")
        await processing_msg.edit_text(error_msg)
