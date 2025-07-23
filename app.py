from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database/booking.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    shows = conn.execute('SELECT * FROM shows').fetchall()
    conn.close()
    return render_template('index.html', shows=shows)

@app.route('/book/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    conn = get_db_connection()
    show = conn.execute('SELECT * FROM shows WHERE id = ?', (show_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        seats = int(request.form['seats'])

        # Insert booking and get booking ID
        cursor = conn.execute('INSERT INTO bookings (show_id, name, email, seats) VALUES (?, ?, ?, ?)',
                              (show_id, name, email, seats))
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Redirect to confirmation with booking ID
        return redirect(url_for('confirmation', booking_id=booking_id))

    conn.close()
    return render_template('booking.html', show=show)

@app.route('/confirmation')
def confirmation():
    booking_id = request.args.get('booking_id')

    conn = get_db_connection()

    # Fetch full booking info with show details
    booking = conn.execute('''
        SELECT b.name, b.email, b.seats,
               s.name AS show_name, s.date, s.time
        FROM bookings b
        JOIN shows s ON b.show_id = s.id
        WHERE b.id = ?
    ''', (booking_id,)).fetchone()

    conn.close()

    return render_template('confirmation.html', booking=booking)

if __name__ == '__main__':
    app.run(debug=True)
