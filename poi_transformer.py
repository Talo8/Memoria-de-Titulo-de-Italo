import os

def txt_a_poi():
    ruta_entrada = "Datos/HySEA/PuntosPOI.txt"
    ruta_salida = "Datos/EasyWave/puntos.poi"

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_entrada, 'r') as f:
        lineas = f.readlines()

    with open(ruta_salida, 'w') as f_out:
        for i, linea in enumerate(lineas, start=1):
            partes = linea.strip().split()
            if len(partes) < 2:
                continue  
            lon, lat = partes[0], partes[1]
            f_out.write(f"P{i:04d} {float(lon):.10f} {float(lat):.10f}\n")

    print(f"✅ Archivo .poi generado correctamente en: {ruta_salida}")


if __name__ == "__main__":
    txt_a_poi()
