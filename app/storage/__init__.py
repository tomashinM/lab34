import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from ..entities import User, Todo

# Подключаемся к БД
db = sqlite3.connect(Path(__file__).parent / '..' / '..' / 'db' / 'database.sqlite', check_same_thread=False)


class Storage:

    @staticmethod
    def add_user(user):
        # Вместо пароля сохраняем хэш пароля
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email, password_hash):
        user_data = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        # Не проверяем явно равенство паролей, а проверяем через его хэш
        if user_data and check_password_hash(user_data[2], password_hash):
            return User(*user_data)
        else:
            return None

    @staticmethod
    def get_user_by_id(user_id):
        user_data = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user_data:
            return User(*user_data)
        else:
            return None

    @staticmethod
    def get_user_todos(user_id):
        todos = db.execute('SELECT id, title, txt, user_id, done FROM todos WHERE user_id = ?', (user_id,)).fetchall()
        if todos:
            return map(lambda todo: Todo(*todo), todos)
        else:
            return None

    @staticmethod
    def get_todo_by_id(todo_id,user_id):
        todo = db.execute('SELECT id, title, txt, user_id, done FROM todos WHERE user_id = ? AND id = ?', (user_id,todo_id)).fetchone()
        if todo:
            return Todo(*todo)
        else:
            return None

    @staticmethod
    def add_todo(todo):
        todo_id = db.execute('INSERT INTO todos (title, txt, user_id) VALUES (?, ?, ?)', (todo.title, todo.txt, todo.user_id)).lastrowid
        db.commit()
        todo = db.execute('SELECT id, title, txt, user_id, done FROM todos WHERE id = ?', (todo_id,)).fetchone()
        return Todo(*todo)

    @staticmethod
    def delete_todo(todo_id):
        db.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        db.commit()
    
    @staticmethod
    def update_todo(todo_id):
        db.execute('UPDATE todos SET done=-1*(done-1) WHERE id = ?', (todo_id,))
        db.commit()