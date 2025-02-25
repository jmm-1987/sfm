from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import db
from datetime import date
from models import User, Expedicion, Cliente, Vehiculo
from metodos.grabar_expedicion import ruta_grabar_expedidion
from metodos.grabar_cliente import ruta_grabar_cliente
from metodos.grabar_vehiculo import ruta_grabar_vehiculo
from metodos.editar_expedicion import ruta_editar_expedicion
from metodos.asignar_expedicion import ruta_asignar_expedicion
from metodos.imprimir_etiqueta import ruta_imprimir_etiqueta
from metodos.imprimir_albaran import ruta_imprimir_albaran
from metodos.asignar_reparto import ruta_asignar_reparto
from metodos.entregar_expedicion import ruta_entregar_expedicion
from metodos.consultar_expedicion import ruta_consultar_expedicion
from metodos.editar_vehiculo import ruta_editar_vehiculo
from metodos.editar_cliente import ruta_editar_cliente
from metodos.exportar_pdf_facturacion import route_exportar_pdf_facturacion
from metodos.retasar_ingreso_distribucion import ruta_retasar_ingreso_distribucion
from metodos.editar_expedicion_simple import ruta_editar_expedicion_simple



# Configuración de la app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '78587fgrtyth'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ruta_grabar_expedidion(app)
ruta_grabar_cliente(app)
ruta_grabar_vehiculo(app)
ruta_editar_expedicion(app)
ruta_asignar_expedicion(app)
ruta_imprimir_etiqueta(app)
ruta_imprimir_albaran(app)
ruta_asignar_reparto(app)
ruta_entregar_expedicion(app)
ruta_consultar_expedicion(app)
ruta_editar_vehiculo(app)
ruta_editar_cliente(app)
route_exportar_pdf_facturacion(app)
ruta_retasar_ingreso_distribucion(app)
ruta_editar_expedicion_simple(app)



# Modelo de usuario básico (para fines de ejemplo)
class User(UserMixin):
    def __init__(self, id):
        self.id = id


# Cargar usuarios
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Ruta para la página de inicio
@app.route('/')
def index():
    return redirect(url_for('login'))


# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Aquí puedes verificar las credenciales desde una base de datos
        if (username == 'santi' and password == 'santi_chico25') or (username == 'oficina' and password == 'oficina25'):
            user = User(id=username)
            login_user(user)
            return redirect(url_for('repartos'))
        else:
            return "Credenciales inválidas", 401

    return render_template('login.html')




@app.route('/vehiculos')
@login_required
def vehiculos():
    vehiculos = db.session.query(Vehiculo).all()  # Obtener todas las expediciones
    return render_template("vehiculos.html", vehiculos=vehiculos)

@app.route('/importaciones')
@login_required
def importaciones():

    return render_template("importaciones.html")


@app.route('/repartos')
@login_required
def repartos():
    vehiculos = db.session.query(Vehiculo.matricula).all()
    clientes = db.session.query(Cliente.alias).all()
    agencias = ["SFM","PALLEX","SEYTRA","TyD","TEDi","REDPALLETS"]
    tipo_bulto = ["MQTR","QTR","MLIGHT","HALF","LIGHT","FULL","MEGAFULL"]
    expedicion_id = request.args.get("id")
    expedicion = get_expedicion_by_id(expedicion_id) if expedicion_id else None
    expediciones = db.session.query(Expedicion).filter(Expedicion.estado != "entregado").order_by(Expedicion.fecha.desc()).all()
    fecha_actual = date.today().strftime('%Y-%m-%d')

    return render_template("repartos.html", expediciones=expediciones, clientes=clientes,
                           vehiculos=vehiculos, expedicion=expedicion, agencias=agencias, fecha_actual=fecha_actual,
                           tipo_bulto=tipo_bulto)

@app.route("/get_expedicion_by_id")
def get_expedicion_by_id(expedicion_id):

    if not expedicion_id:
        return None

    # Busca la expedición por su ID en la base de datos
    expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id).first()

    return expedicion

@app.route("/get_cliente_by_alias")
def get_cliente_by_alias(cliente_alias):

    if not cliente_alias:
        return None

    # Busca la expedición por su ID en la base de datos
    cliente = db.session.query(Cliente).filter_by(alias=cliente_alias).first()

    return cliente



@app.route('/clientes')
@login_required
def clientes():
    tarifas=["no aplica","06PX25_"]
    clientes = db.session.query(Cliente).all()  # Obtener todas las expediciones
    cliente_alias = request.args.get("alias")
    cliente = get_cliente_by_alias(cliente_alias) if cliente_alias else None
    return render_template("clientes.html", clientes=clientes, tarifas=tarifas, cliente=cliente)

@app.route('/facturacion')
@login_required
def facturacion():
    expediciones = db.session.query(Expedicion).all()  # Obtener todas las expediciones
    expedicion_id = request.args.get("id")
    expedicion = get_expedicion_by_id(expedicion_id) if expedicion_id else None
    return render_template("facturacion.html", expedicion=expedicion,expediciones=expediciones)

@app.route('/produccion')
@login_required
def produccion():
    expediciones = db.session.query(Expedicion).all()  # Obtener todas las expediciones
    return render_template("produccion.html", expediciones=expediciones)

@app.route('/cerrar_repartos')
@login_required
def cerrar_repartos():
    expediciones_asignadas = db.session.query(Expedicion).filter(Expedicion.estado == "en reparto").all()
    return render_template("cerrar_repartos.html", expediciones_asignadas=expediciones_asignadas)



# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Ejecutar la aplicación
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)

