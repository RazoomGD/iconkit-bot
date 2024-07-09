import json

from config import PROJECT_ROOT
from db.user import User

import logging as log


db_file = f"{PROJECT_ROOT}/db/database.json"


with open(db_file, "r") as f:
    content = f.read()
    if len(content) == 0:
        content = "{}"
    db: dict[str, dict] = json.loads(content)


def get_user_by_tg_id(user_id: int) -> User:
    user_id = str(user_id)
    if user_id not in db:
        user = User(user_id)
        save_user(user)
        return user
    else:
        return User(user_id, dictionary_args=db[user_id])


def save_user(user: User) -> None:
    db.update({str(user.tg_id): dict(user.__dict__)})
    with open(db_file, "w+") as f:
        f.write(json.dumps(db))
    log.info(f"Added new user: {user.tg_id}")



