
import time
from typing import NoReturn

import schedule

from config import TIME_SCAN, URL_LIST
from database.database import Base, engine
from libs.request import get_real_status_code, update_status_code_db
from libs.text import get_dt_now


def ping_site_list() -> None:

    print(get_dt_now())

    for url in URL_LIST:

        status_code = get_real_status_code(url)
        update_status_code_db(url, status_code)
    print()


def main() -> NoReturn:

    Base.metadata.create_all(engine)

    print(URL_LIST)

    # schedule.every(5).seconds.do(ping_site_list)
    schedule.every(TIME_SCAN).minutes.do(ping_site_list)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
