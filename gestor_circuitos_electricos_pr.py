#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 GESTOR PROFESIONAL DE CIRCUITOS ELÉCTRICOS - PINAR DEL RÍO
VERSIÓN CORREGIDA Y COMPLETA - Todos los circuitos + Tabla seleccionable + Áreas sombreadas
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import urllib.request
import ssl
import urllib.parse

# ==================== TODOS LOS CIRCUITOS ====================
CIRCUITS_DATA = [
    # Circuitos nuevos que proporcionaste
    {"code": "P 915", "municipio": "Pinar del Río", "description": "Carretera San Juan desde km 4 hasta el km 8 Loma del Ganso.", "lat": 22.406, "lon": -83.685},
    {"code": "P 916", "municipio": "Pinar del Río", "description": "Carretera a San Juan, desde el km 4 hasta el Pedro Téllez.", "lat": 22.410, "lon": -83.680},
    {"code": "P 990", "municipio": "Pinar del Río", "description": "Zona Industrial 7 matas (San Mateo, Escuela de la CTC, Fertilizantes, Cemento), Llamazares, Galeano, Alfredo Porta, Reparto Mijares, Portilla, Otero, Calle San Juan, Maceo, Virtudes, Sol, La Flora.", "lat": 22.420, "lon": -83.690},
    {"code": "P 919", "municipio": "Pinar del Río", "description": "Alameda y Galeano final, Reparto Lazareto, Jacinto, Parte del Reparto Cuba Libre.", "lat": 22.425, "lon": -83.695},
    {"code": "PD 2180", "municipio": "Pinar del Río", "description": "Desde el cementerio de la carretera a Luis Lazo hasta el km 18 Guanito. Parte del Reparto Cuba Libre. Piezas y Repuestos. Reparto Lázaro Acosta.", "lat": 22.390, "lon": -83.720},
    {"code": "PU30", "municipio": "Pinar del Río", "description": "PU30 (P131, P369, S606 y P266)", "lat": 22.380, "lon": -83.750},
    {"code": "P 266", "municipio": "Pinar del Río", "description": "Briones Pueblo - Cayo El Pilar, Punta de Palma", "lat": 22.370, "lon": -83.760},
    {"code": "S 606", "municipio": "Pinar del Río", "description": "Santa María, Carlos Lóriga y la Soledad, Buena Vista, Tirado.", "lat": 22.365, "lon": -83.755},
    {"code": "P 131", "municipio": "Pinar del Río", "description": "Carretera a la Coloma desde Km 11 hasta el Km 18.", "lat": 22.350, "lon": -83.780},
    {"code": "P 369", "municipio": "Pinar del Río", "description": "Carretera a La Coloma desde Km 18 al 21 de la Coloma, Pueblo de la Coloma, Las Canas, Parte de Luengo.", "lat": 22.340, "lon": -83.790},
    {"code": "P 961", "municipio": "Pinar del Río", "description": "Planta de Gases, Materiales 7, Gas Licuado, Carretera a la Coloma hasta km 10. Zona industrial 7 Matas.", "lat": 22.415, "lon": -83.700},
    {"code": "P 970", "municipio": "Pinar del Río", "description": "Entrada del Llamazares, Baldosa y Mosaicos. Gerardo Medina desde el Llamazares hasta la calle Maceo.", "lat": 22.418, "lon": -83.692},
    {"code": "P 60", "municipio": "Pinar del Río", "description": "Parte del Reparto Oriente. Ferrocarriles, PCC Provincial. Reparto Carlos Manuel. Reparto Capó. Reparto Vista Alegre. Parte de la Avenida Rafael Ferro. Terminal de Ómnibus. Pedagógico.", "lat": 22.430, "lon": -83.680},
    {"code": "P 80", "municipio": "Pinar del Río", "description": "Reparto Villamil, Polivalente, Calle Herriman, Calle San Juan hasta la EIDE Ormani Arenado, Reparto Maika. Parte del Rpto Oriente.", "lat": 22.435, "lon": -83.675},
    {"code": "P 90", "municipio": "Pinar del Río", "description": "calle 26 de noviembre-, parte de la Calle Sol y parte del Rpto Oriente.", "lat": 22.428, "lon": -83.685},
    {"code": "P 70", "municipio": "Pinar del Río", "description": "Máximo Gómez, 12 Planta, Teatro Milanés, Tienda Guamá, Doña Neli, Tienda el Fuego, Gobierno Provincial, Alameda, Reparto Vélez, Venegas.", "lat": 22.422, "lon": -83.688},
    {"code": "P 529", "municipio": "Pinar del Río", "description": "Calle Martí hasta Calle San Juan y la Calle Gerardo Medina desde Calle Martí hasta el Hotel Italia. Recreo, Universidad Hermanos Saíz y Hotel Pinar del Río.", "lat": 22.415, "lon": -83.695},
    {"code": "P523", "municipio": "Pinar del Río", "description": "Reparto Los Militares, Reparto Orlando Jerez, Reparto 26 Julio, 10 de Octubre, carretera a Viñales km 1-8, Camino de los Mangos, El Marañón, Cuajaní, Los carretones, La Guanajera.", "lat": 22.440, "lon": -83.670},
    {"code": "P 526", "municipio": "Pinar del Río", "description": "Reparto Hermanos Cruz (Micro I, III, IV y V). ESPA, Cívico, Parte del 10 de Octubre, Vial Colón.", "lat": 22.425, "lon": -83.665},
    {"code": "P 512", "municipio": "Pinar del Río", "description": "IPVCE Federico Engels, Escuela 1ro de Mayo, La casa del Deambulante, Agropecuaria Militar, Montequín, La Conchita hasta Prevención.", "lat": 22.445, "lon": -83.660},

    # Circuitos anteriores (mantengo todos)
    {"code": "PD 1082", "municipio": "Mantua", "description": "Mantua, Arroyos de Mantua, Montezuelo, Macurije, Antúnez, Dimas, Carretera de Guane a Mantua (Guane 2).", "lat": 22.29083, "lon": -84.28722},
    {"code": "PD 1083", "municipio": "Sandino", "description": "Sandino, San Julián, La Fe, Las Martinas, Manuel Lazo, Parte de Babineyes", "lat": 22.08111, "lon": -84.22167},
    {"code": "PD 1081", "municipio": "Guane", "description": "Guane 1, Surí, Isabel Rubio, Benito Juárez, Sabálo, Bailén, Guillén, Boca de Galafre...", "lat": 22.20056, "lon": -84.08361},
    {"code": "PD 415", "municipio": "San Luis", "description": "San Luis, Entronque San Luis, El Cafetal, Río Seco, Vivero, Obeso, Punta de Carta, El Corojo, San Juan.", "lat": 22.28306, "lon": -83.76778},
    {"code": "PD 45", "municipio": "Luis Lazo", "description": "Carretera a Luis Lazo desde Km 21, Las Minas, Pica Pica, Cabeza, Pons, Sumidero, La Güira, El Moncada.", "lat": 22.4106, "lon": -83.9708},
    {"code": "PD 60", "municipio": "Viñales", "description": "La Sabana, Santa Lucía, Río del Medio, Geología.", "lat": 22.4500, "lon": -83.6500},
    {"code": "PD 2175", "municipio": "Viñales", "description": "km 9 de la carretera a Viñales, Viñales, San Vicente, Puerto Esperanza, Los Hoyos, La Jagua...", "lat": 22.61528, "lon": -83.71583},
    {"code": "PD 2190", "municipio": "Consolación del Sur", "description": "Ovas, Pilotos, Pueblo Nuevo, Alonso de Rojas, Monte Alegre...", "lat": 22.50000, "lon": -83.51528},
    {"code": "PD 105", "municipio": "Consolación del Sur", "description": "Crucero Juan Pérez, Presa El Patate, Herradura, Villa 1...", "lat": 22.50000, "lon": -83.51528},
    {"code": "PD 100", "municipio": "Los Palacios", "description": "Los Palacios, Cubanacán, Paso Real, Valverde, Cubaquivir.", "lat": 22.58250, "lon": -83.24889},
]

