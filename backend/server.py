# backend/server.py

from flask import Flask, render_template, request, redirect, url_for, flash
# from db_helper import get_connection
from backend.db_helper import get_connection


app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()

    # 🎯 Add this new line
    yearly_data, monthly_data, category_data, top_expenses, avg_monthly = fetch_dashboard_data()

    return render_template(
        'index.html',
        expenses=expenses,
        yearly_data=yearly_data,
        monthly_data=monthly_data,
        category_data=category_data,
        top_expenses=top_expenses,
        avg_monthly=round(avg_monthly, 2)
    )

# 📌 Below get_connection() or at the bottom of server.py
def fetch_dashboard_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Yearly total
    cursor.execute("""
        SELECT YEAR(expense_date) AS year, SUM(amount) AS total
        FROM expenses
        GROUP BY YEAR(expense_date)
        ORDER BY year
    """)
    yearly_data = cursor.fetchall()

    # Month-wise total
    cursor.execute("""
        SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month
    """)
    monthly_data = cursor.fetchall()

    # Category-wise total
    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """)
    category_data = cursor.fetchall()

    # Top 5 highest expenses
    cursor.execute("""
        SELECT expense_date, category, amount, notes
        FROM expenses
        ORDER BY amount DESC
        LIMIT 5
    """)
    top_expenses = cursor.fetchall()

    # Average monthly spend
    cursor.execute("""
        SELECT AVG(monthly_sum) AS avg_spend
        FROM (
            SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount) AS monthly_sum
            FROM expenses
            GROUP BY month
        ) AS monthly_totals
    """)
    avg_monthly = cursor.fetchone()['avg_spend']

    cursor.close()
    conn.close()

    return yearly_data, monthly_data, category_data, top_expenses, avg_monthly


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
    if expense:  # ✅ Fix date for date input
        expense['expense_date'] = expense['expense_date'].strftime('%Y-%m-%d')
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
