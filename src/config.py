import sys
from datetime import datetime
from pathlib import Path

from colorama import Fore, init
from loguru import logger

init(autoreset=True)


ABS_PATH = Path('./src').resolve()  # windows
# ABS_PATH = sys.path[0]  # linux
APP_NAME = 'pingator'


# =====================================
# load config

try:

    if sys.version_info.major == 3 and sys.version_info.minor >= 11:

        import tomllib

        with open(f"{ABS_PATH}/config.toml", "rb") as f:
            config = tomllib.load(f)
    else:

        import toml

        with open(f"{ABS_PATH}/config.toml", "r") as f:
            config = toml.load(f)

    IND = config['utils']['console_indent']

    URL_LIST = config['ping']['url_list']

    SUCCESS_CODE_LIST = config['ping']['success_code_list']
    TIME_SCAN = config['ping']['time_scan']
    DB_FILE = Path(f"{ABS_PATH}/{config['db_sqlite']['db_dir']}/{config['db_sqlite']['db_file']}")

    BITRIX_API_URL_MESSAGE = config['bitrix']['bitrix_api_url_message']
    BITRIX_API_ID_USER = config['bitrix']['bitrix_api_id_user']
    BITRIX_API_ID_CHAT = config['bitrix']['bitrix_api_id_chat']

    # logging

    log_file_name = f'{datetime.now().strftime("%Y-%m-%d")}'
    logger.remove()
    logger.add(f'{ABS_PATH}/logs/{log_file_name}_error.log', format='{time} {level} {message}', level='ERROR', rotation='1 day')

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} start app: {APP_NAME}')
    print(f'{IND} python {sys.version_info.major}.{sys.version_info.minor}')
    print(f'{IND} config loaded: OK')
    print(f'{IND} url list: {URL_LIST}\n')

except Exception as e:
    raise Exception(f'config load -> error: {e}')
