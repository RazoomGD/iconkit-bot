from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, LinkPreviewOptions

from config import SUPPORT_GROUP_ID

router = Router()

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Вы запустили бота, работающего с иконками из <b>Geometry Dash</b>. Введите /help, чтобы узнать о возможностях бота")


@router.message(Command("cancel"))
async def cancel_choosing(message: Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state:
        await message.answer("Действие отменено")
        await state.clear()
    else:
        await message.answer("Никаких текущих операций для отмены нет")


@router.message(Command("help"))
async def command_help(message: Message) -> None:
    command_descriptions = (
        "<b>Используйте команды:</b>\n"
        "/start - для запуска бота\n"
        "/help - для получения справки по командам\n\n"
        "<b>Основные команды:</b>\n"
        "/iconkit - для просмотра всех иконок сразу\n"
        "/choose - для выбора иконок\n\n"
        "<b>Дополнительные команды:</b>\n"
        "/cube, /ship, /ball, /ufo, /wave, /robot, /spider, /swing, /jetpack - для просмотра иконок по одной и скачивания изображений иконок без сжатия\n\n"
        "<b>А также:</b>\n"
        "/support - для сообщений о проблемах с ботом и получения поддержки\n"
        "/about - информация о боте"
    )
    await message.answer(command_descriptions)


class GettingSupport(StatesGroup):
    posting_feedback = State()


@router.message(Command("support"))
async def command_support(message: Message, state: FSMContext):
    await state.set_state(GettingSupport.posting_feedback)
    await message.answer("Вы можете отправить сообщение с фитбэком, вопросом или информацией о проблеме: следующее сообщение, которое "
                         "вы отправите в этот чат, будет перенаправлено в службу поддержки. Чтобы отменить, используйте /cancel")


@router.message(GettingSupport.posting_feedback)
async def post_feedback(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(int(SUPPORT_GROUP_ID), f"Новое сообщение в поддержку от пользователя: {message.from_user},\n\nchat_id={message.chat.id}")
    await message.forward(int(SUPPORT_GROUP_ID))
    await message.reply("Данное сообщение направлено в службу поддержки")
    await state.clear()



@router.message(Command("about"))
async def command_about(message: Message):
    await message.answer('- Автор бота: <a href="https://www.youtube.com/channel/UC8V0agF7G-VPg7Tyy_9ceyA">RaZooM GD</a>\n'
                         '- GitHub: <a href="https://github.com/RazoomGD/iconkit-bot">Исходный код бота</a>\n'
                         '- От автора: Я давно хотел научится делать телеграм-ботов. И вот, момент настал. Это мой первый бот - я написал его за неделю, и надеюсь, он получился неплохим. '
                         'В любом случае, это было очень интересно! Буду благодарен за оставленный фитбэк (можете отправлять командой /support), а также за идеи и предложения. Спасибо.',
                         link_preview_options=LinkPreviewOptions(is_disabled=True))
