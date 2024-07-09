import re

from aiogram import Router, F, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from io import BytesIO

from db.db_emulator import save_user
from db.user import User
from icons import icon_utils
from icons.boomlings import get_gd_user_profile
from icons.icon import Quality


router = Router()
router.message.middleware(ChatActionMiddleware())


# possible states when stealing icons
class StealingIcons(StatesGroup):
    stealing = State() # getting icons by GD username
    deciding = State() # decides to set icons or not


@router.callback_query(F.data == "steal_icons", StateFilter(None))
async def stealing_icons(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(StealingIcons.stealing)
    await callback.message.answer("Введите имя аккаунта в ГД:")
    await callback.answer()


@router.message(StealingIcons.stealing)
@flags.chat_action("typing")
async def stealing_icons_username_entered(message: Message, state: FSMContext) -> None:
    username = message.text
    if len(username) > 32:
        await message.answer("Имя аккаунта слишком длинное")
    elif not re.match("^[A-Za-z0-9_\- ]+$", username):
        await message.answer("Имя аккаунта содержит недопустимые символы")
    else:
        user = get_gd_user_profile(username.lower())
        if user is None:
            # Error getting data from boomlings.com
            await message.answer("Ошибка: в данный момент функция не работает")
            await state.clear()
        elif not user[1]:
            await message.answer("Аккаунт с таким именем не найден")
            await state.clear()
        else:
            user = user[1]
            user.tg_id = message.from_user.id

            await state.update_data(new_profile=user)

            image = icon_utils.create_icon_grid(user.get_list_of_icons(Quality.UHD))
            bio = BytesIO()
            image.save(bio, "png")
            bio.seek(0)

            builder = ReplyKeyboardBuilder()
            builder.add(
                KeyboardButton(text="Да"),
                KeyboardButton(text="Нет"),
            )

            await message.answer_photo(
                BufferedInputFile(
                    bio.read(),
                    filename="icon_kit"
                ),
                caption=f"Иконки игрока: <b>{username}</b>. Хотите выбрать их?",
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(StealingIcons.deciding)


@router.message(StealingIcons.deciding, F.text.lower().in_({"да", "нет"}))
async def stealing_icons_decision_made(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        new_profile: User = data["new_profile"]
        save_user(new_profile)
        await message.answer("Новые иконки установлены. Используйте /choose, чтобы изменить", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Старые иконки сохранены. Используйте /choose, чтобы изменить", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(StealingIcons.deciding)
async def stealing_icons_wrong_answer(message: Message): # when answer not in {да, нет}
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет"),
    )
    await message.answer("Ответ должен быть \"Да\" или \"Нет\"", reply_markup=builder.as_markup(resize_keyboard=True))


