from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import Image
import json

app = Flask(__name__)

def route_exportar_pdf_facturacion(app):
    @app.route('/exportar_pdf_facturacion', methods=['POST'])
    def exportar_pdf_facturacion():
        try:
            datos = request.json.get('data', [])

            if not datos:
                return jsonify({'error': 'No hay datos para exportar'}), 400

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
            width, height = landscape(A4)

            # Obtener cliente (usamos el de la primera fila)
            cliente = datos[0].get("cliente", "Cliente Desconocido")

            # Logo
            logo_path = "static/img/logosfm.jpg"  # Asegúrate de que el logo esté en esta ruta
            pdf.drawImage(logo_path, 30, height - 60, width=100, height=50, preserveAspectRatio=True)

            # Título
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(150, height - 40, f"Informe de Expediciones - Cliente: {cliente}")

            # Dibujar la tabla
            pdf.setFont("Helvetica", 10)
            x_start, y_start = 30, height - 80
            row_height = 20
            col_widths = [50, 70, 80, 80, 80, 80, 40, 40, 50, 50, 70, 70]

            # Encabezados de la tabla
            headers = [
                "ID", "Fecha", "Expedición", "Agencia", "Remitente", "Destinatario",
                "Bultos", "Kg", "Volumen", "Kg Conv", "Distribución", "Cargo"
            ]

            x_pos = x_start
            for i, header in enumerate(headers):
                pdf.drawString(x_pos, y_start, header)
                x_pos += col_widths[i]

            # Dibujar filas de datos
            y_pos = y_start - row_height
            total_expediciones = 0
            total_kg = 0
            total_distribucion = 0
            total_cargos = 0

            for item in datos:
                x_pos = x_start
                total_expediciones += 1
                total_kg += float(item.get("kg", 0))
                total_distribucion += float(item.get("ingreso_distribucion", 0))
                total_cargos += float(item.get("ingreso_cargo_adicional", 0))

                for i, key in enumerate(["id", "fecha", "expedicion", "agencia", "remitente", "destinatario",
                                         "bultos", "kg", "volumen", "kg_conv", "ingreso_distribucion", "ingreso_cargo_adicional"]):
                    pdf.drawString(x_pos, y_pos, str(item.get(key, "")))
                    x_pos += col_widths[i]
                y_pos -= row_height

                if y_pos < 40:  # Salto de página si no hay espacio
                    pdf.showPage()
                    y_pos = height - 80

            # Agregar sumatorio
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(30, y_pos - 30, f"Total Expediciones: {total_expediciones}")
            pdf.drawString(200, y_pos - 30, f"Total Kg: {total_kg:.2f}")
            pdf.drawString(350, y_pos - 30, f"Total Distribución: {total_distribucion:.2f} €")
            pdf.drawString(550, y_pos - 30, f"Total Cargos: {total_cargos:.2f} €")

            pdf.save()
            buffer.seek(0)

            return send_file(buffer, as_attachment=True, download_name="expediciones.pdf", mimetype="application/pdf")

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
