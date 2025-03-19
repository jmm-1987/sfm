from flask import request, redirect, url_for, flash
import os
import random
import string
from models import Vehiculo, DocumentoVehiculo
import db
import paramiko
from flask import send_file, abort
from io import BytesIO

# Datos del SFTP
SFTP_HOST = "access-5017125124.webspace-host.com"
SFTP_PORT = 22
SFTP_USER = "a632109"
SFTP_PASS = "924-Tx%20.2"  # Reemplaza esto con la contraseña correcta
SFTP_DIR = "/sfm/vehiculos/"  # Ruta donde guardarás los archivos en el servidor

def ruta_subir_documento(app):
    @app.route('/subir_doc_vehiculo', methods=['POST'])
    def subir_doc_vehiculo():
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'jpg', 'png', 'jpeg'}

        def generar_nombre_archivo(matricula, extension):
            sufijo = ''.join(random.choices(string.digits, k=5))
            return f"{matricula}_{sufijo}.{extension}"

        matricula = request.form.get('matricula_doc')
        archivo = request.files.get('documento')

        if not archivo or archivo.filename == '':
            flash('No se seleccionó ningún archivo')
            return redirect(request.referrer)

        if not allowed_file(archivo.filename):
            flash('Extensión de archivo no permitida')
            return redirect(request.referrer)

        vehiculo = db.session.query(Vehiculo).filter_by(matricula=matricula).first()
        if not vehiculo:
            flash('Vehículo no encontrado')
            return redirect(request.referrer)

        extension = archivo.filename.rsplit('.', 1)[1].lower()
        filename = generar_nombre_archivo(matricula, extension)

        # Conexión SFTP
        try:
            transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
            transport.connect(username=SFTP_USER, password=SFTP_PASS)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Crear carpeta si no existe
            try:
                sftp.chdir(SFTP_DIR)
            except IOError:
                sftp.mkdir(SFTP_DIR)
                sftp.chdir(SFTP_DIR)

            remote_path = f"{SFTP_DIR}{filename}"
            file_data = archivo.read()
            sftp.putfo(BytesIO(file_data), remote_path)

            sftp.close()
            transport.close()
        except Exception as e:
            flash(f"Error al subir al SFTP: {str(e)}", "error")
            return redirect(request.referrer)

        # Guardar en base de datos
        nuevo_doc = DocumentoVehiculo(
            matricula=matricula,
            nombre_archivo=filename,
            ruta=remote_path,  # ruta remota
        )
        db.session.add(nuevo_doc)
        db.session.commit()

        flash('Documento subido correctamente al servidor SFTP')
        return redirect(request.referrer)

    @app.route('/eliminar_documento', methods=['POST'])
    def eliminar_documento():
        documento_id = request.form.get('documento_id')

        if not documento_id:
            flash('ID de documento no proporcionado', 'error')
            return redirect(request.referrer)

        documento = db.session.query(DocumentoVehiculo).filter_by(id=documento_id).first()

        if not documento:
            flash('Documento no encontrado', 'error')
            return redirect(request.referrer)

        # Eliminar archivo del servidor SFTP
        try:
            transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
            transport.connect(username=SFTP_USER, password=SFTP_PASS)
            sftp = paramiko.SFTPClient.from_transport(transport)

            try:
                sftp.remove(documento.ruta)
            except FileNotFoundError:
                flash('Archivo no encontrado en el servidor SFTP (ya fue eliminado o ruta incorrecta)', 'warning')

            sftp.close()
            transport.close()
        except Exception as e:
            flash(f'Error al conectar al servidor SFTP para eliminar archivo: {str(e)}', 'error')

        # Eliminar de la base de datos
        db.session.delete(documento)
        db.session.commit()

        flash('Documento eliminado correctamente', 'success')
        return redirect(request.referrer)

    @app.route('/ver_documento/<path:nombre_archivo>')
    def ver_documento(nombre_archivo):
        try:
            transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
            transport.connect(username=SFTP_USER, password=SFTP_PASS)
            sftp = paramiko.SFTPClient.from_transport(transport)

            remote_path = f"{SFTP_DIR}{nombre_archivo}"
            file_data = BytesIO()
            sftp.getfo(remote_path, file_data)
            file_data.seek(0)

            sftp.close()
            transport.close()

            # Tipo de contenido básico (puedes mejorarlo usando mimetypes si quieres)
            extension = nombre_archivo.rsplit('.', 1)[-1].lower()
            mimetypes = {
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png'
            }
            content_type = mimetypes.get(extension, 'application/octet-stream')

            return send_file(file_data, mimetype=content_type, download_name=nombre_archivo)

        except Exception as e:
            print(f"Error al mostrar el documento: {str(e)}")
            abort(404)