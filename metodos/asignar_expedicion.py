from flask import request, redirect, url_for
import db
from models import Expedicion
from datetime import datetime

def ruta_asignar_expedicion(app):
    @app.route('/asignar_expedicion', methods=['POST'])
    def asignar_expedicion():
        expedicion_form = request.form.get('expedicion')
        vehiculo = request.form.get('matricula')

        expedicion_id = db.session.query(Expedicion).filter_by(expedicion=expedicion_form).first()

        if not expedicion_id:
            return redirect(url_for('asignar_reparto', error='Expedición no encontrada'))


        expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id.id).first()

        # Actualizar los campos de la expedición
        fecha_str = request.form['fecha_asignacion']
        fecha_asignacion = datetime.strptime(fecha_str, "%Y-%m-%d")
        expedicion.fecha_asignacion = fecha_asignacion
        expedicion.asignada_a = vehiculo
        expedicion.estado = "en reparto"

        db.session.commit()

        expediciones_asignadas = db.session.query(Expedicion).filter(

            Expedicion.asignada_a == vehiculo
        ).all()



        # Redirigir con los parámetros necesarios para restaurar el estado
        return redirect(url_for('asignar_reparto', matricula=vehiculo, fecha_asignacion=str(fecha_asignacion)))
