from flask import send_file, abort
from io import BytesIO
import paramiko

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