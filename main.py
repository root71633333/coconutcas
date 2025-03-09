from flask import Flask, jsonify, render_template, request
import random
import sqlite3

app = Flask(__name__)

# Инициализация БД
def init_db():
    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                 balance REAL DEFAULT 100.0)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/balance', methods=['GET'])
def get_balance():
    user_id = 1  # Для примера используем статический ID
    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = c.fetchone()[0]
    conn.close()
    return jsonify({'balance': balance})

@app.route('/api/bet', methods=['POST'])
def place_bet():
    data = request.json
    user_id = 1
    bet_amount = float(data['amount'])
    choice = data['choice']

    # Получаем текущий баланс
    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = c.fetchone()[0]

    if bet_amount > balance:
        return jsonify({'error': 'Недостаточно средств'}), 400

    # Симулируем игру
    result = random.choice(['heads', 'tails'])
    win = result == choice
    new_balance = balance + (bet_amount if win else -bet_amount)

    # Обновляем баланс
    c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        'result': result,
        'win': win,
        'new_balance': new_balance
    })

@app.route('/api/coinflip', methods=['POST'])
def coinflip():
    data = request.json
    user_id = data.get('user_id', 1)
    bet_amount = float(data['bet'])
    choice = data['choice']

    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = c.fetchone()[0]

    if bet_amount > balance:
        return jsonify({'error': 'Недостаточно средств'}), 400

    result = random.choice(['heads', 'tails'])
    win = result == choice
    new_balance = balance + (bet_amount if win else -bet_amount)

    c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        'result': result,
        'win': win,
        'new_balance': new_balance
    })

if __name__ == '__main__':
    app.run(debug=True)