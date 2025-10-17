import os

def convertir_faults_a_flt(input_txt, output_flt):
    """Función original de Talo para convertir un .txt a .flt (preserva lógica original).
       Ahora suma +360 a la primera columna (longitud) de cada línea de datos.
    """
    with open(input_txt, 'r') as fin, open(output_flt, 'w') as fout:
        next(fin)

        for line in fin:
            valores = line.strip().split()
            if not valores:
                continue

            valores = valores[1:]

            try:
                lon = float(valores[0])
                if lon < 0:       
                    lon += 360.0
                valores[0] = str(lon)
            except Exception as e:
                print(f"⚠️ No pude convertir longitud en línea: '{line.strip()}' ({e})")
                continue
                    

            valores = [f"{float(v):.3f}" for v in valores]

            salida = (
                f"-location {valores[0]} {valores[1]} {valores[2]} "
                f"-size {valores[3]} {valores[4]} "
                f"-strike {valores[5]} "
                f"-dip {valores[6]} "
                f"-rake {valores[7]} "
                f"-slip {valores[8]}"
            )

            fout.write(salida + "\n")

    print(f"✅ Convertido: {os.path.basename(input_txt)} → {os.path.basename(output_flt)}")


if __name__ == "__main__":
    base_folder = r"Datos/simulaciones-tsunami-hysea"

    for root, dirs, files in os.walk(base_folder):
        for fname in files:
            if not fname.lower().endswith(".txt"):
                continue

            stem = os.path.splitext(fname)[0]

            if not stem.isdigit():
                print(f"⏭ Ignorado (no numerado): {os.path.join(root, fname)}")
                continue

            input_path = os.path.join(root, fname)
            output_path = os.path.join(root, f"{stem}.flt")

            try:
                convertir_faults_a_flt(input_path, output_path)
            except Exception as e:
                print(f"⚠️ Error al convertir {input_path}: {e}")
