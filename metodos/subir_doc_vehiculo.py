from flask import request, redirect, url_for, flash
import os
import random
import string
from models import Vehiculo, DocumentoVehiculo
import db

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

        # Extraer extensión
        extension = archivo.filename.rsplit('.', 1)[1].lower()
        filename = generar_nombre_archivo(matricula, extension)

        ruta_relativa = os.path.join('static/doc_vehiculos', filename)
        ruta_absoluta = os.path.join(app.root_path, ruta_relativa)

        os.makedirs(os.path.dirname(ruta_absoluta), exist_ok=True)
        archivo.save(ruta_absoluta)

        nuevo_doc = DocumentoVehiculo(
            matricula = matricula,
            nombre_archivo=filename,
            ruta = ruta_relativa,
        )
        db.session.add(nuevo_doc)

        db.session.commit()

        flash('Documento subido y asociado correctamente')
        return redirect(request.referrer)

    @app.route('/eliminar_documento', methods=['POST'])
    def eliminar_documento():
        documento_id = request.form.get('documento_id')
        print(documento_id)

        if not documento_id:
            flash('ID de documento no proporcionado', 'error')
            return redirect(request.referrer)

        documento = db.session.query(DocumentoVehiculo).filter_by(id=documento_id).first()
        print(documento)

        if not documento:
            flash('Documento no encontrado', 'error')
            return redirect(request.referrer)

        # Ruta absoluta del archivo en el sistema
        ruta_absoluta = os.path.join(app.root_path, documento.ruta)

        # Eliminar archivo físico si existe
        if os.path.exists(ruta_absoluta):
            try:
                os.remove(ruta_absoluta)
            except Exception as e:
                flash(f'Error al eliminar el archivo físico: {str(e)}', 'error')

        # Eliminar de la base de datos
        db.session.delete(documento)
        db.session.commit()

        flash('Documento eliminado correctamente', 'success')
        return redirect(request.referrer)
