
from libs.request import UrlRequest


def main():

    request = UrlRequest(method='get', url='https://ya.ru')
    print(request)
    request.send()

    # print(request.status_code)


if __name__ == "__main__":
    main()
