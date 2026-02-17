import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from rembg import remove, new_session
from PIL import Image


BOT_TOKEN = os.getenv("BOT_TOKEN")

# preload AI model once
session = new_session("u2netp")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a photo to remove background.")


async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = await update.message.reply_text("⏳ Processing...")

        photo = update.message.photo[-1]
        file = await photo.get_file()

        img_bytes = await file.download_as_bytearray()

        print("Image received")

        input_image = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        print("Running AI model...")

        output = remove(input_image, session=session)

        bio = io.BytesIO()
        output.save(bio, format="PNG")
        bio.seek(0)

        print("Sending result...")

        await update.message.reply_document(
            document=bio,
            filename="removed.png"
        )

        await msg.delete()

        print("Done")

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("❌ Failed to process image")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, remove_bg))

    print("✅ Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
