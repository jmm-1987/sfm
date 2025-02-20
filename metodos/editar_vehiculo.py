from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from db import session
from models import Vehiculo


def ruta_editar_vehiculo(app):
    @app.route('/editar_vehiculo/<string:matricula>', methods=['POST'])
    def editar_vehiculo(matricula):
        vehiculo = session.query(Vehiculo).filter_by(matricula=matricula).first()

        if not vehiculo:
            flash("Vehículo no encontrado", "error")
            return redirect(url_for('vehiculos'))

        # Obtener los datos del formulario
        vehiculo.capacidad = request.form.get('capacidad')
        vehiculo.chofer_habitual = request.form.get('chofer_habitual')

        # Convertir las fechas (si existen)
        def convertir_fecha(fecha_str):
            return datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else None

        vehiculo.caducidad_itv = convertir_fecha(request.form.get('caducidad_itv'))
        vehiculo.caducidad_seguro = convertir_fecha(request.form.get('caducidad_seguro'))
        vehiculo.caducidad_tacografo = convertir_fecha(request.form.get('caducidad_tacografo'))

        vehiculo.activo = 'activo' in request.form  # Verifica si el checkbox está marcado

        # Guardar cambios en la base de datos
        session.commit()
        flash("Vehículo actualizado correctamente", "success")

        return redirect(url_for('vehiculos'))