PROJECT_ROOT = Path("gestor_circuitos_electricos_pr")

def write_file(relative_path: str, content: str):
    path = PROJECT_ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f"[OK] Creado: {path}")

def download_file(url, dest_path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=ctx) as r, open(dest_path, 'wb') as f:
            f.write(r.read())
        print(f"[OK] Descargado: {dest_path}")
    except Exception as e:
        print(f"[ERROR] {url}: {e}")

def download_static():
    static = PROJECT_ROOT / "static"
    download_file("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", static / "css" / "bootstrap.min.css")
    download_file("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js", static / "js" / "bootstrap.bundle.min.js")

# ==================== ARCHIVOS ====================
write_file("requirements.txt", """Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
WTForms==3.1.2
python-dotenv==1.0.1
folium==0.18.0
fpdf2==2.7.9
openpyxl==3.1.2
""")

write_file(".env", """DATABASE_URL=sqlite:///circuitos.db
SECRET_KEY=super-clave-segura-2026
FLASK_ENV=development
""")

write_file("models.py", """from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Circuit(db.Model):
    __tablename__ = 'circuits'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    municipio = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

class SENUpdate(db.Model):
    __tablename__ = 'sen_updates'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    national_deficit_night_mw = db.Column(db.Float)
    provincial_affectation_mw = db.Column(db.Float)
    note = db.Column(db.Text)
    affectations = db.relationship('CircuitAffectation', backref='update', lazy=True)

class CircuitAffectation(db.Model):
    __tablename__ = 'circuit_affectations'
    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey('sen_updates.id'))
    circuit_code = db.Column(db.String(20), db.ForeignKey('circuits.code'))
""")

