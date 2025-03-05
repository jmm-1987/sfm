from db import session
from models import Cliente
from flask import request, redirect, url_for, render_template, flash

def ruta_grabar_cliente(app):
    @app.route('/grabar_cliente', methods=['POST'])
    def grabar_cliente():
        try:
            # Obtener los datos del formulario
            alias = request.form.get('alias').strip()
            nombre_fiscal = request.form.get('nombre_fiscal').strip()
            direccion = request.form.get('direccion')
            codigo_postal = request.form.get('codigo_postal')
            poblacion = request.form.get('poblacion')
            provincia = request.form.get('provincia')
            pais = request.form.get('pais')
            telefono = request.form.get('telefono')
            cif = request.form.get('cif')
            notas = request.form.get('notas')
            tarifa = request.form.get('tarifa')
            email = request.form.get('email')
            activo = request.form.get('estado', True)  # Estado por defecto: 'activo'

            # Verificar si el alias ya existe
            alias_existente = session.query(Cliente).filter_by(alias=alias).first()
            if alias_existente:
                flash("Error: El alias ya está en uso por otro cliente.", "error")
                return redirect(url_for('clientes'))

            # Verificar si el nombre fiscal ya existe
            nombre_existente = session.query(Cliente).filter_by(nombre_fiscal=nombre_fiscal).first()
            if nombre_existente:
                flash("Error: El nombre fiscal ya está en uso por otro cliente.", "error")
                return redirect(url_for('clientes'))

            # Crear una nueva instancia de Cliente si no hay duplicados
            nuevo_cliente = Cliente(
                alias=alias,
                nombre_fiscal=nombre_fiscal,
                direccion=direccion,
                codigo_postal=codigo_postal,
                poblacion=poblacion,
                provincia=provincia,
                pais=pais,
                telefono=telefono,
                tarifa=tarifa,
                email=email,
                cif=cif,
                notas=notas,
                activo=activo
            )

            # Guardar en la base de datos
            session.add(nuevo_cliente)
            session.commit()
            flash("Cliente grabado con éxito.", "success")

            # Redirigir a la página de clientes con la lista actualizada
            return redirect(url_for('clientes'))

        except Exception as e:
            # Si hay un error, hacer rollback y mostrar mensaje de error
            session.rollback()
            flash(f"Error al grabar el cliente: {e}", "error")
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
