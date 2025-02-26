from db import session
from models import Expedicion, Cliente
from metodos.calcular_ingreso_distribucion import calcular_ingreso_distribucion

from flask import redirect, url_for, jsonify


def ruta_retasar_ingreso_distribucion(app):

    @app.route('/retasar_ingreso_distribucion/<int:expedicion_id>', methods=['GET'])
    def retasar_ingreso_distribucion(expedicion_id):
        # Obtener la expedición
        expedicion = session.query(Expedicion).filter_by(id=expedicion_id).first()
        if not expedicion:
            return jsonify({"error": "Expedición no encontrada"}), 404

        # Obtener cliente
        cliente = session.query(Cliente).filter_by(alias=expedicion.cliente).first()
        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404

        # Extraer datos necesarios para calcular el ingreso de distribución
        codigo_postal_destinatario = str(expedicion.cod_postal_destinatario).zfill(5)


        bultos = expedicion.bultos
        tipo_bulto = expedicion.tipo_bulto
        kg_conv = expedicion.kg_conv
        tarifa = cliente.tarifa

        # Calcular nuevo ingreso de distribución
        ingreso_distribucion = calcular_ingreso_distribucion(tarifa, codigo_postal_destinatario, bultos, tipo_bulto, kg_conv)

        print(ingreso_distribucion)
        # Asignar el nuevo valor y guardar cambios en la base de datos
        expedicion.ingreso_distribucion = ingreso_distribucion
        session.commit()  # Guarda los cambios

        return redirect(url_for('facturacion'))
