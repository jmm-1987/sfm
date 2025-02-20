from flask import request, render_template
import db
from models import Expedicion

def ruta_consultar_expedicion(app):
    @app.route('/consultar_expedicion', methods=['GET'])
    def consultar_expedicion():
        expedicion_id = request.args.get('id')

        if not expedicion_id:
            return render_template('repartos.html', error="Por favor, ingrese un número de expedición.")

        # Buscar por ID
        expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id).first()

        # Si no se encuentra por ID, buscar por número de expedición
        if not expedicion:
            expedicion = db.session.query(Expedicion).filter_by(expedicion=expedicion_id).first()

        # Si no se encuentra en ambas búsquedas, mostrar error
        if not expedicion:
            return render_template('repartos.html', error="Expedición no encontrada.")

        # Si la expedición se encuentra, mostrar la vista con el modal abierto
        return render_template('repartos.html', expedicion=expedicion, abrir_modal=True)

