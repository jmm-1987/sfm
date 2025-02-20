from flask import request, redirect, url_for, flash
import db
from models import Expedicion
from datetime import datetime

def ruta_entregar_expedicion(app):
    @app.route('/entregar_expedicion', methods=['POST'])
    def entregar_expedicion():
        expediciones_form = request.form.getlist('expediciones[]')  # Obtener lista de expediciones marcadas

        print(expediciones_form)

        if not expediciones_form:
            flash("No seleccionaste ninguna expedición.", "warning")
            return redirect(url_for('repartos'))

        # Recorrer y actualizar cada expedición
        for expedicion_id in expediciones_form:
            expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id).first()

            if expedicion:
                # Convertir la fecha recibida en formato correcto
                fecha_str = request.form.get('fecha_entrega', datetime.today().strftime("%Y-%m-%d"))
                fecha_entrega = datetime.strptime(fecha_str, "%Y-%m-%d")

                # Actualizar los campos de la expedición
                expedicion.fecha_entrega = fecha_entrega
                expedicion.estado = "entregado"

        # Guardar cambios en la base de datos
        db.session.commit()
        flash(f"Se marcaron {len(expediciones_form)} expediciones como entregadas.", "success")

        return redirect(url_for('repartos'))  # Redirigir a la vista de repartos
