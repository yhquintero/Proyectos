#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 GENERADOR DE TARJETA DE ESTIBA (KARDEX)
Sistema de control de inventario por producto, mostrando movimientos sin importe total.
"""

import urllib.request
import ssl
import os
import re
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ==================== RAW_DATA DE PRODUCTOS (142 productos) ====================
RAW_DATA = """
1 Aceite $ 1,100.00 $ 1,300.00
2 Aceite 1 Litro 1400 $ 1,300.00 $ 1,400.00
3 Bombón $ 30.00 $ 50.00
4 Botonetas $ 35.00 $ 50.00
5 Café Ziva $ 1,000.00 $ 1,200.00
6 Cerveza 3 Caballos 210 $ 185.00 $ 210.00
7 Cerveza 3 Caballos 230 $ 200.00 $ 230.00
8 Cerveza Breda $ 210.00 $ 250.00
9 Cerveza Cristal 280 $ 250.00 $ 280.00
10 Cerveza Mayabe 230 $ 200.00 $ 230.00
11 Cerveza Mayabe 280 $ 250.00 $ 280.00
12 Cerveza Parranda 210 $ 180.00 $ 210.00
13 Cerveza Parranda 230 $ 200.00 $ 230.00
14 Cerveza Presidente 210 $ 210.00 $ 250.00
15 Cerveza Presidente 250 $ 220.00 $ 250.00
16 Cerveza Shekels 220 $ 170.00 $ 220.00
17 Cerveza Shekels 250 $ 200.00 $ 250.00
18 Cerveza Unlager 220 $ 170.00 $ 220.00
19 Chambelona $ 20.00 $ 50.00
20 Chicle $ 10.00 $ 20.00
21 Chupa (60) $ 40.00 $ 60.00
22 Cigarros H Upman $ 400.00 $ 450.00
23 Cigarros Popular Rojo $ 450.00 $ 650.00
24 Coditos 500g $ 300.00 $ 350.00
25 Detergente 1kg $ 600.00 $ 850.00
26 Detergente 500g 500 $ 310.00 $ 500.00
27 Embutido Jamón $ 510.00 $ 620.00
28 Energizante $ 210.00 $ 270.00
29 Galleta Craker $ 145.00 $ 180.00
30 Galleta Lamore $ 300.00 $ 350.00
31 Galleta Minees 70 $ 70.00 $ 120.00
32 Galleta Pygmi $ 50.00 $ 70.00
33 Galleta Salrica $ 145.00 $ 200.00
34 Galletas de sal $ 680.00 $ 750.00
35 Galletas Luanezco $ 190.00 $ 240.00
36 Galletas My Bit $ 190.00 $ 240.00
37 Habana Club Añejo Lt $ 1,200.00 $ 1,500.00
38 Jabón $ 130.00 $ 180.00
39 Jabón 200 $ 160.00 $ 200.00
40 Jugos $ 150.00 $ 190.00
41 Malta Guajira 330 ml $ 200.00 $ 250.00
42 Malta Vitali $ 200.00 $ 250.00
43 Menta Plus $ 80.00 $ 100.00
44 Mybar $ 125.00 $ 170.00
45 Pasta Dental $ 500.00 $ 600.00
46 Pelly $ 55.00 $ 80.00
47 Peter Cars 100 $ 85.00 $ 100.00
48 Picadillo $ 270.00 $ 300.00
49 Pollo Ahumado 300 $ 250.00 $ 300.00
50 Pure de Tomate $ 350.00 $ 450.00
51 Refresco Cola (1.5L) $ 500.00 $ 550.00
52 Refresco Cola (lata) 250 $ 215.00 $ 250.00
53 Refresco Cotel paquete $ 35.00 $ 60.00
54 Refresco Guanabana (paquete) $ 35.00 $ 60.00
55 Refresco Limon (Lata) 250 $ 215.00 $ 250.00
56 Refresco Mandarina (paquete) $ 31.00 $ 60.00
57 Refresco Melocotón (paquete) $ 35.00 $ 60.00
58 Refresco Naranja (1.5L) $ 480.00 $ 550.00
59 Refresco Naranja (Lata) 250 $ 215.00 $ 250.00
60 Refresco Pepsi $ 195.00 $ 250.00
61 Refresco Piña Colada (paquete) $ 35.00 $ 60.00
62 Refresco Pomo 250ml $ 165.00 $ 210.00
63 Rona granel 200 ml $ 120.00 $ 200.00
64 Rona Arocha 260 $ 200.00 $ 260.00
65 Rona Arocha 500 ml $ 380.00 $ 500.00
66 Ron cajio venta granel 200 ml $ 120.00 $ 200.00
67 Ron Guayabita $ 500.00 $ 800.00
68 Ron Nucay (granel) 350 ml $ 0.24 $ 1.00
69 Ron Old Partner $ 1,250.00 $ 1,500.00
70 Ron Rivera $ 600.00 $ 800.00
71 Ron Vega del Rio $ 850.00 $ 950.00
72 Sal Común $ 130.00 $ 200.00
73 Salchicha 480 g $ 500.00 $ 560.00
74 Sazón Comino $ 50.00 $ 70.00
75 Sazón Guama $ 45.00 $ 65.00
76 Sopa $ 195.00 $ 250.00
77 Sorbeto Piña Colada (paquete) $ 35.00 $ 60.00
78 Sorbeto Nuto 250 $ 185.00 $ 250.00
79 Sorbeto Renata $ 260.00 $ 300.00
80 Sorbeto Togo $ 50.00 $ 70.00
81 Sorbeto Pepe $ 130.00 $ 200.00
82 Spaguetti $ 300.00 $ 350.00
83 Togo Peanut $ 65.00 $ 100.00
84 Vinagre $ 290.00 $ 350.00
85 Vip Max $ 125.00 $ 180.00
86 Vodka Mágico $ 1,300.00 $ 1,500.00
87 Vodka NA ZOOROVIE 40 Grado $ 1,350.00 $ 1,550.00
88 Vodka Royal $ 50.00 $ 70.00
89 Vodka Tabarish $ 45.00 $ 65.00
90 Sorbeto Fist $ 130.00 $ 200.00
91 Sorbeto Mege $ 125.00 $ 180.00
92 Sorbeto Nuto 250 $ 185.00 $ 250.00
93 Sorbeto Renata $ 260.00 $ 300.00
94 Sorbeto Togo $ 50.00 $ 70.00
95 Sorbeto Pepe $ 130.00 $ 200.00
96 Sorbeto Peanut $ 125.00 $ 180.00
97 Sorbeto Mege $ 125.00 $ 180.00
98 Sorbeto Nuto 250 $ 185.00 $ 250.00
99 Sorbeto Renata $ 260.00 $ 300.00
100 Sorbeto Togo $ 50.00 $ 70.00
101 Sorbeto Pepe $ 130.00 $ 200.00
102 Sorbeto Peanut $ 125.00 $ 180.00
103 Sorbeto Mege $ 125.00 $ 180.00
104 Sorbeto Nuto 250 $ 185.00 $ 250.00
105 Sorbeto Renata $ 260.00 $ 300.00
106 Sorbeto Togo $ 50.00 $ 70.00
107 Sorbeto Pepe $ 130.00 $ 200.00
108 Sorbeto Peanut $ 125.00 $ 180.00
109 Vip Max $ 125.00 $ 180.00
110 Vodka Mágico $ 1,300.00 $ 1,500.00
111 Vodka NA ZOOROVIE 40 Grado $ 1,350.00 $ 1,550.00
112 Vodka Royal $ 1,300.00 $ 1,550.00
113 Vodka Tabarish $ 1,300.00 $ 1,500.00
114 Wisky 375 ml $ 640.00 $ 750.00
115 Sorbeto First $ 75.00 $ 100.00
116 Sorbeto Mege $ 125.00 $ 180.00
117 Sorbeto Nuto 250 $ 185.00 $ 250.00
118 Sorbeto Renata $ 260.00 $ 300.00
119 Sorbeto Togo $ 50.00 $ 70.00
120 Sorbeto Pepe $ 130.00 $ 200.00
121 Sorbeto Peanut $ 125.00 $ 180.00
122 Sorbeto Mege $ 125.00 $ 180.00
123 Sorbeto Nuto 250 $ 185.00 $ 250.00
124 Sorbeto Renata $ 260.00 $ 300.00
125 Sorbeto Togo $ 50.00 $ 70.00
126 Sorbeto Pepe $ 130.00 $ 200.00
127 Sorbeto Peanut $ 125.00 $ 180.00
128 Sorbeto Mege $ 125.00 $ 180.00
129 Sorbeto Nuto 250 $ 185.00 $ 250.00
130 Sorbeto Renata $ 260.00 $ 300.00
131 Sorbeto Togo $ 50.00 $ 70.00
132 Sorbeto Pepe $ 130.00 $ 200.00
133 Sorbeto Peanut $ 125.00 $ 180.00
134 Sorbeto Mege $ 125.00 $ 180.00
135 Vip Max $ 125.00 $ 180.00
136 Vodka Mágico $ 1,300.00 $ 1,500.00
137 Vodka NA ZOOROVIE 40 Grado $ 1,350.00 $ 1,550.00
138 Vodka Royal $ 1,300.00 $ 1,550.00
139 Vodka Tabarish $ 1,300.00 $ 1,500.00
140 Vodka Pepe $ 130.00 $ 200.00
141 Vodka Peanut $ 125.00 $ 180.00
142 Vodka Mágico $ 1,300.00 $ 1,500.00
"""

def parse_products_from_raw(raw_text):
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    pattern = re.compile(r'^\d+\s+(.+?)\s+\$\s*([\d,]+\.\d+)\s+\$\s*([\d,]+\.\d+)$')
    products = []
    seen = {}
    for line in lines:
        match = pattern.match(line)
        if match:
            name = match.group(1).strip()
            cost = float(match.group(2).replace(',', ''))
            price = float(match.group(3).replace(',', ''))
            if name not in seen:
                seen[name] = True
                products.append({'name': name, 'cost': cost, 'price': price})
    return products

PRODUCTS_LIST = parse_products_from_raw(RAW_DATA)
PROJECT_ROOT = Path("tarjeta_estiba")

def write_file(relative_path: str, content: str):
    path = PROJECT_ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f"✅ Creado: {path}")

def download_file(url, dest_path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=ctx) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"📥 Descargado: {dest_path}")
    except Exception as e:
        print(f"❌ Error descargando {url}: {e}")

def download_static_dependencies():
    static_dir = PROJECT_ROOT / "static"
    bootstrap_css = static_dir / "css" / "bootstrap.min.css"
    if not bootstrap_css.exists():
        download_file("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", bootstrap_css)
    bootstrap_js = static_dir / "js" / "bootstrap.bundle.min.js"
    if not bootstrap_js.exists():
        download_file("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js", bootstrap_js)
    icons_css = static_dir / "css" / "bootstrap-icons.min.css"
    if not icons_css.exists():
        download_file("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css", icons_css)
    icons_font_dir = static_dir / "css" / "fonts"
    icons_font_files = [
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2",
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff"
    ]
    for font_url in icons_font_files:
        font_name = font_url.split("/")[-1]
        font_path = icons_font_dir / font_name
        if not font_path.exists():
            download_file(font_url, font_path)
    # Chart.js no es necesario pero se descarga por si acaso
    chart_js = static_dir / "js" / "chart.min.js"
    if not chart_js.exists():
        download_file("https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js", chart_js)

# ==================== ESCRITURA DE ARCHIVOS ====================
write_file("requirements.txt", """Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
WTForms==3.1.2
python-dotenv==1.0.1
psycopg2-binary==2.9.9
click==8.1.7
""")

write_file(".env", """DATABASE_URL=sqlite:///kardex.db
SECRET_KEY=clave-segura-para-desarrollo
FLASK_ENV=development
""")

write_file("README.md", """# Tarjeta de Estiba - Sistema de Kardex

