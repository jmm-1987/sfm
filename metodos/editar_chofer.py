from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from db import session
from models import Chofer


def ruta_editar_chofer(app):
    @app.route('/editar_chofer/<string:alias>', methods=['POST'])
    def editar_chofer(alias):
        chofer = session.query(Chofer).filter_by(alias=alias).first()

        if not chofer:
            flash("Conductor no encontrado", "error")
            return redirect(url_for('repartidores'))

        # Obtener los datos del formulario
        chofer.nombre_completo = request.form.get('nombre_completo')
        chofer.dni = request.form.get('dni')
        chofer.notas = request.form.get('notas')
        chofer.activo = 'activo' in request.form  # Verifica si el checkbox está marcado

        # Guardar cambios en la base de datos
        session.commit()
        flash("Chofer actualizado correctamente", "success")

        return redirect(url_for('repartidores'))
