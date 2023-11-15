from datetime import datetime


def get_dt_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_time_now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def get_text_message(hostname: str, status_code: int) -> str:
    return f'{get_dt_now()} <b>{hostname}</b> ➜ <b>{status_code}</b>'


def get_json_message(id_chat, message) -> str:
    return f'{{"DIALOG_ID": "{id_chat}", "MESSAGE": "{message}"}}'.encode('utf-8')


def get_json_notification(id_user, message) -> str:
    return f'{{"USER_ID": "{id_user}", "MESSAGE": "{message}"}}'.encode('utf-8')
