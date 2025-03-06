from flask import request, redirect, url_for, render_template
import db
from models import Expedicion
from datetime import datetime

def ruta_desasignar_expedicion(app):
    @app.route('/desasignar_expedicion', methods=['POST'])
    def desasignar_expedicion():
        print("aldo")
        expedicion_form = request.form.get('expedicion') or request.args.get('fecha_asignacion')
        vehiculo = request.form.get('matricula')

        print(expedicion_form,vehiculo)

        expedicion_id = db.session.query(Expedicion).filter_by(expedicion=expedicion_form).first()

        if not expedicion_id:
            return redirect(url_for('asignar_reparto', error='Expedición noOO encontrada'))

        expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id.id).first()

        # Actualizar los campos de la expedición
        fecha_str = request.form['fecha_asignacion']
        fecha_asignacion = datetime.strptime(fecha_str.split()[0], "%Y-%m-%d")
        print(fecha_asignacion)
        fecha_asignacion_limpia = ""

        expedicion.asignada_a = ""
        expedicion.estado = "almacen"
        expedicion.fecha_asignacion = fecha_asignacion_limpia


        db.session.commit()

        expediciones_asignadas = db.session.query(Expedicion).filter(

            Expedicion.asignada_a == vehiculo,
            Expedicion.fecha_asignacion == fecha_asignacion
        ).all()

        if expediciones_asignadas:

            # Redirigir con los parámetros necesarios para restaurar el estado
            return render_template('asignar_reparto.html', matricula=vehiculo, fecha_asignacion=fecha_asignacion)

        else:
            return redirect(url_for('repartos'))
