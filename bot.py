import os
import io
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from rembg import remove
from PIL import Image


BOT_TOKEN = os.getenv("BOT_TOKEN")


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to AI Background Remover Bot!\n\n"
        "Send a photo and I will remove background."
    )


# HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send any photo to remove background."
    )


# REMOVE BACKGROUND
async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = await update.message.reply_text("⏳ Processing...")

        photo = update.message.photo[-1]
        file = await photo.get_file()

        img_bytes = await file.download_as_bytearray()

        input_image = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        output = remove(input_image)

        bio = io.BytesIO()
        output.save(bio, "PNG")
        bio.seek(0)

        await update.message.reply_document(
            document=bio,
            filename="removed.png",
            caption="✅ Done!"
        )

        await msg.delete()

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("❌ Failed to process image")


# MAIN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, remove_bg))

    print("✅ Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
