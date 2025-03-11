from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import db
from models import Expedicion, Vehiculo


def ruta_exportar_pdf_listado(app):

    @app.route('/exportar_pdf_listado', methods=['POST'])
    def exportar_pdf_listado():
        try:
            # Obtener los datos del formulario enviado con Jinja
            vehiculo_id = request.form.get('vehiculo')
            fecha_asignacion_str = request.form.get('fecha_asignacion')
            chofer = request.form.get('nombre_chofer')

            print(vehiculo_id, fecha_asignacion_str, chofer)

            fecha_asignacion = datetime.strptime(fecha_asignacion_str, "%Y-%m-%d")

            # Obtener datos de la base de datos
            expediciones = db.session.query(Expedicion).filter(
                Expedicion.asignada_a == vehiculo_id,
                Expedicion.fecha_asignacion == fecha_asignacion
            ).all()

            if not expediciones:
                return "No hay expediciones para esta fecha y vehículo.", 400

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
            width, height = landscape(A4)

            # Agregar logotipo
            logo_path = "static/img/logosfm.jpg"
            pdf.drawImage(logo_path, 30, height - 60, width=100, height=50, preserveAspectRatio=True)

            fecha_formateada = fecha_asignacion.strftime('%d/%m/%Y')

            # Título
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(150, height - 40, f"Listado de Reparto - Vehículo: {vehiculo_id}")
            pdf.drawString(150, height - 60, f"Fecha: {fecha_formateada}  |  Chofer: {chofer}")

            # Encabezados de la tabla
            pdf.setFont("Helvetica", 10)
            x_start, y_start = 30, height - 100
            row_height = 20

            # Se agregó espacio para la nueva columna "Población Destinatario"
            col_widths = [60, 80, 100, 100, 100, 100, 50, 50]

            headers = ["Número", "Fecha", "Expedición", "Remitente", "Destinatario", "Población", "Bultos", "Kg"]
            x_pos = x_start
            for i, header in enumerate(headers):
                pdf.drawString(x_pos, y_start, header)
                x_pos += col_widths[i]

            # Dibujar filas de datos
            y_pos = y_start - row_height
            total_expediciones = len(expediciones)
            total_kg = sum(float(exp.kg) for exp in expediciones)

            for exp in expediciones:
                x_pos = x_start
                values = [
                    exp.id, exp.fecha.strftime('%d/%m/%Y'), exp.expedicion,
                    exp.remitente, exp.destinatario, exp.poblacion_destinatario,
                    exp.bultos, exp.kg
                ]
                for i, value in enumerate(values):
                    pdf.drawString(x_pos, y_pos, str(value))
                    x_pos += col_widths[i]
                y_pos -= row_height

                if y_pos < 40:  # Salto de página si no hay espacio
                    pdf.showPage()
                    y_pos = height - 100

            # Agregar sumatorio
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(30, y_pos - 30, f"Total Expediciones: {total_expediciones}")
            pdf.drawString(200, y_pos - 30, f"Total Kg: {total_kg:.2f}")

            pdf.save()
            buffer.seek(0)

            return send_file(buffer, as_attachment=True, download_name="listado_reparto.pdf", mimetype="application/pdf")

        except Exception as e:
            return f"Error al generar PDF: {str(e)}", 500

    if __name__ == '__main__':
        app.run(debug=True)
