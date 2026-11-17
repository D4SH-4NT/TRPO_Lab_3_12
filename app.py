import re
from datetime import date

from flask import Flask, jsonify, request

app = Flask(__name__)

# Проверка формата ДД.ММ.ГГГГ
DATE_RE = re.compile(r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}")


def parse_date(value):
    if not isinstance(value, str):
        raise ValueError("значение должно быть строкой вида ДД.ММ.ГГГГ")

    value = value.strip()

    if not DATE_RE.fullmatch(value):
        raise ValueError("ожидается формат ДД.ММ.ГГГГ (цифры и точки)")

    day, month, year = map(int, value.split("."))

    try:
        return date(year, month, day)
    except ValueError:
        raise ValueError("такой даты нет в календаре")


def make_error(message, details):
    return jsonify({
        "error": {
            "code": "VALIDATION_ERROR",
            "message": message,
            "details": details
        }
    }), 400


@app.route("/api/v1/dates/days-between", methods=["POST"])
def days_between():
    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return make_error(
            "Тело запроса должно быть JSON-объектом",
            []
        )

    dates = {}
    errors = []

    for field in ("firstDate", "secondDate"):
        if field not in body:
            errors.append({
                "field": field,
                "message": "поле обязательно"
            })
            continue

        try:
            dates[field] = parse_date(body[field])
        except ValueError as exc:
            errors.append({
                "field": field,
                "message": str(exc)
            })

    if errors:
        return make_error(
            "Переданные данные не прошли проверку",
            errors
        )

    days = abs((dates["secondDate"] - dates["firstDate"]).days)

    print(
        f"Получены даты: {body['firstDate'].strip()} и "
        f"{body['secondDate'].strip()}. "
        f"Количество дней: {days}",
        flush=True
    )

    return jsonify({
        "data": {
            "firstDate": body["firstDate"].strip(),
            "secondDate": body["secondDate"].strip(),
            "days": days
        }
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)