from db import session
from flask import request, jsonify
from models import Cliente
import db

def ruta_obtener_datos_cliente_js(app):


    @app.route('/get_cliente_data')

    def get_cliente_data():
        alias = request.args.get("alias")

        if not alias:
            return jsonify({"error": "No se proporcionó un alias"}), 400

        cliente = db.session.query(Cliente).filter_by(alias=alias).first()

        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404

        return jsonify({
            "remitente": cliente.alias,
            "dir_remitente": cliente.direccion,
            "cod_postal_remitente": str(cliente.codigo_postal).zfill(5),
            "poblacion_remitente": cliente.poblacion,
            "provincia_remitente": cliente.provincia,

        })
