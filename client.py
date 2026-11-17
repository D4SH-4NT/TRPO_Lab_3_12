import requests

URL = "http://127.0.0.1:5000/api/v1/dates/days-between"


def main():
    first = input("Введите первую дату (ДД.ММ.ГГГГ): ")
    second = input("Введите вторую дату (ДД.ММ.ГГГГ): ")

    try:
        response = requests.post(
            URL,
            json={
                "firstDate": first,
                "secondDate": second
            },
            timeout=5
        )
    except requests.RequestException:
        print("Не удалось связаться с сервером. Он запущен?")
        return

    try:
        result = response.json()
    except ValueError:
        print("Сервер вернул ответ не в формате JSON")
        return

    if response.ok:
        print("Полных дней между датами:", result["data"]["days"])
    else:
        print("Ошибка:", result["error"]["message"])

        for item in result["error"]["details"]:
            print(item["field"] + ":", item["message"])


if __name__ == "__main__":
    main()