from db import session
from metodos.calcular_ingreso_distribucion import calcular_ingreso_distribucion
from models import Expedicion, Cliente
from flask import request, redirect, url_for, render_template
from datetime import datetime
import db



def ruta_grabar_expedidion(app):
    @app.route('/grabar_expedicion', methods=['POST'])
    def grabar_expedicion():

        # Obtener los datos del formulario
        fecha_str = request.form.get('fecha')  # Formato: 'yyyy-mm-dd'
        # Convertir la cadena a un objeto datetime.date
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        expedicion = request.form.get('expedicion')
        agencia_origen = request.form.get('agencia_origen')
        agencia_destino = request.form.get('agencia_destino')
        cliente = request.form.get('cliente')
        remitente = request.form.get('remitente')
        dir_remitente = request.form.get('dir_remitente')
        cod_postal_remitente = request.form.get('cod_postal_remitente')
        poblacion_remitente = request.form.get('poblacion_remitente')
        provincia_remitente = request.form.get('provincia_remitente')
        pais_remitente = request.form.get('pais_remitente')
        destinatario = request.form.get('destinatario')
        dir_destinatario = request.form.get('dir_destinatario')
        cod_postal_destinatario = request.form.get('cod_postal_destinatario')
        poblacion_destinatario = request.form.get('poblacion_destinatario')
        provincia_destinatario = request.form.get('provincia_destinatario')
        pais_destinatario = request.form.get('pais_destinatario')
        bultos = request.form.get('bultos')
        kg = request.form.get('kg')
        volumen = request.form.get('volumen')
        kg_conv = request.form.get('kg_conv')
        tipo_bulto = request.form.get('tipo_bulto')

        # Valores opcionales con valor predeterminado si no se envían
        reembolso = request.form.get('reembolso', 0.0)
        estado = request.form.get('estado', "almacen")
        ingreso_com_reembolso = request.form.get('ingreso_com_reembolso', 0.0)
        ingreso_cargo_adicional = request.form.get('ingreso_cargo_adicional', 0.0)
        coste_reparto = request.form.get('coste_reparto', 0.0)
        coste_arrastre = request.form.get('coste_arrastre', 0.0)
        coste_removido = request.form.get('coste_removido', 0.0)
        coste_distribucion = request.form.get('coste_distribucion', 0.0)

        reembolso = float(reembolso) if reembolso else 0.0
        volumen = float(volumen) if volumen else 0.0  # Si el valor no es numérico, asigna 0.0

        tarifa = db.session.query(Cliente.tarifa).filter(Cliente.alias == cliente).scalar()

        ingreso_distribucion = calcular_ingreso_distribucion(tarifa,cod_postal_destinatario, bultos, tipo_bulto, kg_conv)
        print (ingreso_distribucion)

        # Crear la instancia de la clase Expedicion con los datos recibidos
        nueva_expedicion = Expedicion(
            fecha=fecha,
            expedicion=expedicion,
            agencia_origen=agencia_origen,
            agencia_destino=agencia_destino,
            cliente=cliente,
            remitente=remitente,
            dir_remitente=dir_remitente,
            cod_postal_remitente=cod_postal_remitente,
            poblacion_remitente=poblacion_remitente,
            provincia_remitente=provincia_remitente,
            pais_remitente=pais_remitente,
            destinatario=destinatario,
            dir_destinatario=dir_destinatario,
            cod_postal_destinatario=cod_postal_destinatario,
            poblacion_destinatario=poblacion_destinatario,
            provincia_destinatario=provincia_destinatario,
            pais_destinatario=pais_destinatario,
            bultos=bultos,
            kg=kg,
            volumen=volumen,
            kg_conv=kg_conv,
            tipo_bulto=tipo_bulto,
            reembolso=reembolso,
            estado=estado,
            ingreso_com_reembolso=ingreso_com_reembolso,
            ingreso_distribucion=ingreso_distribucion,
            ingreso_cargo_adicional=ingreso_cargo_adicional,
            coste_reparto=coste_reparto,
            coste_arrastre=coste_arrastre,
            coste_removido=coste_removido,
            coste_distribucion=coste_distribucion
        )

        # Añadir la expedición a la sesión y hacer commit para guardarla en la base de datos
        session.add(nueva_expedicion)
        session.commit()
        print("Expedición grabada con éxito.")

        #expediciones = db.session.query(Expedicion).all()  # Obtener todas las expediciones
        return redirect(url_for('repartos'))

