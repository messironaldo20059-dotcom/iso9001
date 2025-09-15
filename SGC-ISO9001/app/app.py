
# Ruta para checklist ISO 9001 (4.1 a 10.3)
@app.route('/checklist-iso', methods=['GET', 'POST'])
@login_required
def checklist_iso():
    msg = None
    if request.method == 'POST':
        campos = [
            'c4_1','c4_2','c4_3','c4_4','c5_1','c5_2','c5_3','c6_1','c6_2','c6_3',
            'c7_1','c7_2','c7_3','c7_4','c7_5','c8_1','c8_2','c8_3','c8_4','c8_5','c8_6','c8_7',
            'c9_1','c9_2','c9_3','c10_1','c10_2','c10_3'
        ]
        valores = [1 if request.form.get(c) == 'on' else 0 for c in campos]
        usuario = session.get('user', 'admin')
        from datetime import datetime
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"""
            INSERT INTO checklist_iso (
                usuario, {', '.join(campos)}, fecha
            ) VALUES (
                ?, {', '.join(['?']*len(campos))}, ?
            )
        """, [usuario] + valores + [fecha])
        conn.commit()
        conn.close()
        msg = 'Checklist guardado con éxito.'
        return render_template('checklist_iso.html', msg=msg)
    return render_template('checklist_iso.html', msg=msg)




from flask import Flask, render_template, request, redirect, url_for, Response, session
import sqlite3
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave segura en producción




from flask import Flask, render_template, request, redirect, url_for, Response, session
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave segura en producción
# Página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Usuario y contraseña fijos para ejemplo
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render_template('login.html', error=error)

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Decorador para requerir login
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
DB_PATH = os.path.join(os.path.dirname(__file__), 'sgc.db')

# Exportar pruebas a CSV
@app.route('/pruebas/exportar')
def exportar_pruebas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM pruebas')
    datos = c.fetchall()
    conn.close()
    def generate():
        header = ['ID', 'Nombre', 'Resultado', 'Enlace', 'Externo', 'Fecha']
        yield ','.join(header) + '\n'
        for row in datos:
            yield ','.join([str(x) if x is not None else '' for x in row]) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=pruebas.csv"})
# Exportar acciones a CSV
@app.route('/acciones/exportar')
def exportar_acciones():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM acciones')
    datos = c.fetchall()
    conn.close()
    def generate():
        header = ['ID', 'Descripción', 'Responsable', 'Estado', 'Enlace', 'Externo', 'Fecha']
        yield ','.join(header) + '\n'
        for row in datos:
            yield ','.join([str(x) if x is not None else '' for x in row]) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=acciones.csv"})
# Exportar indicadores a CSV
@app.route('/indicadores/exportar')
def exportar_indicadores():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM indicadores')
    datos = c.fetchall()
    conn.close()
    def generate():
        header = ['ID', 'Nombre', 'Valor', 'Enlace', 'Externo', 'Fecha']
        yield ','.join(header) + '\n'
        for row in datos:
            yield ','.join([str(x) if x is not None else '' for x in row]) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=indicadores.csv"})
# Exportar auditorías a CSV
@app.route('/auditorias/exportar')
def exportar_auditorias():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM auditorias')
    datos = c.fetchall()
    conn.close()
    def generate():
        header = ['ID', 'Tipo', 'Resultado', 'Enlace', 'Externo', 'Fecha']
        yield ','.join(header) + '\n'
        for row in datos:
            yield ','.join([str(x) if x is not None else '' for x in row]) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=auditorias.csv"})


# (DB_PATH ya está definido arriba, no es necesario redefinirlo)

