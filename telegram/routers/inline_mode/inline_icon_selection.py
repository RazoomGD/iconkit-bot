import json
import logging as log

from aiogram import Router, F
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from config import PROJECT_ROOT, TELEGRAM_PREMADE_ICONS_FOLDER_URL
from icons.icon import IconType

router = Router()

with open(f"{PROJECT_ROOT}/telegram/pre_built/icons/icons.json", "r") as f:
    icon_info: dict = json.loads(f.read())


# returns list of GD icon ids and file names: (icon_id, filename)
def get_icon_range(type: IconType, start: int, size: int) -> list[(int, str)]:
    result = []
    for i in range(start, start+size):
        if i >= type.value[2]: break
        result.append((icon_info[type.value[0]][i]["number"], icon_info[type.value[0]][i]["file"]))
    return result

@router.inline_query(F.query.lower().in_({"cube", "ship", "ball", "ufo", "wave", "robot", "spider", "swing", "jetpack"}))
async def choose_jet_inline(inline_query: InlineQuery):
    query_text = inline_query.query.lower()

    icon_type = {"cube": IconType.CUBE, "ship": IconType.SHIP, "ball": IconType.BALL, "ufo": IconType.UFO, "wave": IconType.WAVE, "robot": IconType.ROBOT, "spider": IconType.SPIDER, "swing": IconType.SWING, "jetpack": IconType.JET}[query_text]
    title = {"cube": "Cube", "ship": "Ship", "ball": "Ball", "ufo": "UFO", "wave": "Wave", "robot": "Robot", "spider": "Spider", "swing": "Swing", "jetpack": "Jetpack"}[query_text]

    offset = int(inline_query.offset or 0)
    results = []
    for num, filename in get_icon_range(icon_type, offset, 50):
        results.append(InlineQueryResultArticle(
            id=str(num),
            thumbnail_url=f"{TELEGRAM_PREMADE_ICONS_FOLDER_URL}/{filename}",
            title=f"{title} {num}",
            description=f"id: {num}",
            input_message_content=InputTextMessageContent(
                message_text=f"{num}"
            )
        ))

    if len(results) < 50:
        await inline_query.answer(results, is_personal=False, cache_time=86400) # 1 day
        log.debug(f"sent last portion: {offset} - {offset+len(results)}")
    else:
        await inline_query.answer(results, is_personal=False, next_offset=str(offset+50), cache_time=86400) # 1 day
        log.debug(f"sent: {offset} - {offset + 50}")
