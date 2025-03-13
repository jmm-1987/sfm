from flask import request, redirect, url_for, flash
from db import session
from models import Expedicion

def ruta_eliminar_expedicion(app):
    @app.route('/eliminar_expedicion', methods=['POST'])
    def eliminar_expedicion():
        expedicion_id = request.form.get('expedicion_id')
        print (expedicion_id)
        print("algo")

        if not expedicion_id:
            flash("Error: No se proporcionó el código de expedición.", "error")
            return redirect(url_for('repartos'))

        # Buscar la expedición en la base de datos
        expedicion = session.query(Expedicion).filter_by(id=expedicion_id).first()

        if expedicion:
            # Verificar el estado de la expedición


            # Eliminar la expedición y confirmar cambios
            session.delete(expedicion)
            session.commit()
            flash(f"Expedición {expedicion_id} eliminada con éxito.", "success")
            print(f"Expedición {expedicion_id} eliminada con éxito.")
        else:
            flash(f"Error: Expedición {expedicion_id} no encontrada.", "error")
            print(f"Error: Expedición {expedicion_id} no encontrada.")

        return redirect(url_for('facturacion'))
