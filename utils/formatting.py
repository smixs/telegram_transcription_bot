from models.transcription import TranscriptionResult
from handlers.style import get_style_keyboard

def format_transcription(result: TranscriptionResult) -> tuple[str, dict]:
    """Format transcription result into a readable message with style buttons."""
    # Return clean text without prefix
    return result.text, {"reply_markup": get_style_keyboard()}
