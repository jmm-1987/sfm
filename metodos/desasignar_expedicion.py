from flask import request, redirect, url_for, flash
from models import Expedicion
from db import session

def ruta_desasignar_expedicion(app):
    @app.route('/desasignar_expedicion', methods=['POST'])
    def desasignar_expedicion():

        expedicion_id = request.form.get('expedicion_id')

        if not expedicion_id:
            flash("Error: No se proporcionó el código de expedición.", "error")
            return redirect(url_for('repartos'))

        expedicion = session.query(Expedicion).filter_by(id=expedicion_id).first()

        if expedicion:
            print(f"Expedición encontrada: {expedicion}")  # Depuración

            fecha_asignacion_limpia = None

            expedicion.asignada_a = ""
            expedicion.estado = "almacen"
            expedicion.fecha_asignacion = fecha_asignacion_limpia

            session.commit()
            flash(f"Expedición {expedicion_id} desasignada con éxito.", "success")
            print(f"Expedición {expedicion_id} desasignada con éxito.")
        else:
            flash(f"Error: Expedición {expedicion_id} no encontrada.", "error")
            print(f"Error: Expedición {expedicion_id} no encontrada.")

        return redirect(url_for('repartos'))