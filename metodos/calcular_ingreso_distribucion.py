import pandas as pd


def calcular_ingreso_distribucion(tarifa, cod_postal_destinatario, bultos, tipo_bulto):
    try:
        # Ruta del archivo Excel
        file_path = "static/tarifas/06PX25_.xlsx"

        # Cargar el archivo Excel
        df = pd.read_excel(file_path, sheet_name="Hoja1", header=None)

        # Obtener los dos primeros dígitos del código postal
        cod_postal_prefijo = str(cod_postal_destinatario)[:2]

        # Buscar la fila donde está el código postal en la primera columna
        fila_cp = df[df.iloc[:, 0].astype(str).str.startswith(cod_postal_prefijo)]

        if fila_cp.empty:
            print(f"❌ No se encontró tarifa para CP {cod_postal_prefijo} en {tarifa}")
            return 0.0

        # Buscar la columna donde está el tipo de bulto en la fila 11
        columnas_bulto = df.iloc[11, :].astype(str)
        indices_tipo_bulto = columnas_bulto[columnas_bulto == tipo_bulto].index.tolist()

        if not indices_tipo_bulto:
            print(f"❌ No se encontró el tipo de bulto '{tipo_bulto}' en {tarifa}")
            return 0.0

        # Identificar la columna adecuada según la cantidad de bultos
        if tipo_bulto in ["HALF", "LIGHT", "FULL", "MEGAFULL"]:
            # Buscar la columna exacta para el número de bultos en la fila 12
            columnas_subtipo = df.iloc[12, indices_tipo_bulto].astype(str)
            index_correcto = None

            for i, col_index in enumerate(indices_tipo_bulto):
                if i + 1 == int(bultos):  # Si coincide con el número de bultos
                    index_correcto = col_index
                    break

            if index_correcto is None:
                index_correcto = indices_tipo_bulto[-1]  # Tomar el último si excede

        else:
            index_correcto = indices_tipo_bulto[0]  # Tomar el primero si no es caso especial

        # Obtener la tarifa base
        tarifa_base = fila_cp.iloc[:, index_correcto].values[0]

        # Calcular el ingreso total
        ingreso_distribucion = round(float(tarifa_base), 2)

        return ingreso_distribucion

    except Exception as e:
        print(f"Error al calcular ingreso_distribucion: {e}")
        return 0.0
