from datetime import datetime

from flask import render_template, request, redirect, url_for
import db
from db import session
from models import Expedicion


def ruta_asignar_expedicion(app):
    @app.route('/asignar_expedicion', methods=['GET', 'POST'])
    def asignar_expedicion():
        expedicion_form = request.form.get('expedicion')
        vehiculo = request.form.get('vehiculo')
        print(vehiculo)
        expedicion_id = db.session.query(Expedicion).filter_by(expedicion=expedicion_form).first()

        expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id.id).first()

        if request.method == 'POST':
            # Actualizar los campos de la expedición
            fecha_str = request.form['fecha_asignacion']
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            expedicion.fecha_asignacion = fecha_obj
            expedicion.asignada_a = vehiculo
            expedicion.estado = "en reparto"

            db.session.commit()
            return redirect(url_for('repartos'))

        expediciones = db.session.query(Expedicion).all()

        return render_template('repartos.html', expediciones=expediciones, expedidion=expedicion)