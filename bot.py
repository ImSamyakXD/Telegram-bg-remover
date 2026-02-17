import os
import io
import asyncio
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


# ==========================
# BOT TOKEN FROM ENV VARIABLE
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")


# ==========================
# START COMMAND
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to AI Background Remover Bot!\n\n"
        "📸 Send me any photo and I will remove the background automatically.\n\n"
        "Commands:\n"
        "/start - Start bot\n"
        "/help - Help info"
    )


# ==========================
# HELP COMMAND
# ==========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 How to use:\n"
        "1️⃣ Send a photo\n"
        "2️⃣ Wait few seconds\n"
        "3️⃣ Download transparent PNG\n\n"
        "Powered by AI 🤖"
    )


# ==========================
# REMOVE BACKGROUND FUNCTION
# ==========================
async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ Processing image...")

        photo = update.message.photo[-1]
        file = await photo.get_file()

        img_bytes = await file.download_as_bytearray()

        input_image = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        output = remove(input_image)

        bio = io.BytesIO()
        output.save(bio, format="PNG")
        bio.seek(0)

        await update.message.reply_document(
            document=bio,
            filename="removed_background.png",
            caption="✅ Background Removed Successfully!"
        )

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("❌ Failed to process image")


# ==========================
# MAIN FUNCTION
# ==========================
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, remove_bg))

    print("✅ Bot Running...")
    await app.run_polling()


# ==========================
# RUN BOT
# ==========================
if __name__ == "__main__":
    asyncio.run(main())
