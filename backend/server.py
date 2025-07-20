# backend/server.py

from flask import Flask, render_template, request, redirect, url_for, flash
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
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_date = request.form['expense_date']
        amount = request.form['amount']
        category = request.form['category']
        notes = request.form['notes']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (expense_date, amount, category, notes)
            VALUES (%s, %s, %s, %s)
        """, (expense_date, amount, category, notes))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('add_expense.html')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        expense_date = request.form['expense_date']
        amount = request.form['amount']
        category = request.form['category']
        notes = request.form['notes']

        cursor.execute("""
            UPDATE expenses
            SET expense_date = %s, amount = %s, category = %s, notes = %s
            WHERE id = %s
        """, (expense_date, amount, category, notes, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    # GET: show form with existing data
    cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
    expense = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('edit_expense.html', expense=expense)
@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
