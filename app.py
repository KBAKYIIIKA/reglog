from flask import Flask, render_template, request, redirect
import psycopg2
from config import db_connection

app = Flask(__name__)

# Подключение к базе данных
conn = psycopg2.connect(**db_connection)
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    # Вход в аккаунт пользователя при методе POST
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            # Не заполнены все поля
            if username == '' or password == '':
                return render_template('all_fields.html')
            # Нет пользователя
            if not records:
                return render_template('not_exist.html')
            # Страница пользователя
            return render_template('account.html', full_name=records[0][1], log=username, pas=password)
        # Переход на страницу регистрации по кнопке
        elif request.form.get("registration"):
            return redirect("/registration/")
    # Отображение страницы при методе GET
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    # Регистрация при методе POST
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
        records = list(cursor.fetchall())
        # Проверка на существование пользователя
        if records:
            return render_template('user_exists.html')
        # Регистрация
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',
                       (str(name), str(login), str(password)))
        # Не заполнены все поля
        if name == '' or login == '' or password == '':
            return render_template('all_fields.html')
            pass
        conn.commit()
        # Переход на страницу входа при успешной регистрации
        return redirect('/login/')
    # Отображение страницы при методе GET
    return render_template('registration.html')