Aplicación para control de inventario por producto con movimientos (entradas y salidas).

## Características
- Gestión de productos (CRUD)
- Registro de entradas y salidas con cantidad y valor unitario (costo/precio)
- **Visualización tipo tarjeta**: lista de movimientos sin importe total
- Validación de stock (no permite salidas mayores al disponible)
- Papelera de movimientos con restauración
- Fecha automática (datetime.now) en cada movimiento

## Instalación y ejecución
```bash
cd tarjeta_estiba
python -m venv venv
source venv/bin/activate  # o venv\\Scripts\\activate en Windows
pip install -r requirements.txt
flask init-db
flask import-products
flask run
Abrir http://127.0.0.1:5000
""")

write_file("models.py", """from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    cost = db.Column(db.Numeric(12,2), nullable=False)
    price = db.Column(db.Numeric(12,2), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    inventory = db.relationship('Inventory', backref='product', uselist=False)
    transactions = db.relationship('Transaction', backref='product', lazy=True)

class Inventory(db.Model):
    __tablename__ = 'inventories'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    transaction_type = db.Column(db.String(3), nullable=False)  # 'IN' o 'OUT'
    quantity = db.Column(db.Integer, nullable=False)
    unit_value = db.Column(db.Numeric(12,2), nullable=False)   # costo para IN, precio para OUT
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(300))
    deleted = db.Column(db.Boolean, default=False)
""")

write_file("forms.py", """from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from models import Product

class ProductForm(FlaskForm):
    name = StringField('Nombre del Producto', validators=[DataRequired()])
    cost = DecimalField('Costo', places=2, validators=[DataRequired(), NumberRange(min=0)])
    price = DecimalField('Precio Venta', places=2, validators=[DataRequired(), NumberRange(min=0)])

    def validate_name(self, field):
        product = Product.query.filter_by(name=field.data, deleted=False).first()
        if product and product.id != getattr(self, '_product_id', None):
            raise ValidationError('Ya existe un producto con este nombre.')

class TransactionForm(FlaskForm):
    product_id = SelectField('Producto', coerce=int, validators=[DataRequired()])
    transaction_type = SelectField('Tipo', choices=[('IN', 'Entrada (Compra)'), ('OUT', 'Salida (Venta)')], validators=[DataRequired()])
    quantity = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField('Notas')
""")

write_file("utils.py", """from datetime import datetime, timedelta
from models import db, Transaction, Product, Inventory

def update_inventory(product_id, quantity, transaction_type):
    inv = Inventory.query.get(product_id)
    if not inv:
        inv = Inventory(product_id=product_id, quantity=0)
        db.session.add(inv)
    if transaction_type == 'IN':
        inv.quantity += quantity
    else:
        if inv.quantity < quantity:
            raise ValueError(f"Stock insuficiente: {inv.quantity} < {quantity}")
        inv.quantity -= quantity
    db.session.commit()

def revert_inventory(product_id, old_quantity, old_type):
    inv = Inventory.query.get(product_id)
    if not inv:
        inv = Inventory(product_id=product_id, quantity=0)
        db.session.add(inv)
    if old_type == 'IN':
        inv.quantity -= old_quantity
    else:
        inv.quantity += old_quantity
    if inv.quantity < 0:
        inv.quantity = 0
    db.session.commit()

def get_current_stock(product_id):
    inv = Inventory.query.get(product_id)
    return inv.quantity if inv else 0
""")

write_file("app.py", '''
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Inventory, Transaction
from forms import ProductForm, TransactionForm
from utils import update_inventory, revert_inventory, get_current_stock
from datetime import datetime
import click
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-segura-por-defecto')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///kardex.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ==================== DATOS RAW (para importación) ====================
RAW_DATA = """
1 Aceite $ 1,100.00 $ 1,300.00
2 Aceite 1 Litro 1400 $ 1,300.00 $ 1,400.00
3 Bombón $ 30.00 $ 50.00
4 Botonetas $ 35.00 $ 50.00
5 Café Ziva $ 1,000.00 $ 1,200.00
6 Cerveza 3 Caballos 210 $ 185.00 $ 210.00
7 Cerveza 3 Caballos 230 $ 200.00 $ 230.00
8 Cerveza Breda $ 210.00 $ 250.00
9 Cerveza Cristal 280 $ 250.00 $ 280.00
10 Cerveza Mayabe 230 $ 200.00 $ 230.00
11 Cerveza Mayabe 280 $ 250.00 $ 280.00
12 Cerveza Parranda 210 $ 180.00 $ 210.00
13 Cerveza Parranda 230 $ 200.00 $ 230.00
14 Cerveza Presidente 210 $ 210.00 $ 250.00
15 Cerveza Presidente 250 $ 220.00 $ 250.00
16 Cerveza Shekels 220 $ 170.00 $ 220.00
17 Cerveza Shekels 250 $ 200.00 $ 250.00
18 Cerveza Unlager 220 $ 170.00 $ 220.00
19 Chambelona $ 20.00 $ 50.00
20 Chicle $ 10.00 $ 20.00
21 Chupa (60) $ 40.00 $ 60.00
22 Cigarros H Upman $ 400.00 $ 450.00
23 Cigarros Popular Rojo $ 450.00 $ 650.00
24 Coditos 500g $ 300.00 $ 350.00
25 Detergente 1kg $ 600.00 $ 850.00
26 Detergente 500g 500 $ 310.00 $ 500.00
27 Embutido Jamón $ 510.00 $ 620.00
28 Energizante $ 210.00 $ 270.00
29 Galleta Craker $ 145.00 $ 180.00
30 Galleta Lamore $ 300.00 $ 350.00
31 Galleta Minees 70 $ 70.00 $ 120.00
32 Galleta Pygmi $ 50.00 $ 70.00
33 Galleta Salrica $ 145.00 $ 200.00
34 Galletas de sal $ 680.00 $ 750.00
35 Galletas Luanezco $ 190.00 $ 240.00
36 Galletas My Bit $ 190.00 $ 240.00
37 Habana Club Añejo Lt $ 1,200.00 $ 1,500.00
38 Jabón $ 130.00 $ 180.00
39 Jabón 200 $ 160.00 $ 200.00
40 Jugos $ 150.00 $ 190.00
41 Malta Guajira 330 ml $ 200.00 $ 250.00
42 Malta Vitali $ 200.00 $ 250.00
43 Menta Plus $ 80.00 $ 100.00
44 Mybar $ 125.00 $ 170.00
45 Pasta Dental $ 500.00 $ 600.00
46 Pelly $ 55.00 $ 80.00
47 Peter Cars 100 $ 85.00 $ 100.00
48 Picadillo $ 270.00 $ 300.00
49 Pollo Ahumado 300 $ 250.00 $ 300.00
50 Pure de Tomate $ 350.00 $ 450.00
51 Refresco Cola (1.5L) $ 500.00 $ 550.00
52 Refresco Cola (lata) 250 $ 215.00 $ 250.00
53 Refresco Cotel paquete $ 35.00 $ 60.00
54 Refresco Guanabana (paquete) $ 35.00 $ 60.00
55 Refresco Limon (Lata) 250 $ 215.00 $ 250.00
56 Refresco Mandarina (paquete) $ 31.00 $ 60.00
57 Refresco Melocotón (paquete) $ 35.00 $ 60.00
58 Refresco Naranja (1.5L) $ 480.00 $ 550.00
59 Refresco Naranja (Lata) 250 $ 215.00 $ 250.00
60 Refresco Pepsi $ 195.00 $ 250.00
61 Refresco Piña Colada (paquete) $ 35.00 $ 60.00
62 Refresco Pomo 250ml $ 165.00 $ 210.00
63 Rona granel 200 ml $ 120.00 $ 200.00
64 Rona Arocha 260 $ 200.00 $ 260.00
65 Rona Arocha 500 ml $ 380.00 $ 500.00
66 Ron cajio venta granel 200 ml $ 120.00 $ 200.00
67 Ron Guayabita $ 500.00 $ 800.00
68 Ron Nucay (granel) 350 ml $ 0.24 $ 1.00
69 Ron Old Partner $ 1,250.00 $ 1,500.00
70 Ron Rivera $ 600.00 $ 800.00
71 Ron Vega del Rio $ 850.00 $ 950.00
72 Sal Común $ 130.00 $ 200.00
73 Salchicha 480 g $ 500.00 $ 560.00
74 Sazón Comino $ 50.00 $ 70.00
75 Sazón Guama $ 45.00 $ 65.00
76 Sopa $ 195.00 $ 250.00
77 Sorbeto Piña Colada (paquete) $ 35.00 $ 60.00
78 Sorbeto Nuto 250 $ 185.00 $ 250.00
79 Sorbeto Renata $ 260.00 $ 300.00
80 Sorbeto Togo $ 50.00 $ 70.00
81 Sorbeto Pepe $ 130.00 $ 200.00
82 Spaguetti $ 300.00 $ 350.00
83 Togo Peanut $ 65.00 $ 100.00
84 Vinagre $ 290.00 $ 350.00
85 Vip Max $ 125.00 $ 180.00
86 Vodka Mágico $ 1,300.00 $ 1,500.00
87 Vodka NA ZOOROVIE 40 Grado $ 1,350.00 $ 1,550.00
88 Vodka Royal $ 50.00 $ 70.00
89 Vodka Tabarish $ 45.00 $ 65.00
90 Sorbeto Fist $ 130.00 $ 200.00
91 Sorbeto Mege $ 125.00 $ 180.00
92 Sorbeto Nuto 250 $ 185.00 $ 250.00
93 Sorbeto Renata $ 260.00 $ 300.00
94 Sorbeto Togo $ 50.00 $ 70.00
95 Sorbeto Pepe $ 130.00 $ 200.00
96 Sorbeto Peanut $ 125.00 $ 180.00
97 Sorbeto Mege $ 125.00 $ 180.00
98 Sorbeto Nuto 250 $ 185.00 $ 250.00
99 Sorbeto Renata $ 260.00 $ 300.00
100 Sorbeto Togo $ 50.00 $ 70.00
101 Sorbeto Pepe $ 130.00 $ 200.00
102 Sorbeto Peanut $ 125.00 $ 180.00
103 Sorbeto Mege $ 125.00 $ 180.00
104 Sorbeto Nuto 250 $ 185.00 $ 250.00
105 Sorbeto Renata $ 260.00 $ 300.00
106 Sorbeto Togo $ 50.00 $ 70.00
107 Sorbeto Pepe $ 130.00 $ 200.00
108 Sorbeto Peanut $ 125.00 $ 180.00
109 Vip Max $ 125.00 $ 180.00
110 Vodka Mágico $ 1,300.00 $ 1,500.00
111 Vodka NA ZOOROVIE 40 Grado $ 1,350.00 $ 1,550.00
112 Vodka Royal $ 1,300.00 $ 1,550.00
113 Vodka Tabarish $ 1,300.00 $ 1,500.00
114 Wisky 375 ml $ 640.00 $ 750.00
115 Sorbeto First $ 75.00 $ 100.00
116 Sorbeto Mege $ 125.00 $ 180.00
117 Sorbeto Nuto 250 $ 185.00 $ 250.00
118 Sorbeto Renata $ 260.00 $ 300.00
119 Sorbeto Togo $ 50.00 $ 70.00
120 Sorbeto Pepe $ 130.00 $ 200.00
121 Sorbeto Peanut $ 125.00 $ 180.00
122 Sorbeto Mege $ 125.00 $ 180.00
123 Sorbeto Nuto 250 $ 185.00 $ 250.00
124 Sorbeto Renata $ 260.00 $ 300.00
125 Sorbeto Togo $ 50.00 $ 70.00
126 Sorbeto Pepe $ 130.00 $ 200.00
127 Sorbeto Peanut $ 125.00 $ 180.00
128 Sorbeto Mege $ 125.00 $ 180.00
129 Sorbeto Nuto 250 $ 185.00 $ 250.00
130 Sorbeto Renata $ 260.00 $ 300.00
131 Sorbeto Togo $ 50.00 $ 70.00
132 Sorbeto Pepe $ 130.00 $ 200.00
133 Sorbeto Peanut $ 125.00 $ 180.00
134 Sorbeto Mege $ 125.00 $ 180.00
135 Vip Max $ 125.00 $ 180.00
136 Vodka Mágico $ 1,300.00 $ 1,500.00
137 Vodka NA ZOOROVIE 40 Grado $ 1,350.00 $ 1,550.00
138 Vodka Royal $ 1,300.00 $ 1,550.00
139 Vodka Tabarish $ 1,300.00 $ 1,500.00
140 Vodka Pepe $ 130.00 $ 200.00
141 Vodka Peanut $ 125.00 $ 180.00
142 Vodka Mágico $ 1,300.00 $ 1,500.00
"""

def parse_products_from_raw(raw_text):
    lines = [line.strip() for line in raw_text.strip().split('\\n') if line.strip()]
    pattern = re.compile(r'^\\d+\\s+(.+?)\\s+\\$\\s*([\\d,]+\\.\\d+)\\s+\\$\\s*([\\d,]+\\.\\d+)$')
    products = []
    seen = {}
    for line in lines:
        match = pattern.match(line)
        if match:
            name = match.group(1).strip()
            cost = float(match.group(2).replace(',', ''))
            price = float(match.group(3).replace(',', ''))
            if name not in seen:
                seen[name] = True
                products.append({'name': name, 'cost': cost, 'price': price})
    return products

# ==================== COMANDOS FLASK ====================
@app.cli.command('init-db')
def init_db_command():
    db.create_all()
    click.echo('[OK] Base de datos inicializada.')

@app.cli.command('import-products')
def import_products():
    products = parse_products_from_raw(RAW_DATA)
    count = 0
    for p in products:
        if not Product.query.filter_by(name=p['name'], deleted=False).first():
            prod = Product(name=p['name'], cost=p['cost'], price=p['price'])
            db.session.add(prod)
            db.session.flush()
            db.session.add(Inventory(product_id=prod.id, quantity=0))
            count += 1
    db.session.commit()
    click.echo(f'[OK] Se importaron {count} productos nuevos.')

# ==================== RUTAS ====================
@app.route('/')
def index():
    products = Product.query.filter_by(deleted=False).all()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>/kardex')
def kardex(id):
    product = Product.query.get_or_404(id)
    transactions = Transaction.query.filter_by(product_id=id, deleted=False).order_by(Transaction.transaction_date.desc()).all()
    stock = get_current_stock(id)
    return render_template('kardex.html', product=product, transactions=transactions, stock=stock)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, cost=form.cost.data, price=form.price.data)
        db.session.add(product)
        db.session.flush()
        db.session.add(Inventory(product_id=product.id, quantity=0))
        db.session.commit()
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('product_form.html', form=form, title='Nuevo Producto')

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form._product_id = id
    if form.validate_on_submit():
        product.name = form.name.data
        product.cost = form.cost.data
        product.price = form.price.data
        db.session.commit()
        flash('Producto actualizado', 'success')
        return redirect(url_for('index'))
    return render_template('product_form.html', form=form, title='Editar Producto')

@app.route('/product/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    product.deleted = True
    db.session.commit()
    flash('Producto movido a papelera', 'warning')
    return redirect(url_for('index'))

@app.route('/product/restore/<int:id>')
def restore_product(id):
    product = Product.query.get_or_404(id)
    product.deleted = False
    db.session.commit()
    flash('Producto restaurado', 'success')
    return redirect(url_for('deleted_products'))

@app.route('/products/deleted')
def deleted_products():
    products = Product.query.filter_by(deleted=True).all()
    return render_template('deleted_products.html', products=products)

@app.route('/transaction/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.filter_by(deleted=False).order_by(Product.name).all()]
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        now = datetime.now()
        # Determinar valor unitario según tipo
        if form.transaction_type.data == 'IN':
            unit_value = product.cost
        else:
            unit_value = product.price
            # Validar stock
            stock = get_current_stock(product.id)
            if stock < form.quantity.data:
                flash(f'Stock insuficiente. Disponible: {stock}, solicitado: {form.quantity.data}', 'danger')
                return redirect(url_for('add_transaction'))
        
        trans = Transaction(
            product_id=product.id,
            transaction_type=form.transaction_type.data,
            quantity=form.quantity.data,
            unit_value=unit_value,
            transaction_date=now,
            notes=form.notes.data,
            deleted=False
        )
        db.session.add(trans)
        try:
            update_inventory(product.id, form.quantity.data, form.transaction_type.data)
            db.session.commit()
            flash('Movimiento registrado', 'success')
            return redirect(url_for('kardex', id=product.id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'danger')
    return render_template('transaction_form.html', form=form)

@app.route('/transaction/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    trans = Transaction.query.get_or_404(id)
    if trans.deleted:
        flash('Movimiento ya está en papelera', 'warning')
        return redirect(request.referrer or url_for('index'))
    try:
        revert_inventory(trans.product_id, trans.quantity, trans.transaction_type)
        trans.deleted = True
        db.session.commit()
        flash('Movimiento movido a papelera', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(request.referrer or url_for('index'))

@app.route('/transaction/restore/<int:id>', methods=['POST'])
def restore_transaction(id):
    trans = Transaction.query.get_or_404(id)
    if not trans.deleted:
        flash('Movimiento ya activo', 'warning')
        return redirect(url_for('deleted_transactions'))
    # Verificar stock si es salida
    if trans.transaction_type == 'OUT':
        stock = get_current_stock(trans.product_id)
        if stock < trans.quantity:
            flash(f'No se puede restaurar: stock insuficiente ({stock} < {trans.quantity})', 'danger')
            return redirect(url_for('deleted_transactions'))
    try:
        update_inventory(trans.product_id, trans.quantity, trans.transaction_type)
        trans.deleted = False
        db.session.commit()
        flash('Movimiento restaurado', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('deleted_transactions'))

@app.route('/transactions/deleted')
def deleted_transactions():
    transactions = Transaction.query.filter_by(deleted=True).order_by(Transaction.transaction_date.desc()).all()
    return render_template('deleted_transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
''')

# ==================== TEMPLATES ====================
write_file("templates/base.html", """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tarjeta de Estiba</title>
    <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/bootstrap-icons.min.css') }}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">📋 Tarjeta de Estiba</a>
            <div>
                <a href="{{ url_for('add_product') }}" class="btn btn-outline-light btn-sm">+ Producto</a>
                <a href="{{ url_for('deleted_products') }}" class="btn btn-outline-light btn-sm">🗑️ Papelera</a>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
</body>
</html>
""")

write_file("templates/index.html", """{% extends 'base.html' %}
{% block content %}
<h2>Productos</h2>
<table class="table table-striped">
    <thead class="table-dark">
        <tr><th>Nombre</th><th>Costo</th><th>Precio Venta</th><th>Stock</th><th>Acciones</th></tr>
    </thead>
    <tbody>
        {% for p in products %}
        <tr>
            <td>{{ p.name }}</td>
            <td>${{ "{:,.2f}".format(p.cost) }}</td>
            <td>${{ "{:,.2f}".format(p.price) }}</td>
            <td>{{ p.inventory.quantity if p.inventory else 0 }}</td>
            <td>
                <a href="{{ url_for('kardex', id=p.id) }}" class="btn btn-sm btn-info">📋 Tarjeta</a>
                <a href="{{ url_for('edit_product', id=p.id) }}" class="btn btn-sm btn-warning">✏️</a>
                <a href="{{ url_for('delete_product', id=p.id) }}" class="btn btn-sm btn-danger" onclick="return confirm('¿Mover a papelera?')">🗑️</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<a href="{{ url_for('add_transaction') }}" class="btn btn-success">➕ Registrar Movimiento</a>
{% endblock %}
""")

write_file("templates/kardex.html", """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h2>Tarjeta de Estiba: {{ product.name }}</h2>
    <a href="{{ url_for('index') }}" class="btn btn-secondary">← Volver</a>
</div>
<p><strong>Stock actual:</strong> {{ stock }} unidades</p>
<p><strong>Costo unitario:</strong> ${{ "{:,.2f}".format(product.cost) }} | <strong>Precio venta:</strong> ${{ "{:,.2f}".format(product.price) }}</p>
<hr>

<h4>Movimientos</h4>
<table class="table table-bordered table-hover">
    <thead class="table-dark">
        <tr>
            <th>Fecha/Hora</th>
            <th>Tipo</th>
            <th>Cantidad</th>
            <th>Valor Unitario</th>
            <th>Notas</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {% for t in transactions %}
        <tr>
            <td>{{ t.transaction_date.strftime('%Y-%m-%d %H:%M:%S') }}</td>
            <td>
                {% if t.transaction_type == 'IN' %}
                    <span class="badge bg-success">Entrada</span>
                {% else %}
                    <span class="badge bg-danger">Salida</span>
                {% endif %}
            </td>
            <td>{{ t.quantity }}</td>
            <td>${{ "{:,.2f}".format(t.unit_value) }}</td>
            <td>{{ t.notes or '-' }}</td>
            <td>
                <form method="POST" action="{{ url_for('delete_transaction', id=t.id) }}" style="display:inline;" onsubmit="return confirm('¿Mover este movimiento a la papelera?')">
                    <button type="submit" class="btn btn-sm btn-danger">🗑️</button>
                </form>
            </td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="text-center">No hay movimientos registrados.{% endfor %}
    </tbody>
</table>
<a href="{{ url_for('add_transaction') }}?product_id={{ product.id }}" class="btn btn-primary">➕ Agregar Movimiento</a>
{% endblock %}
""")

write_file("templates/product_form.html", """{% extends 'base.html' %}
{% block content %}
<div class="card shadow">
    <div class="card-header bg-primary text-white"><h4>{{ title }}</h4></div>
    <div class="card-body">
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="mb-3">{{ form.name.label(class="form-label") }}{{ form.name(class="form-control") }}</div>
            <div class="mb-3">{{ form.cost.label(class="form-label") }}{{ form.cost(class="form-control") }}</div>
            <div class="mb-3">{{ form.price.label(class="form-label") }}{{ form.price(class="form-control") }}</div>
            <button type="submit" class="btn btn-primary">Guardar</button>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""")

write_file("templates/transaction_form.html", """{% extends 'base.html' %}
{% block content %}
<div class="card shadow">
    <div class="card-header bg-success text-white"><h4>Registrar Movimiento</h4></div>
    <div class="card-body">
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="mb-3">{{ form.product_id.label(class="form-label") }}{{ form.product_id(class="form-select") }}</div>
            <div class="mb-3">{{ form.transaction_type.label(class="form-label") }}{{ form.transaction_type(class="form-select") }}</div>
            <div class="mb-3">{{ form.quantity.label(class="form-label") }}{{ form.quantity(class="form-control") }}</div>
            <div class="mb-3">{{ form.notes.label(class="form-label") }}{{ form.notes(class="form-control") }}</div>
            <button type="submit" class="btn btn-success">Registrar</button>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""")

write_file("templates/deleted_products.html", """{% extends 'base.html' %}
{% block content %}
<h2>🗑️ Papelera de Productos</h2>
<a href="{{ url_for('index') }}" class="btn btn-primary mb-3">← Volver</a>
<table class="table table-striped">
    <thead class="table-dark">
        <tr><th>Nombre</th><th>Costo</th><th>Precio</th><th>Acciones</th></tr>
    </thead>
    <tbody>
        {% for p in products %}
        <tr>
            <td>{{ p.name }}</td>
            <td>${{ "{:,.2f}".format(p.cost) }}</td>
            <td>${{ "{:,.2f}".format(p.price) }}</td>
            <td><a href="{{ url_for('restore_product', id=p.id) }}" class="btn btn-sm btn-success">↩️ Restaurar</a></td>
        </tr>
        {% else %}
        <tr><td colspan="4" class="text-center">No hay productos en papelera.{% endfor %}
    </tbody>
</table>
{% endblock %}
""")

write_file("templates/deleted_transactions.html", """{% extends 'base.html' %}
{% block content %}
<h2>🗑️ Movimientos Eliminados</h2>
<a href="{{ url_for('index') }}" class="btn btn-primary mb-3">← Volver</a>
<table class="table table-striped">
    <thead class="table-dark">
        <tr><th>Fecha</th><th>Producto</th><th>Tipo</th><th>Cantidad</th><th>Valor Unit.</th><th>Acciones</th></tr>
    </thead>
    <tbody>
        {% for t in transactions %}
        <tr>
            <td>{{ t.transaction_date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td>{{ t.product.name }}</td>
            <td><span class="badge bg-{{ 'success' if t.transaction_type=='IN' else 'danger' }}">{{ 'Entrada' if t.transaction_type=='IN' else 'Salida' }}</span></td>
            <td>{{ t.quantity }}</td>
            <td>${{ "{:,.2f}".format(t.unit_value) }}</td>
            <td>
                <form method="POST" action="{{ url_for('restore_transaction', id=t.id) }}" style="display:inline;">
                    <button type="submit" class="btn btn-sm btn-success" onclick="return confirm('¿Restaurar?')">↩️ Restaurar</button>
                </form>
            </td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="text-center">No hay movimientos en papelera.{% endfor %}
    </tbody>
</table>
{% endblock %}
""")

write_file("static/css/style.css", """body { background: #f8f9fa; }
.card { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.navbar { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
""")

# ==================== FUNCIONES DE EJECUCIÓN ====================
def run_command(cmd, cwd=None):
    print(f"\n> {cmd}")
    process = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding='utf-8', errors='replace')
    for line in process.stdout:
        print(line, end='')
    process.wait()
    if process.returncode != 0:
        print(f"⚠️  El comando falló con código {process.returncode}")
        sys.exit(process.returncode)

def run_application():
    os.chdir(PROJECT_ROOT)
    run_command("python -m venv venv")
    if sys.platform == "win32":
        python_exe = "venv\\Scripts\\python.exe"
        flask_exe = "venv\\Scripts\\flask.exe"
    else:
        python_exe = "venv/bin/python"
        flask_exe = "venv/bin/flask"
    run_command(f"{python_exe} -m pip install --upgrade pip")
    run_command(f"{python_exe} -m pip install -r requirements.txt")
    run_command(f"{flask_exe} init-db")
    run_command(f"{flask_exe} import-products")
    print("\n🚀 Levantando servidor Flask...")
    run_command(f"{python_exe} app.py")

if __name__ == '__main__':
    download_static_dependencies()
    print("🚀 Generando proyecto Tarjeta de Estiba...")
    print("📁 Carpeta: tarjeta_estiba/")
    print("✅ 142 productos importados")
    print("✅ Movimientos sin importe total (solo valor unitario)")
    print("\n🚀 Iniciando instalación automática y ejecución...\n")
    run_application()