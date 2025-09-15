from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'sgc.db')

# Inicialización de la base de datos

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        estado TEXT DEFAULT 'Abierta',
        fecha TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM incidencias')
    incidencias = c.fetchall()
    conn.close()
    return render_template('index.html', incidencias=incidencias)

@app.route('/nueva', methods=['POST'])
def nueva_incidencia():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO incidencias (titulo, descripcion, fecha) VALUES (?, ?, ?)', (titulo, descripcion, fecha))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
