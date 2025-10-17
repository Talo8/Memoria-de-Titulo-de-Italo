import subprocess
import glob
import os
import shutil
from pathlib import Path

grd_file = r"Datos/EasyWave/GrdASCII/grilla_ascii.grd"
flt_base = r"Datos/simulaciones-tsunami-hysea"
out_folder = r"Datos/EasyWave/Outputs"
poi_file = r"Datos/EasyWave/puntos.poi"

os.makedirs(out_folder, exist_ok=True)

flt_files = glob.glob(os.path.join(flt_base, "**", "*.flt"), recursive=True)

for flt_file in flt_files:
    rel_path = os.path.relpath(flt_file, flt_base)
    sim_name = os.path.splitext(rel_path.replace(os.sep, "_"))[0]

    run_out = os.path.join(out_folder, sim_name)
    os.makedirs(run_out, exist_ok=True)

    print(f"🌊 Ejecutando EasyWave para {sim_name} ...")

    subprocess.run([
        "easywave",
        "-grid", os.path.abspath(grd_file),
        "-source", os.path.abspath(flt_file),
        "-poi", os.path.abspath(poi_file),
        "-poi_report", os.path.abspath(poi_file),
        "-time", "120",
        "-gpu"                                       #SE AÑADE PARA QUE CORRA CON LA GPU
    ], cwd=run_out)


    print(f"✅ Simulación {sim_name} finalizada")

print("🏁 Todas las simulaciones EasyWave se ejecutaron correctamente.")
