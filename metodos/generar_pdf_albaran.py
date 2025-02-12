from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from models import Expedicion
import db

def generar_pdf_albaran(expedicion_id):
    # Obtiene los datos de la expedición
    expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id).first()

    if not expedicion:
        return None  # Devuelve None si la expedición no existe

    # Crea el archivo PDF
    output_pdf = f"albaran_{expedicion_id}.pdf"
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Altura del cuerpo de cada sección
    cuerpo_altura = 90 * mm
    for i in range(3):
        y_offset = 297 * mm - (i + 1) * cuerpo_altura

        # Inserta el logo
        c.drawImage("static/img/logosfm.png", +5 * mm, y_offset +60 * mm, width=50 * mm, height=30 * mm)

        # Encabezado
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60 * mm, y_offset + 80 * mm, "SFL Logística")  # Desplazado para dejar espacio al logo
        c.setFont("Helvetica", 10)
        c.drawString(60 * mm, y_offset + 75 * mm, "C/Pamplona, 22")
        c.drawString(60 * mm, y_offset + 70 * mm, "06800 MÉRIDA (BADAJOZ)")

        # Fecha y datos básicos
        c.drawString(150 * mm, y_offset + 80 * mm, f"Fecha: {expedicion.fecha}")
        c.drawString(150 * mm, y_offset + 75 * mm, f"Expedición: {expedicion.id}")

        # Línea divisoria
        c.line(20 * mm, y_offset + 60 * mm, 190 * mm, y_offset + 60 * mm)

        # Datos del remitente
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, y_offset + 55 * mm, "Remitente:")
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, y_offset + 50 * mm, f"Nombre: {expedicion.remitente}")
        c.drawString(20 * mm, y_offset + 45 * mm, f"Dirección: {expedicion.dir_remitente}")
        c.drawString(20 * mm, y_offset + 40 * mm, f"Población: {expedicion.poblacion_remitente}")
        c.drawString(20 * mm, y_offset + 35 * mm, f"Teléfono: {expedicion.id}")

        # Datos del destinatario
        c.setFont("Helvetica-Bold", 10)
        c.drawString(110 * mm, y_offset + 55 * mm, "Destinatario:")
        c.setFont("Helvetica", 10)
        c.drawString(110 * mm, y_offset + 50 * mm, f"Nombre: {expedicion.destinatario}")
        c.drawString(110 * mm, y_offset + 45 * mm, f"Dirección: {expedicion.dir_destinatario}")
        c.drawString(110 * mm, y_offset + 40 * mm, f"Población: {expedicion.poblacion_destinatario}")
        c.drawString(110 * mm, y_offset + 35 * mm, f"Teléfono: {expedicion.id}")

        # Observaciones
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, y_offset + 30 * mm, "Observaciones:")
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, y_offset + 25 * mm, "DEVOLVER ALBARÁN FIRMADO")

        # Tabla para bultos, peso, etc.
        data = [["Bultos", "Kilos", "Volumen"],
                [expedicion.bultos, expedicion.kg, expedicion.volumen]]

        table = Table(data, colWidths=[30 * mm, 30 * mm, 30 * mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Dibuja la tabla
        table.wrapOn(c, 100 * mm,y_offset + 20 * mm)
        table.drawOn(c, 100 * mm, y_offset +10 * mm)

        # Firma y sello
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, y_offset + 15 * mm, "Firma/Sello:")
        c.drawString(20 * mm, y_offset + 10 * mm, "DNI:")


    # Finaliza el PDF
    c.save()

    return output_pdf  # Devuelve la ruta del PDF generado
