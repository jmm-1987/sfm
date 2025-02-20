from datetime import datetime

from flask import render_template, request, redirect, url_for
import db
from db import session
from models import Expedicion


def ruta_editar_expedicion(app):
    @app.route('/editar_expedicion/<int:id>', methods=['GET', 'POST'])
    def editar_expedicion(id):
        expedicion = db.session.query(Expedicion).filter_by(id=id).first()

        if request.method == 'POST':
            # Actualizar los campos de la expedición
            fecha_str = request.form['fecha']
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            expedicion.fecha = fecha_obj
            expedicion.numero = request.form['expedicion']
            expedicion.cliente = request.form['cliente']
            expedicion.agencia_origen = request.form['agencia_origen']
            expedicion.agencia_destino = request.form['agencia_destino']
            expedicion.remitente = request.form['remitente']
            expedicion.dir_remitente = request.form['dir_remitente']
            expedicion.destinatario = request.form['destinatario']
            expedicion.dir_destinatario = request.form['dir_destinatario']
            expedicion.bultos = request.form['bultos']
            expedicion.kg = request.form['kg']
            expedicion.reembolso = request.form['reembolso']
            expedicion.estado = request.form['estado']
            expedicion.ingreso_distribucion = request.form['ingreso_distribucion']

            db.session.commit()
            return redirect(url_for('repartos'))

        expediciones = db.session.query(Expedicion).all()

        return render_template('repartos.html', expediciones=expediciones, expedidion=expedicion)