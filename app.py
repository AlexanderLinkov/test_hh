from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re


# Инициализируем приложение
app = Flask(__name__)

# Подключаемся к базе данных TinyDB
db = TinyDB('forms_db.json')
form_templates = db.table('templates')


# Функция для проверки на email
def is_email(value):
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value))


# Функция для проверки на телефон
def is_phone(value):
    return bool(re.match(r'^(\+7|8)\s?$?\d{3}$?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$', value))


# Функция для проверки на дату
def is_date(value):
    formats = ['%d.%m.%Y', '%Y-%m-%d']
    for fmt in formats:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            pass
    return False


# Функция для определения типа поля
def get_field_type(field_value):
    if is_email(field_value):
        return 'email'
    elif is_phone(field_value):
        return 'phone'
    elif is_date(field_value):
        return 'date'
    else:
        return 'text'


@app.route('/get_form', methods=['POST'])
def get_form():
    form_data = request.form.to_dict()

    # Поиск подходящего шаблона
    matching_template = None
    for template in form_templates.all():
        fields_match = True

        for field_name, field_type in template['fields'].items():
            if field_name not in form_data or get_field_type(form_data[field_name]) != field_type:
                fields_match = False
                break

        if fields_match:
            matching_template = template['name']
            break

    if matching_template:
        return jsonify({'template': matching_template})
    else:
        typed_fields = {k: get_field_type(v) for k, v in form_data.items()}
        return jsonify(typed_fields)


if __name__ == '__main__':
    app.run(debug=True)