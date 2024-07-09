import re

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_emulator import get_user_by_tg_id, save_user
from icons.color import min_color, max_color
from icons.icon import IconType

router = Router()
bot_username = ""

class ChoosingIcons(StatesGroup):
    choosing_icon = State()
    choosing_color = State()

@router.callback_query(F.data == "choose_icons")
async def choosing_icons(callback: CallbackQuery):

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="cube", callback_data="cube"),
        InlineKeyboardButton(text="ship", callback_data="ship"),
        InlineKeyboardButton(text="ball", callback_data="ball"),
    )
    builder.row(
        InlineKeyboardButton(text="ufo", callback_data="ufo"),
        InlineKeyboardButton(text="wave", callback_data="wave"),
        InlineKeyboardButton(text="robot", callback_data="robot"),
    )
    builder.row(
        InlineKeyboardButton(text="spider", callback_data="spider"),
        InlineKeyboardButton(text="swing", callback_data="swing"),
        InlineKeyboardButton(text="jetpack", callback_data="jetpack"),
    )
    builder.row(
        InlineKeyboardButton(text="color 1", callback_data="col_1"),
        InlineKeyboardButton(text="color 2", callback_data="col_2"),
    )
    builder.row(
        InlineKeyboardButton(text="color 3", callback_data="col_3"),
        InlineKeyboardButton(text="glow", callback_data="glow"),
    )
    await callback.message.answer("Выберите, что хотите изменить:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.in_({"cube", "ship", "ball", "ufo", "wave", "robot", "spider", "swing", "jetpack"}))
async def change_icon(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global bot_username
    if not bot_username:
        info = await bot.get_me()
        bot_username = info.username

    await state.set_state(ChoosingIcons.choosing_icon)

    icon_type, word_form, search_word = {
        "cube":    (IconType.CUBE,   "куба",          "cube"),
        "ship":    (IconType.SHIP,   "корабля",       "ship"),
        "ball":    (IconType.BALL,   "шара",          "ball"),
        "ufo":     (IconType.UFO,    "НЛО",           "ufo"),
        "wave":    (IconType.WAVE,   "волны",         "wave"),
        "robot":   (IconType.ROBOT,  "робота",        "robot"),
        "spider":  (IconType.SPIDER, "паука",         "spider"),
        "swing":   (IconType.SWING,  "свинг-коптера", "swing"),
        "jetpack": (IconType.JET,    "джет-пака",     "jetpack"),
    }[callback.data]

    await state.update_data(icon_type=icon_type, word_form=word_form, search_word=search_word)

    text = (f"Введите id иконки <b>{word_form}</b> (от {icon_type.value[1]} до {icon_type.value[2]}) "
            f"или воспользуйтесь командой\n<code>@{bot_username} {search_word}</code>\n"
            f"для интерактивного выбора.\n\nКоманда /cancel, чтобы отменить.")

    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data.in_({"col_1", "col_2", "col_3"}))
async def change_icon(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global bot_username
    if not bot_username:
        info = await bot.get_me()
        bot_username = info.username

    await state.set_state(ChoosingIcons.choosing_color)
    await state.update_data(color=callback.data)

    text = (f"Введите id цвета (от {min_color} до {max_color}) или воспользуйтесь командой\n<code>@{bot_username} color</code>\n"
            f"для интерактивного выбора.\n\nКоманда /cancel, чтобы отменить.")

    await callback.message.answer(text)
    await callback.answer()


# @router.message(ChoosingIcons.choosing_icon, Command("cancel"))
# async def cancel_choosing(message: Message, state: FSMContext):
#     await message.answer(f"Выбор иконки отменен")
#     await state.clear()


@router.callback_query(F.data == "glow")
async def switch_glow(callback: CallbackQuery):
    user = get_user_by_tg_id(callback.from_user.id)
    if user.has_glow:
        await callback.message.answer("<b>glow</b> отключен. /iconkit, чтобы посмотреть.")
    else:
        await callback.message.answer("<b>glow</b> включен. /iconkit, чтобы посмотреть.")
    user.has_glow = not user.has_glow
    save_user(user)
    await callback.answer()


@router.message(ChoosingIcons.choosing_icon)
async def make_choice_icon(message: Message, state: FSMContext):
    user_data = await state.get_data()
    min_id = user_data['icon_type'].value[1]
    max_id = user_data['icon_type'].value[2]
    text = (f"Введите id иконки <b>{user_data['word_form']}</b> (от {min_id} до {max_id}).\n"
            f"Или воспользуйтесь командой:\n<code>@{bot_username} {user_data['search_word']}</code>\nдля интерактивного выбора.\n"
            f"Команда /cancel, чтобы отменить.")
    if re.match("^\d+$", message.text):
        icon_id = int(message.text)
        if icon_id > max_id:
            await message.answer(f"<b>Слишком большой id иконки</b>\n{text}")
        elif icon_id < min_id:
            await message.answer(f"<b>Слишком маленький id иконки</b>\n{text}")
        else:
            user = get_user_by_tg_id(message.from_user.id)
            user.set_icon_by_type(user_data['icon_type'], icon_id)
            save_user(user)
            await message.answer(f"Установлена новая иконка <b>{user_data['word_form']}</b>. "
                                 f"Используйте /iconkit или /{user_data['search_word']}, чтобы посмотреть")
            await state.clear()
    else:
        await message.answer(f"<b>Недопустимый ввод</b>\n{text}")


@router.message(ChoosingIcons.choosing_color)
async def make_choice_color(message: Message, state: FSMContext):
    user_data = await state.get_data()
    color = user_data["color"]

    text = (f"Введите id цвета (от {min_color} до {max_color}) или воспользуйтесь командой\n"
            f"<code>@{bot_username} color</code>\nдля интерактивного выбора.\n\nКоманда /cancel, чтобы отменить.")

    if re.match("^\d+$", message.text):
        color_id = int(message.text)
        if color_id > max_color:
            await message.answer(f"<b>Слишком большой id цвета</b>\n{text}")
        elif color_id < min_color:
            await message.answer(f"<b>Слишком маленький id цвета</b>\n{text}")
        else:
            user = get_user_by_tg_id(message.from_user.id)
            if color == "col_1":
                user.col_1 = color_id
            elif color == "col_2":
                user.col_2 = color_id
            elif color == "col_3":
                user.col_glow = color_id

            save_user(user)
            await message.answer("Установлен новый цвет. /iconkit, чтобы посмотреть")
            await state.clear()
    else:
        await message.answer(f"<b>Недопустимый ввод</b>\n{text}")