# Inicialización de la base de datos
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Checklist ISO 9001 (4.1 a 10.3)
    c.execute('''CREATE TABLE IF NOT EXISTS checklist_iso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        c4_1 INTEGER,
        c4_2 INTEGER,
        c4_3 INTEGER,
        c4_4 INTEGER,
        c5_1 INTEGER,
        c5_2 INTEGER,
        c5_3 INTEGER,
        c6_1 INTEGER,
        c6_2 INTEGER,
        c6_3 INTEGER,
        c7_1 INTEGER,
        c7_2 INTEGER,
        c7_3 INTEGER,
        c7_4 INTEGER,
        c7_5 INTEGER,
        c8_1 INTEGER,
        c8_2 INTEGER,
        c8_3 INTEGER,
        c8_4 INTEGER,
        c8_5 INTEGER,
        c8_6 INTEGER,
        c8_7 INTEGER,
        c9_1 INTEGER,
        c9_2 INTEGER,
        c9_3 INTEGER,
        c10_1 INTEGER,
        c10_2 INTEGER,
        c10_3 INTEGER,
        fecha TEXT
    )''')
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
        externo TEXT,
        fecha TEXT
    )''')
    # Pruebas de software
    c.execute('''CREATE TABLE IF NOT EXISTS pruebas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        resultado TEXT,
        enlace TEXT,
        externo TEXT,
        fecha TEXT
    )''')
    # Acciones correctivas
    c.execute('''CREATE TABLE IF NOT EXISTS acciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        responsable TEXT,
        estado TEXT,
        enlace TEXT,
        externo TEXT,
        fecha TEXT
    )''')
    # Indicadores
    c.execute('''CREATE TABLE IF NOT EXISTS indicadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        valor TEXT,
        enlace TEXT,
        externo TEXT,
        fecha TEXT
    )''')
    # Auditorías
    c.execute('''CREATE TABLE IF NOT EXISTS auditorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        resultado TEXT,
        enlace TEXT,
        externo TEXT,
        fecha TEXT
    )''')
    # Capacitación
    c.execute('''CREATE TABLE IF NOT EXISTS capacitacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tema TEXT,
        tipo TEXT,
        enlace TEXT,
        externo TEXT,
        fecha TEXT
    )''')
    conn.commit()
    conn.close()

init_db()


# Página principal protegida
@app.route('/')
@login_required
def index():
    return render_template('menu.html')


# Incidencias
@app.route('/incidencias')
@login_required
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
@app.route('/documentos', methods=['GET', 'POST'])
@login_required
def documentos():
    if request.method == 'POST':
        tipo = request.form['tipo']
        nombre = request.form['nombre']
        enlace = request.form['enlace']
        externo = request.form.get('externo', '')
        fecha = request.form['fecha']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO documentos (tipo, nombre, enlace, externo, fecha) VALUES (?, ?, ?, ?, ?)', (tipo, nombre, enlace, externo, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('documentos'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM documentos')
    datos = c.fetchall()
    conn.close()
    return render_template('documentos.html', documentos=datos)

# Exportar documentos a CSV
import csv
from flask import Response

@app.route('/documentos/exportar')
def exportar_documentos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM documentos')
    datos = c.fetchall()
    conn.close()
    def generate():
        header = ['ID', 'Tipo', 'Nombre', 'Enlace', 'Externo', 'Fecha']
        yield ','.join(header) + '\n'
        for row in datos:
            yield ','.join([str(x) if x is not None else '' for x in row]) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=documentos.csv"})

# Pruebas de software
@app.route('/pruebas', methods=['GET', 'POST'])
@login_required
def pruebas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        resultado = request.form['resultado']
        fecha = request.form['fecha']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO pruebas (nombre, resultado, fecha) VALUES (?, ?, ?)', (nombre, resultado, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('pruebas'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM pruebas')
    datos = c.fetchall()
    conn.close()
    return render_template('pruebas.html', pruebas=datos)

# Acciones correctivas
@app.route('/acciones', methods=['GET', 'POST'])
@login_required
def acciones():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        responsable = request.form['responsable']
        estado = request.form['estado']
        fecha = request.form['fecha']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO acciones (descripcion, responsable, estado, fecha) VALUES (?, ?, ?, ?)', (descripcion, responsable, estado, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('acciones'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM acciones')
    datos = c.fetchall()
    conn.close()
    return render_template('acciones.html', acciones=datos)

# Indicadores
@app.route('/indicadores', methods=['GET', 'POST'])
@login_required
def indicadores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        valor = request.form['valor']
        fecha = request.form['fecha']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO indicadores (nombre, valor, fecha) VALUES (?, ?, ?)', (nombre, valor, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('indicadores'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM indicadores')
    datos = c.fetchall()
    conn.close()
    return render_template('indicadores.html', indicadores=datos)

# Auditorías
@app.route('/auditorias', methods=['GET', 'POST'])
@login_required
def auditorias():
    if request.method == 'POST':
        tipo = request.form['tipo']
        resultado = request.form['resultado']
        fecha = request.form['fecha']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO auditorias (tipo, resultado, fecha) VALUES (?, ?, ?)', (tipo, resultado, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('auditorias'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM auditorias')
    datos = c.fetchall()
    conn.close()
    return render_template('auditorias.html', auditorias=datos)

# Capacitación
@app.route('/capacitacion', methods=['GET', 'POST'])
@login_required
def capacitacion():
    if request.method == 'POST':
        tema = request.form['tema']
        tipo = request.form['tipo']
        enlace = request.form['enlace']
        fecha = request.form['fecha']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO capacitacion (tema, tipo, enlace, fecha) VALUES (?, ?, ?, ?)', (tema, tipo, enlace, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('capacitacion'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM capacitacion')
    datos = c.fetchall()
    conn.close()
    return render_template('capacitacion.html', capacitacion=datos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
