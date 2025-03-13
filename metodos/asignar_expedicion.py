from flask import request, redirect, url_for
import db
from models import Expedicion
from datetime import datetime

def ruta_asignar_expedicion(app):
    @app.route('/asignar_expedicion', methods=['POST'])
    def asignar_expedicion():
        expedicion_form = request.form.get('expedicion')
        vehiculo = request.form.get('matricula')

        #Primero busca si existe por id y si el usuario mete una exp, consulta el id a traves de la exp

        expedicion_id = db.session.query(Expedicion).filter_by(id=expedicion_form).first()

        if not expedicion_id:
            expedicion_id = db.session.query(Expedicion.id).filter_by(expedicion=expedicion_form).first()
            print(expedicion_id ,"no es ")

        expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id.id).first()
        print(expedicion.id)

        if not expedicion:
            return redirect(url_for('asignar_reparto', error='Expedición no encontrada'))

        # Actualizar los campos de la expedición
        fecha_str = request.form.get('fecha_asignacion') or request.args.get('fecha_asignacion')

        if fecha_str:
            try:
                fecha_asignacion = datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                return "Formato de fecha incorrecto", 400
        fecha_asignacion = datetime.strptime(fecha_str, "%Y-%m-%d")
        expedicion.fecha_asignacion = fecha_asignacion
        expedicion.asignada_a = vehiculo
        expedicion.estado = "en reparto"

        db.session.commit()

        # Redirigir con los parámetros necesarios para restaurar el estado
        return redirect(url_for('asignar_reparto', matricula=vehiculo, fecha_asignacion=str(fecha_asignacion)))
