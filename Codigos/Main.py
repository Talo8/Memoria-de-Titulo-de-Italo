import subprocess
import glob
import os

# Carpeta donde están tus archivos
grd_folder = r"C:\Users\italo\OneDrive - Universidad Técnica Federico Santa María\Titulo\Datos\EasyWave\GrdASCII" 
flt_folder = r"C:\Users\italo\OneDrive - Universidad Técnica Federico Santa María\Titulo\Datos\EasyWave\ParametersFLT"

# Buscar todos los archivos .grd y extraer los números "N"
grd_files = sorted(glob.glob(os.path.join(grd_folder, "salida_ascii*.grd")))

for grd_file in grd_files:
    # Extraer número N del archivo
    basename = os.path.basename(grd_file)             # salida_asciiN.grd
    n = ''.join(filter(str.isdigit, basename))        # Extrae N

    flt_file = os.path.join(flt_folder, f"data_parameters_{n}.flt")

    # Comandos que quieres ejecutar
    print(f"Procesando N={n} ...")
    
    # Ejecutar 'easywave'
    subprocess.run(["easywave"])
    
    # Ejecutar 'datos'
    subprocess.run(["datos"])
    
    # Ejecutar 'easywave' con parámetros
    subprocess.run([
        "easywave",
        "-grid", grd_file,
        "-source", flt_file,
        "-time", "120"
    ])

print("Todos los procesos han finalizado.")
