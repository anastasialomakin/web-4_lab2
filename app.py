import re
from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)
application = app

# Задание 1

@app.route('/show-args')
def show_args():
    return render_template('show_args.html', args=request.args)

@app.route('/show-headers')
def show_headers():
    return render_template('show_headers.html', headers=request.headers)

@app.route('/set-cookie')
def set_cookie():
    response = make_response(redirect(url_for('show_cookies')))
    response.set_cookie('test_cookie', 'Flask_App_Cookie_Value')
    response.set_cookie('another_cookie', 'Some_Other_Value_123')
    return response

@app.route('/show-cookies')
def show_cookies():
    return render_template('show_cookies.html', cookies=request.cookies)

@app.route('/show-form', methods=['GET', 'POST'])
def show_form():
    if request.method == 'POST':
        return render_template('show_form.html', form_data=request.form, submitted=True)
    return render_template('show_form.html', submitted=False)

# Задание 2

def validate_and_format_phone(phone_raw):

    digits = re.sub(r'\D', '', phone_raw)
    allowed_chars_pattern = re.compile(r'^[0-9()\-.\s+]+$')
    if not allowed_chars_pattern.match(phone_raw) and phone_raw: 
        if not phone_raw.isdigit() and re.search(r'[^0-9()\-.\s+]', phone_raw):
            return None, "Недопустимый ввод. В номере телефона встречаются недопустимые символы."

    n_digits = len(digits)
    expected_len = -1

    phone_stripped = phone_raw.strip()

    if phone_stripped.startswith('+7') or phone_stripped.startswith('8'):
        expected_len = 11
    elif n_digits == 10 :
        expected_len = 10
    elif n_digits == 11 and not (phone_stripped.startswith('+7') or phone_stripped.startswith('8')):
        expected_len = -1
    elif n_digits > 0 :
        expected_len = 10


    if n_digits != expected_len :
         if expected_len in (10, 11):
            return None, "Недопустимый ввод. Неверное количество цифр."
         elif n_digits > 0:
            return None, "Недопустимый ввод. Неверное количество цифр."
         elif n_digits == 0 and not phone_raw:
            return None, None
         else:
            return None, "Недопустимый ввод. Неверное количество цифр."

    if n_digits == 11:
        target_digits = digits[1:]
    else: 
        target_digits = digits

    formatted = f"8-{target_digits[0:3]}-{target_digits[3:6]}-{target_digits[6:8]}-{target_digits[8:10]}"
    return formatted, None


@app.route('/phone-checker', methods=['GET', 'POST'])
def phone_checker():
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
            pass

    return render_template(
        'phone_form.html',
        phone_number_raw=phone_number_raw,
        error_message=error_message,
        validation_class=validation_class,
        formatted_number=formatted_number
    )

@app.route('/')
def index():
    return render_template('base.html', is_index=True) 

if __name__ == '__main__':
    app.run (debug = True)