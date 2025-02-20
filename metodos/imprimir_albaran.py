from flask import send_file
from metodos.generar_pdf_albaran import generar_pdf_albaran

def ruta_imprimir_albaran(app):
    @app.route('/imprimir_albaran/<int:expedicion_id>')
    def imprimir_albaran(expedicion_id):
        # Llamamos a la función para generar el PDF
        pdf_buffer = generar_pdf_albaran(expedicion_id)

        if pdf_buffer is None:
            return "Expedición no encontrada", 404

        # Enviar el archivo PDF generado como respuesta para descargar
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"albaran_{expedicion_id}.pdf",
            mimetype='application/pdf'
        )
