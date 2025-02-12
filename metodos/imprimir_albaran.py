from flask import send_file
from metodos.generar_pdf_albaran import generar_pdf_albaran
def ruta_imprimir_albaran(app):
    @app.route('/imprimir_albaran/<int:expedicion_id>')
    def imprimir_albaran(expedicion_id):
        # Llamamos a la función para generar el PDF
        pdf_path = generar_pdf_albaran(expedicion_id)

        # Enviar el archivo PDF generado como respuesta para descargar
        return send_file(pdf_path, as_attachment=True)

