from db import session
from models import Cliente
from flask import request, redirect, url_for, render_template
import db

def ruta_grabar_cliente(app):
    @app.route('/grabar_cliente', methods=['POST'])
    def grabar_cliente():
        try:
            # Obtener los datos del formulario
            alias = request.form.get('alias')
            nombre_fiscal = request.form.get('nombre_fiscal')
            direccion = request.form.get('direccion')
            codigo_postal = request.form.get('codigo_postal')
            poblacion = request.form.get('poblacion')
            provincia = request.form.get('provincia')
            pais = request.form.get('pais')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            activo = request.form.get('estado', True)  # Estado por defecto: 'activo'

            # Crear una nueva instancia de Cliente
            nuevo_cliente = Cliente(
                alias=alias,
                nombre_fiscal=nombre_fiscal,
                direccion=direccion,
                codigo_postal=codigo_postal,
                poblacion=poblacion,
                provincia=provincia,
                pais=pais,
                telefono=telefono,
                email=email,
                activo=activo
            )

            # Guardar en la base de datos
            session.add(nuevo_cliente)
            session.commit()
            print("Cliente grabado con éxito.")

            # Obtener todos los clientes y renderizar la plantilla
            clientes = db.session.query(Cliente).all()
            return render_template("clientes.html", clientes=clientes)

        except Exception as e:
            # Si hay un error, hacer rollback y mostrar mensaje de error
            session.rollback()
            print(f"Error al grabar el cliente: {e}")
            return redirect(url_for('error_grabar_cliente'))

        finally:
            # Cerrar la sesión
            session.close()

    @app.route('/exito_grabar_cliente')
    def exito_grabar_cliente():
        return "El cliente se ha grabado con éxito."

    @app.route('/error_grabar_cliente')
    def error_grabar_cliente():
       return "Hubo un error al grabar el cliente. Por favor, inténtalo de nuevo más tarde."