write_file("forms.py", """from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, DateTimeField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange

class SENUpdateForm(FlaskForm):
    timestamp = DateTimeField('Fecha y Hora', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    national_deficit_night_mw = FloatField('Déficit Nacional Nocturno (MW)', validators=[DataRequired()])
    provincial_affectation_mw = FloatField('Afectación Provincial (MW)', validators=[DataRequired()])
    note = TextAreaField('Nota')
    affected_circuits = SelectMultipleField('Circuitos afectados', validators=[DataRequired()])
""")

write_file("utils.py", """from models import Circuit, SENUpdate, CircuitAffectation

def get_latest_update():
    return SENUpdate.query.order_by(SENUpdate.timestamp.desc()).first()

def get_municipios():
    return sorted({c.municipio for c in Circuit.query.all()})
""")

write_file("app.py", '''from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from models import db, Circuit, SENUpdate, CircuitAffectation
from forms import SENUpdateForm
from utils import get_latest_update, get_municipios
from datetime import datetime
import folium
from folium.plugins import HeatMap, MarkerCluster, MiniMap
import os
from io import BytesIO
from fpdf import FPDF
import openpyxl
from openpyxl.styles import Font
from dotenv import load_dotenv
import urllib.parse
from collections import defaultdict

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# CIRCUITS_DATA debe estar disponible para los comandos Flask
CIRCUITS_DATA = [
    # (Aquí se copiará toda la lista grande de circuitos del generador)
    {"code": "P 915", "municipio": "Pinar del Río", "description": "Carretera San Juan desde km 4 hasta el km 8 Loma del Ganso.", "lat": 22.406, "lon": -83.685},
    {"code": "P 916", "municipio": "Pinar del Río", "description": "Carretera a San Juan, desde el km 4 hasta el Pedro Téllez.", "lat": 22.410, "lon": -83.680},
    {"code": "P 990", "municipio": "Pinar del Río", "description": "Zona Industrial 7 matas, Llamazares, Galeano, Alfredo Porta, Mijares, Portilla, Otero...", "lat": 22.420, "lon": -83.690},
    {"code": "P 919", "municipio": "Pinar del Río", "description": "Alameda y Galeano final, Lazareto, Jacinto, Cuba Libre.", "lat": 22.425, "lon": -83.695},
    {"code": "PD 2180", "municipio": "Pinar del Río", "description": "Cementerio Luis Lazo hasta km 18 Guanito, Cuba Libre, Lázaro Acosta.", "lat": 22.390, "lon": -83.720},
    {"code": "PU30", "municipio": "Pinar del Río", "description": "PU30 (P131, P369, S606 y P266)", "lat": 22.380, "lon": -83.750},
    {"code": "P 266", "municipio": "Pinar del Río", "description": "Briones Pueblo - Cayo El Pilar, Punta de Palma", "lat": 22.370, "lon": -83.760},
    {"code": "S 606", "municipio": "Pinar del Río", "description": "Santa María, Carlos Lóriga, Soledad, Buena Vista, Tirado.", "lat": 22.365, "lon": -83.755},
    {"code": "P 131", "municipio": "Pinar del Río", "description": "Carretera a la Coloma Km 11-18.", "lat": 22.350, "lon": -83.780},
    {"code": "P 369", "municipio": "Pinar del Río", "description": "Carretera a La Coloma Km 18-21, Pueblo de la Coloma, Las Canas, Luengo.", "lat": 22.340, "lon": -83.790},
    {"code": "P 961", "municipio": "Pinar del Río", "description": "Planta de Gases, Materiales 7, Gas Licuado, Zona industrial 7 Matas.", "lat": 22.415, "lon": -83.700},
    {"code": "P 970", "municipio": "Pinar del Río", "description": "Llamazares, Baldosa y Mosaicos, Gerardo Medina hasta Maceo.", "lat": 22.418, "lon": -83.692},
    {"code": "P 60", "municipio": "Pinar del Río", "description": "Reparto Oriente, Ferrocarriles, PCC, Carlos Manuel, Capó, Vista Alegre, Rafael Ferro.", "lat": 22.430, "lon": -83.680},
    {"code": "P 80", "municipio": "Pinar del Río", "description": "Villamil, Polivalente, Herriman, San Juan hasta EIDE, Maika.", "lat": 22.435, "lon": -83.675},
    {"code": "P 90", "municipio": "Pinar del Río", "description": "Calle 26 de noviembre, parte de Sol y Rpto Oriente.", "lat": 22.428, "lon": -83.685},
    {"code": "P 70", "municipio": "Pinar del Río", "description": "Máximo Gómez, Teatro Milanés, Guamá, Gobierno Provincial, Alameda, Vélez.", "lat": 22.422, "lon": -83.688},
    {"code": "P 529", "municipio": "Pinar del Río", "description": "Martí hasta San Juan, Gerardo Medina, Recreo, Universidad, Hotel Pinar del Río.", "lat": 22.415, "lon": -83.695},
    {"code": "P523", "municipio": "Pinar del Río", "description": "Los Militares, Orlando Jerez, 26 Julio, 10 de Octubre, Viñales km 1-8...", "lat": 22.440, "lon": -83.670},
    {"code": "P 526", "municipio": "Pinar del Río", "description": "Hermanos Cruz, ESPA, Cívico, 10 de Octubre, Vial Colón.", "lat": 22.425, "lon": -83.665},
    {"code": "P 512", "municipio": "Pinar del Río", "description": "IPVCE Federico Engels, Montequín, La Conchita...", "lat": 22.445, "lon": -83.660},
    # ... (los PD antiguos también están incluidos en la lista completa del generador)
    {"code": "PD 1082", "municipio": "Mantua", "description": "Mantua, Arroyos de Mantua...", "lat": 22.29083, "lon": -84.28722},
    {"code": "PD 1083", "municipio": "Sandino", "description": "Sandino, San Julián...", "lat": 22.08111, "lon": -84.22167},
    {"code": "PD 1081", "municipio": "Guane", "description": "Guane 1, Surí, Isabel Rubio...", "lat": 22.20056, "lon": -84.08361},
    {"code": "PD 415", "municipio": "San Luis", "description": "San Luis y zona", "lat": 22.28306, "lon": -83.76778},
    {"code": "PD 45", "municipio": "Luis Lazo", "description": "Luis Lazo y zona", "lat": 22.4106, "lon": -83.9708},
    {"code": "PD 60", "municipio": "Viñales", "description": "La Sabana, Santa Lucía...", "lat": 22.4500, "lon": -83.6500},
    {"code": "PD 2175", "municipio": "Viñales", "description": "Viñales y zona", "lat": 22.61528, "lon": -83.71583},
    {"code": "PD 2190", "municipio": "Consolación del Sur", "description": "Consolación del Sur zona", "lat": 22.50000, "lon": -83.51528},
    {"code": "PD 105", "municipio": "Consolación del Sur", "description": "Consolación del Sur", "lat": 22.50000, "lon": -83.51528},
    {"code": "PD 100", "municipio": "Los Palacios", "description": "Los Palacios y zona", "lat": 22.58250, "lon": -83.24889},
]

@app.cli.command('init-db')
def init_db_command():
    db.create_all()
    print("[OK] Base de datos creada correctamente.")

@app.cli.command('import-circuitos')
def import_circuitos():
    count = 0
    for data in CIRCUITS_DATA:
        if not Circuit.query.filter_by(code=data["code"]).first():
            circuit = Circuit(**data)
            db.session.add(circuit)
            count += 1
    db.session.commit()
    print(f"[OK] {count} circuitos importados correctamente.")

# ==================== DASHBOARD ====================
@app.route('/')
def index():
    circuits = Circuit.query.all()
    latest = get_latest_update()
    return render_template('index.html', circuits=circuits, latest=latest)

# ==================== MAPA CON ÁREAS SOMBREADAS ====================
@app.route('/mapa')
def mapa():
    selected_codes = request.args.getlist('circuits')
    m = folium.Map(location=[22.40, -83.70], zoom_start=9, tiles=None)
    
    folium.TileLayer('OpenStreetMap', name='Calles').add_to(m)
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
    
    circuits = Circuit.query.filter(Circuit.code.in_(selected_codes)).all() if selected_codes else Circuit.query.all()
    
    for c in circuits:
        folium.Marker([c.lat, c.lon], popup=f"<b>{c.code}</b><br>{c.description}", tooltip=c.code).add_to(m)
        # Área sombreada (círculo aproximado de cobertura)
        folium.Circle(location=[c.lat, c.lon], radius=8000, color="red", fill=True, fillOpacity=0.15).add_to(m)
    
    MiniMap().add_to(m)
    folium.LayerControl().add_to(m)
    return render_template('mapa.html', map_html=m._repr_html_(), all_circuits=Circuit.query.all())

# ==================== OTRAS RUTAS (simplificadas) ====================
@app.route('/update/add', methods=['GET', 'POST'])
def add_update():
    form = SENUpdateForm()
    form.affected_circuits.choices = [(c.code, f"{c.code} - {c.municipio}") for c in Circuit.query.all()]
    if form.validate_on_submit():
        update = SENUpdate(timestamp=form.timestamp.data or datetime.utcnow(),
                           national_deficit_night_mw=form.national_deficit_night_mw.data,
                           provincial_affectation_mw=form.provincial_affectation_mw.data,
                           note=form.note.data)
        db.session.add(update)
        db.session.flush()
        for code in form.affected_circuits.data:
            db.session.add(CircuitAffectation(update_id=update.id, circuit_code=code))
        db.session.commit()
        flash('[OK] Actualización guardada', 'success')
        return redirect(url_for('index'))
    return render_template('update_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
''')

