import os
from telegram import ChatAction, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from moviepy.editor import VideoFileClip

# Отримайте токен бота від BotFather
BOT_TOKEN = "6439114775:AAEDsVXRMBiZ6GlIA4VgjIgi2kAuOc5zt_E"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привіт! Відправте мені відео, і я витягну аудіо у голосовому форматі.")

def process_video(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    video_message = update.message.video

    # Надіслати повідомлення про обробку відео
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Зберегти відео-повідомлення на локальний сервер
    video_file = context.bot.get_file(video_message.file_id)
    video_file_path = "input_video.mp4"
    video_file.download(video_file_path)

    # Витягнути аудіо з відео
    audio_file_path = "output_audio.ogg"
    clip = VideoFileClip(video_file_path)
    clip.audio.write_audiofile(audio_file_path)

    # Надіслати аудіо у голосовому повідомленні
    context.bot.send_voice(chat_id, voice=open(audio_file_path, 'rb'))

    # Видалити тимчасові файли
    os.remove(video_file_path)
    os.remove(audio_file_path)

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video & ~Filters.command, process_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()