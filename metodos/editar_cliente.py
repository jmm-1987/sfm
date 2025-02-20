from flask import Flask, render_template, request, redirect, url_for, flash
from db import session
from models import Cliente

def ruta_editar_cliente(app):
    @app.route('/editar_cliente/<string:alias>', methods=['GET', 'POST'])
    def editar_cliente(alias):
        cliente = session.query(Cliente).filter_by(alias=alias).first()

        if not cliente:
            flash("Cliente no encontrado", "error")
            return redirect(url_for('clientes'))

        if request.method == 'POST':
            # Obtener datos del formulario y actualizar

            cliente.email = request.form.get('email')
            cliente.telefono = request.form.get('telefono')
            cliente.notas = request.form.get('notas')
            cliente.direccion = request.form.get('direccion')  # En HTML es "direccion"
            cliente.poblacion = request.form.get('poblacion')
            cliente.codigo_postal = request.form.get('codigo_postal')
            cliente.provincia = request.form.get('provincia')
            cliente.pais = request.form.get('pais')
            cliente.tarifa = request.form.get('tarifa')
            cliente.activo = 'activo' in request.form

            # Guardar cambios
            session.commit()
            flash("Cliente actualizado correctamente", "success")
            return redirect(url_for('clientes'))

        # Renderizar la vista con los datos del cliente
        return render_template("modal_editar_cliente.html", cliente=cliente)