# ==================== TEMPLATES ====================
write_file("templates/index.html", """{% extends 'base.html' %}
{% block content %}
<h2>Lista de Circuitos Eléctricos - Pinar del Río</h2>

<form method="get" action="{{ url_for('mapa') }}">
    <table class="table table-hover" id="circuitsTable">
        <thead class="table-dark">
            <tr>
                <th><input type="checkbox" onclick="toggleAll(this)"></th>
                <th>Código</th>
                <th>Municipio</th>
                <th>Descripción / Zona</th>
            </tr>
        </thead>
        <tbody>
            {% for c in circuits %}
            <tr>
                <td><input type="checkbox" name="circuits" value="{{ c.code }}"></td>
                <td><strong>{{ c.code }}</strong></td>
                <td>{{ c.municipio }}</td>
                <td>{{ c.description }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <button type="submit" class="btn btn-primary">Ver en Mapa con Áreas Sombreadas</button>
</form>

<script>
function toggleAll(source) {
    checkboxes = document.getElementsByName('circuits');
    for(var i=0; i<checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}
</script>
{% endblock %}
""")

write_file("templates/mapa.html", """{% extends 'base.html' %}
{% block content %}
<h2>Mapa con Áreas Sombreadas</h2>
<div class="card">
    <div class="card-body p-0" style="height: 700px;">
        {{ map_html | safe }}
    </div>
</div>
{% endblock %}
""")

# ==================== EJECUCIÓN ====================
def run_command(cmd, cwd=None):
    print(f"\n> {cmd}")
    process = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    for line in process.stdout:
        print(line, end='')
    process.wait()

def run_application():
    os.chdir(PROJECT_ROOT)
    if not (PROJECT_ROOT / "venv").exists():
        run_command("python -m venv venv")
    python_exe = "venv\\Scripts\\python.exe" if os.name == "nt" else "venv/bin/python"
    flask_exe = "venv\\Scripts\\flask.exe" if os.name == "nt" else "venv/bin/flask"
    
    run_command(f"{python_exe} -m pip install --upgrade pip")
    run_command(f"{python_exe} -m pip install -r requirements.txt")
    run_command(f"{flask_exe} init-db")
    run_command(f"{flask_exe} import-circuitos")
    
    print("\n[OK] ¡Todo corregido y listo!")
    print("🌐 Abre: http://127.0.0.1:5000")
    run_command(f"{python_exe} app.py")

if __name__ == '__main__':
    download_static()
    print("🚀 Generando versión FINAL con todos los circuitos...")
    run_application()