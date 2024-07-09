from io import BytesIO

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_emulator import get_user_by_tg_id
from icons import icon_utils
from icons.icon import Quality


router = Router()


@router.message(Command("iconkit"))
async def command_icon_kit(message: Message) -> None:
    user = get_user_by_tg_id(message.from_user.id)
    icon_list = user.get_list_of_icons(Quality.UHD)

    image = icon_utils.create_icon_grid(icon_list)
    bio = BytesIO()
    image.save(bio, "png")
    bio.seek(0)

    await message.answer_photo(
        BufferedInputFile(
            bio.read(),
            filename="icon_kit"
        ),
        caption="<b>Ваш icon kit.</b> Используйте /choose для выбора иконок.",
    )


@router.message(Command("choose"))
async def choose_command(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Вручную", callback_data="choose_icons"),
        InlineKeyboardButton(text="По нику", callback_data="steal_icons"),
    )
    await message.answer(
        text="Можете выбрать иконки вручную или импортировать их из <b>Geometry Dash</b> по нику игрока",
        reply_markup=builder.as_markup()
    )

