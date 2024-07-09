import re

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from config import PROJECT_ROOT, SUPPORT_GROUP_ID

router = Router()

@router.message(F.chat.id == int(SUPPORT_GROUP_ID), Command("backup"))
async def make_db_backup(message: Message):
    await message.answer_document(
        FSInputFile(path=f"{PROJECT_ROOT}/db/database.json", filename="database backup.json")
    )


@router.message(F.chat.id == int(SUPPORT_GROUP_ID), F.reply_to_message)
async def respond_to_user(message: Message, bot: Bot):
    if message.reply_to_message.forward_from:
        await bot.send_message(message.reply_to_message.forward_from_chat.id, f"<b>Вы получили ответ от службы поддержки:</b>\n{message.text}")
        await message.reply("Текст сообщения отправлен пользователю")
    elif "chat_id=" in message.reply_to_message.text:
        # in case user forbid accessing profile through forwarded messages
        chat_id = int(re.findall("chat_id=([-0-9]+)", message.reply_to_message.text)[0]) # oh yeah, parsing!!!
        await bot.send_message(chat_id,f"<b>Вы получили ответ от службы поддержки:</b>\n{message.text}")
        await message.reply(f"Текст сообщения отправлен в чат {chat_id}")
    else:
        await message.reply("Сообщение не отправлено. Возможно пользователь запретил доступ к профилю через пересылку сообщений. Попробуйте ответить на предыдущее сообщение (содержащее chat_id=...)")
