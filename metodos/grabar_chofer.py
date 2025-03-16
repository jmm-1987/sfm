from db import session
from models import Chofer
from flask import request, redirect, url_for, flash

def ruta_grabar_chofer(app):
    @app.route('/grabar_chofer', methods=['POST'])
    def grabar_chofer():
        try:
            # Obtener los datos del formulario
            alias = request.form.get('alias')
            nombre_completo = request.form.get('nombre_completo')
            dni = request.form.get('dni')
            notas = request.form.get('notas')


            # Verificar si la matrícula ya existe en otro vehículo
            chofer_existente = session.query(Chofer).filter_by(alias=alias).first()
            if chofer_existente:
                flash("Error: La conductor ya está en uso.", "error")
                return redirect(url_for('repartidores'))

            # Crear una nueva instancia de Vehiculo
            nuevo_chofer = Chofer(
                alias=alias,
                nombre_completo=nombre_completo,
                dni=dni,
                notas=notas,
            )

            # Guardar en la base de datos
            session.add(nuevo_chofer)
            session.commit()
            flash("Chofer grabado con éxito.", "success")

            # Redirigir a la lista de vehículos
            return redirect(url_for('repartidores'))

        except Exception as e:
            # Si hay un error, hacer rollback y mostrar mensaje de error
            session.rollback()
            flash(f"Error al grabar el chofer: {e}", "error")
            return redirect(url_for('error_grabar_chofer'))

        finally:
            # Cerrar la sesión
            session.close()

    @app.route('/exito_grabar_chofer')
    def exito_grabar_chofer():
        return "El chofer se ha grabado con éxito."

    @app.route('/error_grabar_chofer')
    def error_grabar_chofer():
        return "Hubo un error al grabar el chofer. Por favor, inténtalo de nuevo más tarde."
