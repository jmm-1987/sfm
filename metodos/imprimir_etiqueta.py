from flask import send_file
from metodos.generar_pdf_etiqueta import generar_pdf_etiqueta
def ruta_imprimir_etiqueta(app):
    @app.route('/imprimir_etiqueta/<int:expedicion_id>')
    def imprimir_etiqueta(expedicion_id):
        # Llamamos a la función para generar el PDF
        pdf_path = generar_pdf_etiqueta(expedicion_id)

        # Enviar el archivo PDF generado como respuesta para descargar
        return send_file(pdf_path, as_attachment=True)

