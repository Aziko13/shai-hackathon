import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import app.agent as agent
import asyncio
import re
import json



load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IMAGES_RE = re.compile(r"(?im)^\s*IMAGES:\s*(\[[^\]]*\])\s*$")

graph = agent.build_agent_with_router()

def extract_text_and_images(agent_text: str) -> tuple[str, list[str]]:
    """
    Ищет блок 'IMAGES: ["...","..."]' в конце сообщения.
    Возвращает (text_wo_images, images_list).
    Поддерживает как JSON-массив, так и 'питоновский' список с кавычками.
    """
    images = []
    m = IMAGES_RE.search(agent_text)
    if m:
        raw = m.group(1).strip()
        # сначала пробуем как JSON
        try:
            images = json.loads(raw)
        except json.JSONDecodeError:
            # fallback: грубый парсер строк внутри [ ... ]
            images = re.findall(r"""['"]([^'"]+)['"]""", raw)
        # вырезаем блок IMAGES из текста
        agent_text = agent_text[:m.start()].rstrip()

    # на всякий случай фильтруем пустоты/дубли
    images = [s.strip() for s in images if s and s.strip()]
    return agent_text, images

async def send_images(chat_id: int, images: list[str], context: ContextTypes.DEFAULT_TYPE, reply_to_msg_id: int | None = None):
    for path in images:
        try:
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)
            if re.match(r"^https?://", path, flags=re.I):
                await context.bot.send_photo(chat_id=chat_id, photo=path, reply_to_message_id=reply_to_msg_id)
            else:
                if not os.path.isabs(path):
                    path = os.path.abspath(path)
                with open(path, "rb") as f:
                    await context.bot.send_photo(chat_id=chat_id, photo=f, reply_to_message_id=reply_to_msg_id)
        except Exception as e:
            # короткое уведомление, без утечки путей
            try:
                fname = os.path.basename(path)
            except Exception:
                fname = "image"
            await context.bot.send_message(chat_id=chat_id, text=f"Не удалось отправить изображение: {fname}")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Могу омочь с анализом данных по магазинам.\n"
    )

async def ask_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    def _call_agent():
        msg = {"messages": [{"role": "user", "content": user_text}]}
        config = {"configurable": {"thread_id": str(update.effective_chat.id)}}
        print(config)
        response = graph.invoke(msg, config)
        last_msg = response["messages"][-1]
        return last_msg.content if hasattr(last_msg, "content") else last_msg.get("content", "")

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        agent_response = await asyncio.to_thread(_call_agent)
        text, images = extract_text_and_images(agent_response)
        sent = await update.message.reply_text(text if text.strip() else "Готово.")
        if images:
            await send_images(update.effective_chat.id, images, context, reply_to_msg_id=sent.message_id)

    except Exception as e:
        await update.message.reply_text(f"Sorry, something went wrong: {e}")
        

def run_bot():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not found in .env")

    app_ = Application.builder().token(BOT_TOKEN).build()
    app_.add_handler(CommandHandler("start", start))
    app_.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_agent))
    app_.run_polling()


if __name__ == "__main__":
    run_bot()