from typing import Optional, Tuple

from db.user import User
from icons.icon import Quality
import logging as log
import requests

# parse response format
def as_dict(server_answer: str) -> dict[int, str]:
    parameters = server_answer.split(":")
    dictionary: dict[int, str] = {}
    for i in range(0, len(parameters), 2):
        dictionary.update({int(parameters[i]): parameters[i+1]})
    return dictionary


def get_detailed_info(account_id: int):
    headers = {
        "User-Agent": ""
    }
    data = {
        "secret": "Wmfd2893gb7",
        "targetAccountID": account_id
    }
    req = requests.post('http://www.boomlings.com/database/getGJUserInfo20.php', data=data, headers=headers)

    return req.text

def get_account_info(username: str):
    headers = {
        "User-Agent": ""
    }
    data = {
        "secret": "Wmfd2893gb7",
        "str": username
    }
    req = requests.post('http://www.boomlings.com/database/getGJUsers20.php', data=data, headers=headers)
    return req.text


# returns None on servers error, (false, None) if profile not found, (true, User) if everything is OK
def get_gd_user_profile(username: str, quality: Quality=Quality.UHD) -> Optional[Tuple[bool, Optional[User]]]:
    try:
        account_info = get_account_info(username) # 2 - user_id; 16 - account_id
    except:
        log.error(f"Error in account-info request to boomlings.com. (Username: {username})")
        return None

    log.debug(account_info)
    if account_info == "-1":
        return False, None # account not exists
    elif account_info[0] == "<":
        # probably face cloudFlare barrier
        log.warning(f"account-info request returned: {account_info}")
        return None

    account_info = as_dict(account_info)
    account_id = int(account_info[16])

    try:
        detailed_info = get_detailed_info(account_id)
    except:
        log.error(f"Error in detailed-info request to boomlings.com. (Username: {username}. Account_id: {account_id})")
        return None

    log.debug(detailed_info)
    if detailed_info == "-1":
        return False, None # shouldn't happen (as we just got account id from servers) but just in case
    elif detailed_info[0] == "<":
        # probably face cloudFlare barrier
        log.warning(f"detailed-info request returned: {detailed_info}")
        return None

    detailed_info = as_dict(detailed_info)

    cube   = int(detailed_info[21])
    ship   = int(detailed_info[22])
    ball   = int(detailed_info[23])
    ufo    = int(detailed_info[24])
    wave   = int(detailed_info[25])
    robot  = int(detailed_info[26])
    spider = int(detailed_info[43])
    swing  = int(detailed_info[53])
    jet    = int(detailed_info[54])

    glowing = True if detailed_info[28] == '1' else False

    col_1 = int(detailed_info[10])
    col_2 = int(detailed_info[11])
    col_glow = int(detailed_info[51]) if glowing else col_2

    return True, User("", username, account_id, cube=cube, ship=ship, ufo=ufo, ball=ball,
                      wave=wave, robot=robot, spider=spider, swing=swing, jet=jet, col_1=col_1,
                      col_2=col_2, col_glow=col_glow, has_glow=glowing)
