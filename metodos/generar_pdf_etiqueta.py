from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, white
from reportlab.lib.units import mm
from models import Expedicion
import db


def generar_pdf_etiqueta(expedicion_id):
    # Ruta del logo (ajusta esta ruta según la ubicación de tu archivo)
    LOGO_PATH = "static/img/logosfm.png"

    # Obtiene los datos de la expedición
    expedicion = db.session.query(Expedicion).filter_by(id=expedicion_id).first()

    if not expedicion:
        return None  # Devuelve None si la expedición no existe

    # Crea el archivo PDF
    output_pdf = f"expedicion_{expedicion_id}.pdf"
    c = canvas.Canvas(output_pdf, pagesize=(100 * mm, 150 * mm))  # Tamaño aproximado de la etiqueta

    # **Agrega el logo en la parte superior izquierda**
    try:
        c.drawImage(LOGO_PATH, 5 * mm, 130 * mm, width=30 * mm, height=15 * mm, mask='auto')
    except:
        print("Error: No se pudo cargar el logo. Verifica la ruta del archivo.")

    # **Texto "SEVILLA" grande en negro sin fondo**
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(black)
    c.drawString(40 * mm, 135 * mm, f"Destino:{expedicion.provincia_destinatario}")  # Ajustado para dejar espacio al logo

    # **Información de la etiqueta**
    c.setFont("Helvetica", 10)
    c.drawString(10 * mm, 125 * mm, f"N. EXP: {expedicion.id}")

    # **Datos de bultos, kilos y volumen**
    c.drawString(10 * mm, 115 * mm, f"BULTOS: {expedicion.bultos}")
    c.drawString(40 * mm, 115 * mm, f"KILOS: {expedicion.kg}")
    c.drawString(70 * mm, 115 * mm, f"VOLUMEN: {expedicion.kg_conv}")

    # **Fecha**
    c.drawString(10 * mm, 110 * mm, f"FECHA: {expedicion.fecha}")

    # **Línea divisoria**
    c.line(10 * mm, 108 * mm, 90 * mm, 108 * mm)

    # **Origen y destinatario**
    c.drawString(10 * mm, 100 * mm, f"ORIGEN: {expedicion.provincia_remitente}")
    c.drawString(10 * mm, 95 * mm, f"REMITENTE: {expedicion.remitente}")
    c.drawString(10 * mm, 90 * mm, f"REFERENCIA: {expedicion.expedicion}")

    c.drawString(10 * mm, 80 * mm, f"CONSIG.: {expedicion.destinatario}")
    c.drawString(10 * mm, 75 * mm, f"DIRECCIÓN: {expedicion.dir_destinatario}")

    # **Código de barras (ejemplo simple)**
    c.setFont("Helvetica", 8)
    c.drawString(10 * mm, 60 * mm, "CÓDIGO DE BARRAS:")
    c.drawString(10 * mm, 55 * mm, f"{expedicion.id}")

    # **Finaliza el PDF**
    c.save()

    return output_pdf  # Devuelve la ruta del PDF generado
