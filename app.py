import re
from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secret_and_unguessable_key'

# Задание 1

@app.route('/show-args')
def show_args():
    """Отображает параметры URL (query string)."""
    return render_template('show_args.html', args=request.args)

@app.route('/show-headers')
def show_headers():
    """Отображает заголовки запроса."""
    return render_template('show_headers.html', headers=request.headers)

@app.route('/set-cookie')
def set_cookie():
    """Устанавливает тестовый cookie и перенаправляет на страницу их отображения."""
    response = make_response(redirect(url_for('show_cookies')))
    response.set_cookie('test_cookie', 'Flask_App_Cookie_Value')
    response.set_cookie('another_cookie', 'Some_Other_Value_123')
    return response

@app.route('/show-cookies')
def show_cookies():
    """Отображает cookies запроса."""
    return render_template('show_cookies.html', cookies=request.cookies)

@app.route('/show-form', methods=['GET', 'POST'])
def show_form():
    """Отображает простую форму (GET) и данные из нее (POST)."""
    if request.method == 'POST':
        return render_template('show_form.html', form_data=request.form, submitted=True)
    return render_template('show_form.html', submitted=False)


# Задание 2

def validate_and_format_phone(phone_raw):
    """
    Проверяет и форматирует номер телефона.
    Возвращает кортеж: (formatted_number, error_message)
    formatted_number: отформатированный номер или None при ошибке.
    error_message: сообщение об ошибке или None при успехе.
    """
    # 1. Очистка от всех символов, кроме цифр
    digits = re.sub(r'\D', '', phone_raw)

    # 2. Проверка на недопустимые символы (до очистки)
    # Разрешенные символы: цифры, пробелы, (, ), -, ., +
    allowed_chars_pattern = re.compile(r'^[0-9()\-.\s+]+$')
    if not allowed_chars_pattern.match(phone_raw) and phone_raw: # Добавил проверку на непустую строку
         # Проверим еще раз, но только цифры - если тут остались не цифры, то точно ошибка
         if not phone_raw.isdigit() and re.search(r'[^0-9()\-.\s+]', phone_raw):
            return None, "Недопустимый ввод. В номере телефона встречаются недопустимые символы."

    # 3. Проверка длины
    n_digits = len(digits)
    expected_len = -1

    # Убираем пробелы в начале/конце для проверки префикса
    phone_stripped = phone_raw.strip()

    if phone_stripped.startswith('+7') or phone_stripped.startswith('8'):
        expected_len = 11
    elif n_digits == 10 : # Если не начинается с +7 или 8, и имеет 10 цифр - это ок
         expected_len = 10
    # Если цифр 11, но не начинается с +7 или 8 - это тоже ошибка длины
    elif n_digits == 11 and not (phone_stripped.startswith('+7') or phone_stripped.startswith('8')):
        expected_len = -1 # Устанавливаем в неверное значение, чтобы вызвать ошибку ниже
    elif n_digits > 0 : # Если ввели что-то, но длина не 10 или 11 (и не подпадает под +7/8)
        expected_len = 10 # По умолчанию будем сравнивать с 10 для генерации ошибки


    if n_digits != expected_len :
        # Если ожидалось 10 или 11, но не совпало
         if expected_len in (10, 11):
             return None, "Недопустимый ввод. Неверное количество цифр."
         # Если изначально длина была не 10/11 и префикс не +7/8
         elif n_digits > 0: # Если пользователь что-то ввел
              return None, "Недопустимый ввод. Неверное количество цифр."
         # Если ввод пустой, ошибки нет (просто ничего не делаем)
         elif n_digits == 0 and not phone_raw:
             return None, None # Нет ошибки, но и форматировать нечего
         else: # Общий случай неверного количества (если логика выше не покрыла)
              # Эта ветка скорее всего не будет достигнута при текущей логике, но для полноты
               return None, "Недопустимый ввод. Неверное количество цифр."


    # Если дошли сюда, значит символы и длина корректны
    # 4. Форматирование
    # Берем последние 10 цифр для форматирования
    if n_digits == 11:
        target_digits = digits[1:]
    else: # n_digits == 10
        target_digits = digits

    formatted = f"8-{target_digits[0:3]}-{target_digits[3:6]}-{target_digits[6:8]}-{target_digits[8:10]}"
    return formatted, None


@app.route('/phone-checker', methods=['GET', 'POST'])
def phone_checker():
    """Обрабатывает форму проверки номера телефона."""
    phone_number_raw = ""
    error_message = None
    validation_class = ""
    formatted_number = None

    if request.method == 'POST':
        phone_number_raw = request.form.get('phone_number', '')
        formatted_number, error_message = validate_and_format_phone(phone_number_raw)

        if error_message:
            validation_class = 'is-invalid'
        elif formatted_number:
             # Успех, можно добавить класс is-valid, но не требуется по заданию
             # validation_class = 'is-valid'
             pass # Оставляем пустым, если нет ошибки

    return render_template(
        'phone_form.html',
        phone_number_raw=phone_number_raw,
        error_message=error_message,
        validation_class=validation_class,
        formatted_number=formatted_number
    )

@app.route('/')
def index():
    """Главная страница со ссылками."""
    return render_template('base.html', is_index=True) 

if __name__ == '__main__':
    app.run (debug = True)