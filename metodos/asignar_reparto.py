from flask import request, render_template
import db
from models import Expedicion
from datetime import datetime


def ruta_asignar_reparto(app):
    @app.route('/asignar_reparto', methods=['POST', 'GET'])
    def asignar_reparto():
        vehiculo = request.args.get('matricula') or request.form.get('matricula')
        fecha_asignacion_str = request.args.get('fecha_asignacion') or request.form.get('fecha_asignacion')

        try:
            fecha_asignacion = datetime.strptime(fecha_asignacion_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Intentar solo la fecha si el tiempo no está incluido
            fecha_asignacion = datetime.strptime(fecha_asignacion_str, '%Y-%m-%d')


        expediciones_asignadas = db.session.query(Expedicion).filter(

            Expedicion.asignada_a == vehiculo,
            Expedicion.fecha_asignacion == fecha_asignacion
        ).all()


        # Redirigir con los parámetros necesarios para restaurar el estado
        return render_template('asignar_reparto.html', vehiculo=vehiculo, fecha_asignacion=fecha_asignacion.strftime('%Y-%m-%d'),
                               expediciones_asignadas=expediciones_asignadas)
