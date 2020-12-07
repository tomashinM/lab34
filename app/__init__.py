from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from .entities import User, Todo
from .storage import Storage

# Создаём приложение
app = Flask(__name__)


app.secret_key = b'super-secret-key'




# Главная страница
@app.route('/', methods=['GET'])
def home():
    # Пользователя получаем из сессии
    if 'user_id' in session:
        user_id = session['user_id']
        # Получили пользователя из БД по ID
        user = Storage.get_user_by_id(user_id)
        todos = Storage.get_user_todos(user.id)
        # Ренедрим страницу по шаблону
        return render_template('pages/index.html', page_title='ToDoService', user=user, todos=todos)
    else:
        # Если пользователь не авторизован - перебрасываем на login
        return redirect('/login')


# Добавление тудушки
@app.route('/', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = Storage.get_user_by_id(session['user_id'])
    Storage.add_todo(Todo(None, request.form['title'],request.form['txt'], user.id, None))
    return redirect(url_for('home'))


# Страница с формой входа
@app.route('/login', methods=['GET'])
def login():
    # Если пользователь уже авторизован, перебросим на главную
    if 'user_id' in session:
        return redirect('/')
    return render_template('pages/login.html', page_title='ToDoService')


# Обработка формы входа
@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход | ToDoService'
    # Введённые данные получаем из тела запроса
    # Но сначала проверяем, что они вообще есть
    if not request.form['email']:
        return render_template('pages/login.html', page_title=page_title, error="Требуется ввести Email")
    if not request.form['password']:
        return render_template('pages/login.html', page_title=page_title, error="Требуется ввести пароль")

    # Ищем пользователя в БД с таким email и паролем
    user = Storage.get_user_by_email_and_password(request.form['email'], request.form['password'])

    # Неверный пароль
    if not user:
        return render_template('pages/login.html', page_title=page_title, error="Неверный пароль")

    # Сохраняем пользователя в сессии
    session['user_id'] = user.id

    # Перенаправляем на главную страницу
    return redirect(url_for('home'))


# Форма регистрации
@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация | ToDoService')


# Обработка формы регистрации
@app.route('/registration', methods=['post'])
def registration_action():
    page_title = 'Регистрация | ToDoService'
    error = None
    # Проверяем данные
    if not request.form['email']:
        error = "Требуется ввести Email"
    if not request.form['password']:
        error = "Требуется ввести пароль"
    if not request.form['password2']:
        error = "Требуется ввести повтор пароля"
    if request.form['password'] != request.form['password2']:
        error = "Пароли не совпадают"
    # В случае ошибки рендерим тот же самый шаблон, но с текстом ошибки
    if error:
        return render_template('pages/registration.html', page_title=page_title, error=error)
    # Добавляем пользователя
    Storage.add_user(User(None, request.form['email'], request.form['password']))
    # Перенаправляем на главную
    return redirect(url_for('home'))


# Выход пользователя
@app.route('/logout')
def logout():
    # Просто выкидываем его из сессии
    session.pop('user_id')
    return redirect(url_for('home'))


# API для удаления тудушки для AJAX
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if 'user_id' not in session:
        return 'Not authorized!', 401
    Storage.delete_todo(todo_id)
    # Не возвращаем ничего, 200 - успешный ответ
    return '', 200


@app.route('/api/todos/<int:todo_id>', methods=['UPDATE'])
def update_todo(todo_id):
    if 'user_id' not in session:
        return 'Not authorized!', 401
    Storage.update_todo(todo_id)
    # Не возвращаем ничего, 200 - успешный ответ
    return '', 200

@app.route('/todo/<int:todo_id>')
def get_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = Storage.get_user_by_id(session['user_id'])    
    todo = Storage.get_todo_by_id(todo_id,user.id)
    return render_template('pages/todo.html', page_title='ToDoService', todo=todo, user=user)
    