
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'sgc.db')

# Inicialización de la base de datos
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Incidencias
    c.execute('''CREATE TABLE IF NOT EXISTS incidencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        estado TEXT DEFAULT 'Abierta',
        fecha TEXT
    )''')
    # Documentos
    c.execute('''CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        nombre TEXT,
        enlace TEXT,
        fecha TEXT
    )''')
    # Pruebas de software
    c.execute('''CREATE TABLE IF NOT EXISTS pruebas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        resultado TEXT,
        fecha TEXT
    )''')
    # Acciones correctivas
    c.execute('''CREATE TABLE IF NOT EXISTS acciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        responsable TEXT,
        estado TEXT,
        fecha TEXT
    )''')
    # Indicadores
    c.execute('''CREATE TABLE IF NOT EXISTS indicadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        valor TEXT,
        fecha TEXT
    )''')
    # Auditorías
    c.execute('''CREATE TABLE IF NOT EXISTS auditorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        resultado TEXT,
        fecha TEXT
    )''')
    # Capacitación
    c.execute('''CREATE TABLE IF NOT EXISTS capacitacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tema TEXT,
        tipo TEXT,
        enlace TEXT,
        fecha TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# Página principal
@app.route('/')
def index():
    return render_template('menu.html')

# Incidencias
@app.route('/incidencias')
def incidencias():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM incidencias')
    datos = c.fetchall()
    conn.close()
    return render_template('incidencias.html', incidencias=datos)

@app.route('/incidencias/nueva', methods=['POST'])
def nueva_incidencia():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO incidencias (titulo, descripcion, fecha) VALUES (?, ?, ?)', (titulo, descripcion, fecha))
    conn.commit()
    conn.close()
    return redirect(url_for('incidencias'))

# Documentos
@app.route('/documentos')
def documentos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM documentos')
    datos = c.fetchall()
    conn.close()
    return render_template('documentos.html', documentos=datos)

# Pruebas de software
@app.route('/pruebas')
def pruebas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM pruebas')
    datos = c.fetchall()
    conn.close()
    return render_template('pruebas.html', pruebas=datos)

# Acciones correctivas
@app.route('/acciones')
def acciones():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM acciones')
    datos = c.fetchall()
    conn.close()
    return render_template('acciones.html', acciones=datos)

# Indicadores
@app.route('/indicadores')
def indicadores():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM indicadores')
    datos = c.fetchall()
    conn.close()
    return render_template('indicadores.html', indicadores=datos)

# Auditorías
@app.route('/auditorias')
def auditorias():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM auditorias')
    datos = c.fetchall()
    conn.close()
    return render_template('auditorias.html', auditorias=datos)

# Capacitación
@app.route('/capacitacion')
def capacitacion():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM capacitacion')
    datos = c.fetchall()
    conn.close()
    return render_template('capacitacion.html', capacitacion=datos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
