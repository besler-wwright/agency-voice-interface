import json
import logging
import sys
from datetime import datetime

from voice_assistant.config import RUN_TIME_TABLE_LOG_JSON

logger = logging.getLogger(__name__)

# Track the last event type
_last_event_type = None

def log_runtime(function_or_name: str, duration: float):
    time_record = {
        "timestamp": datetime.now().isoformat(),
        "function": function_or_name,
        "duration": f"{duration:.4f}",
    }
    with open(RUN_TIME_TABLE_LOG_JSON, "a") as file:
        json.dump(time_record, file)
        file.write("\n")

    logger.info(f"⏰ {function_or_name}() took {duration:.4f} seconds")


def log_ws_event(direction: str, event: dict):
    global _last_event_type
    event_type = event.get("type", "Unknown")
    event_emojis = {
        "session.update": "🛠️",
        "session.created": "🔌",
        "session.updated": "🔄",
        "input_audio_buffer.append": "🎤",
        "input_audio_buffer.commit": "✅",
        "input_audio_buffer.speech_started": "🗣️",
        "input_audio_buffer.speech_stopped": "🤫",
        "input_audio_buffer.cleared": "🧹",
        "input_audio_buffer.committed": "📨",
        "conversation.item.create": "📥",
        "conversation.item.delete": "🗑️",
        "conversation.item.truncate": "✂️",
        "conversation.item.created": "📤",
        "conversation.item.deleted": "🗑️",
        "conversation.item.truncated": "✂️",
        "response.create": "➡️",
        "response.created": "📝",
        "response.output_item.added": "➕",
        "response.output_item.done": "✅",
        "response.text.delta": "✍️",
        "response.text.done": "📝",
        "response.audio.delta": "🔊",
        "response.audio.done": "🔇",
        "response.done": "✔️",
        "response.cancel": "⛔",
        "response.function_call_arguments.delta": "📥",
        "response.function_call_arguments.done": "📥",
        "rate_limits.updated": "⏳",
        "error": "❌",
        "conversation.item.input_audio_transcription.completed": "📝",
        "conversation.item.input_audio_transcription.failed": "⚠️",
    }
    emoji = event_emojis.get(event_type, "❓")
    icon = "⬆️ - Out" if direction.lower() == "outgoing" else "⬇️ - In"
    message = f"{emoji} {icon} {event_type}"

    # If it's the same event type, update the current line, this gives the appearance of just the time updating
    if event_type == _last_event_type:
        sys.stdout.write('\033[F')  # Move cursor up one line
        sys.stdout.write('\r')
        sys.stdout.flush()
    logger.info(message)
    _last_event_type = event_type
