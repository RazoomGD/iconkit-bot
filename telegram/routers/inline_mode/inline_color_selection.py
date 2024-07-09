import json
import logging as log

from aiogram import Router, F
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from config import TELEGRAM_PREMADE_COLORS_FOLDER_URL, PROJECT_ROOT

router = Router()

with open(f"{PROJECT_ROOT}/telegram/pre_built/colors/colors.json", "r") as f:
    color_info: list = json.loads(f.read())
    max_color = len(color_info) - 1


# returns list of offsets, GD color ids and filenames: (offset, col_id, file_name)
def get_color_range(start: int, size: int) -> list[(int, str)]:
    result = []
    for i in range(start, start+size):
        if i > max_color: break
        result.append((i, color_info[i]["id"], color_info[i]["file"]))
    return result


@router.inline_query(F.query == "color")
async def choose_color_inline(inline_query: InlineQuery):
    offset = int(inline_query.offset or 0)
    results = []
    for num, col_id, filename in get_color_range(offset, 50):
        results.append(InlineQueryResultArticle(
            id=str(col_id),
            thumbnail_url=f"{TELEGRAM_PREMADE_COLORS_FOLDER_URL}/{filename}",
            title=f"Color {num+1}",
            description=f"id: {col_id}",
            input_message_content=InputTextMessageContent(
                message_text=f"{col_id}"
            )
        ))

    if len(results) < 50:
        await inline_query.answer(results, is_personal=False, cache_time=86400) # 1 day
        log.debug(f"sent last portion: {offset} - {offset+len(results)}")
    else:
        await inline_query.answer(results, is_personal=False, next_offset=str(offset+50), cache_time=86400) # 1 day
        log.debug(f"sent: {offset} - {offset + 50}")
