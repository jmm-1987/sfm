from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import db
from models import User, Expedicion, Cliente, Vehiculo
from metodos.grabar_expedicion import ruta_grabar_expedidion
from metodos.grabar_cliente import ruta_grabar_cliente
from metodos.grabar_vehiculo import ruta_grabar_vehiculo
from metodos.editar_expedicion import ruta_editar_expedicion
from metodos.asignar_reparto import ruta_asignar_expedicion
from metodos.imprimir_etiqueta import ruta_imprimir_etiqueta
from metodos.imprimir_albaran import ruta_imprimir_albaran





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
        if username == 'santi' and password == 'santi_chico25':  # Ejemplo
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


@app.route('/repartos')
@login_required
def repartos():
    vehiculos = db.session.query(Vehiculo.matricula).all()
    clientes = db.session.query(Cliente.alias).all()
    agencias = ["SFM","PALLEX","SEYTRA","TyD","TEDi","REDPALLETS"]
    expedicion_id = request.args.get("id")
    expedicion = get_expedicion_by_id(expedicion_id) if expedicion_id else None
    expediciones = db.session.query(Expedicion).order_by(Expedicion.fecha.desc()).all()
    return render_template("repartos.html", expediciones=expediciones, clientes=clientes,
                           vehiculos=vehiculos, expedicion=expedicion, agencias=agencias)

@app.route("/get_expedicion_by_id")
def get_expedicion_by_id(expedicion_id):

    if not expedicion_id:
        return None

    # Busca la expedición por su ID en la base de datos
    expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id).first()

    return expedicion



@app.route('/clientes')
@login_required
def clientes():
    clientes = db.session.query(Cliente).all()  # Obtener todas las expediciones
    return render_template("clientes.html", clientes=clientes)

@app.route('/facturacion')
@login_required
def facturacion():
    expediciones = db.session.query(Expedicion).all()  # Obtener todas las expediciones
    return render_template("facturacion.html", expediciones=expediciones)

@app.route('/produccion')
@login_required
def produccion():
    expediciones = db.session.query(Expedicion).all()  # Obtener todas las expediciones
    return render_template("produccion.html", expediciones=expediciones)



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

