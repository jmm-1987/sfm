from db import session
from models import Vehiculo
from flask import request, redirect, url_for, render_template
import db
from datetime import datetime

def ruta_grabar_vehiculo(app):
    @app.route('/grabar_vehiculo', methods=['POST'])
    def grabar_vehiculo():
        try:
            # Obtener los datos del formulario
            matricula = request.form.get('matricula')
            capacidad = request.form.get('capacidad')
            caducidad_itv = request.form.get('caducidad_itv')
            caducidad_seguro = request.form.get('caducidad_seguro')
            caducidad_tacografo = request.form.get('caducidad_tacografo')
            chofer_habitual = request.form.get('chofer_habitual')

            # Convertir las fechas de string a objetos date
            formato_fecha = "%Y-%m-%d"  # Asegúrate de que el formato coincida con el del formulario
            caducidad_itv = datetime.strptime(caducidad_itv, formato_fecha).date() if caducidad_itv else None
            caducidad_seguro = datetime.strptime(caducidad_seguro, formato_fecha).date() if caducidad_seguro else None
            caducidad_tacografo = datetime.strptime(caducidad_tacografo, formato_fecha).date() if caducidad_tacografo else None

            # Crear una nueva instancia de Vehiculo
            nuevo_vehiculo = Vehiculo(
                matricula=matricula,
                capacidad=capacidad,
                caducidad_itv=caducidad_itv,
                caducidad_seguro=caducidad_seguro,
                caducidad_tacografo=caducidad_tacografo,
                chofer_habitual=chofer_habitual
            )

            # Guardar en la base de datos
            session.add(nuevo_vehiculo)
            session.commit()
            print("Vehículo grabado con éxito.")

            # Obtener todos los vehículos y renderizar la plantilla
            vehiculos = db.session.query(Vehiculo).all()
            return render_template("vehiculos.html", vehiculos=vehiculos)

        except Exception as e:
            # Si hay un error, hacer rollback y mostrar mensaje de error
            session.rollback()
            print(f"Error al grabar el vehículo: {e}")
            return redirect(url_for('error_grabar_vehiculo'))

        finally:
            # Cerrar la sesión
            session.close()

    @app.route('/exito_grabar_vehiculo')
    def exito_grabar_vehiculo():
        return "El vehículo se ha grabado con éxito."

    @app.route('/error_grabar_vehiculo')
    def error_grabar_vehiculo():
        return "Hubo un error al grabar el vehículo. Por favor, inténtalo de nuevo más tarde."
