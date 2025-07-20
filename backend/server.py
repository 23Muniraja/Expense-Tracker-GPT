# backend/server.py

from flask import Flask, render_template
from db_helper import get_connection

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
