from app import app

# Запускаем приложение

app.env = 'development'
app.run(port=3000, host='localhost', debug=True)
