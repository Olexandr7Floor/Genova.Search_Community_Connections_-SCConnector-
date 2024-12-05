from flask import Flask, redirect, url_for
from Controllers.ListController import ListController

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key = 'your_secret_key'  # Для flash-повідомлень

# Реєстрація Blueprint
app.register_blueprint(ListController, url_prefix='/list')

# Головна сторінка
@app.route('/')
def index():
    return redirect(url_for('ListController.list_page'))

if __name__ == '__main__':
    print("Запуск Flask сервера...")
    app.run()