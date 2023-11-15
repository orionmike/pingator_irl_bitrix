from datetime import datetime
from urllib.parse import urlparse

import requests

from config import BITRIX_API_ID_CHAT, BITRIX_API_ID_USER, BITRIX_API_URL_MESSAGE, IND, SUCCESS_CODE_LIST, Fore, logger
from database.database import session_maker
from database.models import UrlResponce
from libs.text import get_json_message, get_text_message, get_time_now


class UrlRequest:
    method = None
    url = None
    keyarg_dict = {}

    def __init__(self, method: str = None, url: str = None, **kwargs):
        self.method = method
        self.url = url
        self.keyarg_dict = kwargs

    def __repr__(self) -> str:
        return f'{self.method} -> {self.url}'

    def send(self) -> None:

        if self.method and self.url:

            if self.method == 'post':
                r = requests.post(str(self.url), self.keyarg_dict)
                self.status_code = r.status_code
                print(f'{IND} {get_time_now()} Reuqest[{self.url}] -> {self.status_code}')

            if self.method == 'get':
                r = requests.get(str(self.url), self.keyarg_dict)
                self.status_code = r.status_code
                print(f'{IND} {get_time_now()} Reuqest[{self.url}] -> {self.status_code}')

            else:
                print(f'{IND} {get_time_now()} method not correct')

        else:
            print(f'{get_time_now()} {Fore.RED}Request.send() -> not data')


def get_real_status_code(url: str) -> int:

    status_code = None

    try:

        r = UrlRequest(method='get', url=url, timeout=2)
        r.send()
        status_code = r.status_code

        if status_code not in SUCCESS_CODE_LIST:
            logger.error(f'{url} :: {status_code}')

    except Exception as e:
        print(f'{Fore.RED} get_real_status_code -> error: {e}')

    return status_code


def bitrix_send_message(bitrix_user_id, message) -> None:

    try:

        message_json = get_json_message(bitrix_user_id, message)

        headers = {
            'Content-type': 'application/json',
            'charset': 'utf-8'
        }

        request = UrlRequest(
            method='get', url=BITRIX_API_URL_MESSAGE,
            data=message_json, headers=headers,
            timeout=5
        )
        request.send()

    except Exception as e:
        print(f'{Fore.RED} bitrix_send_message -> e:{e}')
        logger.error(f'bitrix_send_message: -> e:{e}')


def update_status_code_db(url: str, status_code: int) -> None:
    """update status code for case using database"""

    try:

        with session_maker() as session:

            exist_responce = session.query(UrlResponce).filter_by(url=url).first()

            if exist_responce:
                if status_code != exist_responce.status_code:

                    print(f'{IND} {exist_responce.url} -> new status_code: {status_code}')

                    hostname = urlparse(url).hostname
                    message = get_text_message(hostname, status_code)

                    bitrix_send_message(BITRIX_API_ID_USER, message)
                    # or
                    # bitrix_send_message(BITRIX_API_ID_CHAT, message)

                exist_responce.status_code = status_code
                exist_responce.datetime_update = datetime.now()
                session.commit()

            else:
                new_responce = UrlResponce()
                new_responce.url = url
                new_responce.status_code = status_code
                new_responce.datetime_update = datetime.now()
                session.add(new_responce)
                session.commit()

    except Exception as e:
        print(f'{Fore.RED} update_status_code -> e:{e}')
        logger.error(f'update_status_code: -> e:{e}')
