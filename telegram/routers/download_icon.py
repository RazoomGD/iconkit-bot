from io import BytesIO

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, BufferedInputFile, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_emulator import get_user_by_tg_id
from icons.icon import IconType, Quality
from icons.icon_utils import create_icon_square

router = Router()

@router.message(Command(commands=["cube","ship","ufo","ball","wave","robot","spider","swing","jetpack"]))
async def command_show_icon(message: Message, command: CommandObject):
    command_text = command.text.lower().replace("/", "")
    icon_type = {"cube": IconType.CUBE, "ship": IconType.SHIP, "ufo": IconType.UFO, "ball": IconType.BALL,
                 "wave": IconType.WAVE, "robot": IconType.ROBOT, "spider": IconType.SPIDER, "swing": IconType.SWING,
                 "jetpack": IconType.JET}[command_text]

    user = get_user_by_tg_id(message.from_user.id)
    icon = user.get_icon_by_type(icon_type, Quality.UHD)

    image = create_icon_square(icon)
    bio = BytesIO()
    image.save(bio, "png")
    bio.seek(0)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Скачать png без сжатия", callback_data=f"download_{command_text}"))

    await message.answer_photo(
        BufferedInputFile(
            bio.read(),
            filename=command_text
        ),
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.in_({"download_cube", "download_ship", "download_ufo", "download_robot", "download_ball",
                                   "download_swing", "download_spider", "download_wave", "download_jetpack"}))
async def download_icon(callback: CallbackQuery):
    callback_text = callback.data.replace("download_", "")
    icon_type = {"cube": IconType.CUBE, "ship": IconType.SHIP, "ufo": IconType.UFO, "ball": IconType.BALL,
                 "wave": IconType.WAVE, "robot": IconType.ROBOT, "spider": IconType.SPIDER, "swing": IconType.SWING,
                 "jetpack": IconType.JET}[callback_text]

    user = get_user_by_tg_id(callback.from_user.id)
    icon = user.get_icon_by_type(icon_type, Quality.UHD)

    image = icon.build_icon()
    bio = BytesIO()
    image.save(bio, "png")
    bio.seek(0)

    await callback.message.answer_document(
        BufferedInputFile(
            bio.read(),
            filename=f"{callback_text}_{icon.icon_number}-uhd.png"
        ),
    )
    await callback.answer()