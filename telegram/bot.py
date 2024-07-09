from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from telegram.routers import basic_commands, icon_stealing, icon_viewing, icon_choosing, download_icon, admin_commands
from telegram.routers.inline_mode import inline_color_selection, inline_icon_selection



async def main() -> None:
    default_bot_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
    bot = Bot(
        token=BOT_TOKEN,
        default=default_bot_properties
    )
    dp = Dispatcher()

    dp.include_router(basic_commands.router)
    dp.include_router(icon_viewing.router)
    dp.include_router(icon_stealing.router)
    dp.include_router(icon_choosing.router)
    dp.include_router(download_icon.router)
    dp.include_router(admin_commands.router)

    dp.include_router(inline_color_selection.router)
    dp.include_router(inline_icon_selection.router)

    await dp.start_polling(bot)


