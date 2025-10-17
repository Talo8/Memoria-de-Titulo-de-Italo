import os
import glob
import numpy as np
import xarray as xr
import struct
from pathlib import Path
from datetime import timedelta

def leer_grilla_easywave_ascii(grd_file):
    with open(grd_file, 'r') as f:
        assert f.readline().strip() == 'DSAA'
        ncols, nrows = map(int, f.readline().split())
        xmin, xmax = map(float, f.readline().split())
        ymin, ymax = map(float, f.readline().split())
        _ = f.readline()
        z = np.empty((nrows, ncols), dtype=np.float32)
        for r in range(nrows):
            vals = f.readline().split()
            row = np.zeros(ncols, dtype=np.float32)
            for c in range(min(len(vals), ncols)):
                row[c] = float(vals[c])
            z[r, :] = row
    return z, nrows, ncols, xmin, xmax, ymin, ymax


def leer_sshmax_subdom(path):
    path = Path(path)
    with path.open('rb') as f:
        if f.read(4) != b'DSBB':
            raise ValueError(f'{path} no comienza con DSBB')
        hdr = f.read(52)
        nI, nJ, loMin, loMax, laMin, laMax, t0, t1 = struct.unpack('<hh6d', hdr)
        _ = struct.unpack('<2d', f.read(16))
        data = np.fromfile(f, dtype='<f4')
        if data.size < nI*nJ:
            tmp = np.zeros(nI*nJ, dtype=np.float32)
            tmp[:data.size] = data
            data = tmp
        arr = data.reshape((nJ, nI))
    return arr, (nI, nJ), (loMin, loMax, laMin, laMax)


def colocar_subdom_en_full(full_shape, domain_bounds, sub_arr, sub_bounds):
    nrows, ncols = full_shape
    xmin, xmax, ymin, ymax = domain_bounds
    loMin, loMax, laMin, laMax = sub_bounds

    lon_full = np.linspace(xmin, xmax, ncols)
    lat_full = np.linspace(ymin, ymax, nrows)

    i0 = int(np.argmin(np.abs(lon_full - loMin)))
    i1 = int(np.argmin(np.abs(lon_full - loMax))) + 1
    j0 = int(np.argmin(np.abs(lat_full - laMin)))
    j1 = int(np.argmin(np.abs(lat_full - laMax))) + 1

    nJ, nI = sub_arr.shape
    if (j1 - j0) != nJ:
        j1 = j0 + nJ
    if (i1 - i0) != nI:
        i1 = i0 + nI

    full = np.zeros((nrows, ncols), dtype=np.float32)
    full[j0:j1, i0:i1] = sub_arr
    return full, lat_full, lon_full


def generar_netcdf(grd_file, sshmax_file, run_out, nc_file):
    bathy, nrows, ncols, xmin, xmax, ymin, ymax = leer_grilla_easywave_ascii(grd_file)
    sub_arr, (nI, nJ), sub_bounds = leer_sshmax_subdom(sshmax_file)
    max_height_full, lat, lon = colocar_subdom_en_full(
        (nrows, ncols),
        (xmin, xmax, ymin, ymax),
        sub_arr,
        sub_bounds
    )

    eta_list, time_list = [], []
    ssh_files = sorted(Path(run_out).glob("eWave.2D.*.ssh"))

    for f in ssh_files:
        try:
            t = int(f.stem.split(".")[2])
        except Exception:
            continue
        arr, (nI, nJ), sub_bounds_t = leer_sshmax_subdom(f)
        eta_full, _, _ = colocar_subdom_en_full(
            (nrows, ncols),
            (xmin, xmax, ymin, ymax),
            arr,
            sub_bounds_t
        )
        eta_list.append(eta_full)
        time_list.append(t)

    ds_vars = {
        "original_bathy": (["lat", "lon"], bathy),
        "max_height": (["lat", "lon"], max_height_full),
    }

    if eta_list:
        ds_vars["eta"] = (["time", "lat", "lon"], np.stack(eta_list, axis=0))

    ds = xr.Dataset(
        data_vars=ds_vars,
        coords={"lat": lat, "lon": lon, "time": time_list if eta_list else []},
        attrs={"source": "EasyWave outputs"}
    )

    ds.to_netcdf(nc_file)
    print(f"✅ NetCDF creado: {nc_file}")


def generar_netcdf_eta(ssh_file, output_nc):
    print(f"📈 Procesando mareogramas: {ssh_file}")

    with open(ssh_file, "r") as f:
        lineas = [line.strip() for line in f if line.strip()]

    datos_numericos = []
    for line in lineas:
        partes = line.split()
        try:
            float(partes[0])
            datos_numericos.append(line)
        except ValueError:
            continue

    data = np.array([list(map(float, l.split())) for l in datos_numericos], dtype=np.float32)
    tiempo_min = data[:, 0]
    eta_vals = data[:, 1:]
    tiempo_hms = [str(timedelta(seconds=int(t * 60))) for t in tiempo_min]

    ds = xr.Dataset(
        {"eta": (["time", "grid_npoints"], eta_vals)},
        coords={"time": tiempo_hms, "grid_npoints": np.arange(eta_vals.shape[1])},
        attrs={"description": "Mareogramas simulados por EasyWave"}
    )

    ds.to_netcdf(output_nc)
    print(f"✅ Mareogramas NetCDF listos: {output_nc}")

# ================== MAIN ==================
grd_file = r"Datos/EasyWave/GrdASCII/grilla_ascii.grd"
flt_base = r"Datos/simulaciones-tsunami-hysea"
out_folder = r"Datos/EasyWave/Outputs"

flt_files = glob.glob(os.path.join(flt_base, "**", "*.flt"), recursive=True)

for flt_file in flt_files:
    rel_path = os.path.relpath(flt_file, flt_base)
    sim_name = os.path.splitext(rel_path.replace(os.sep, "_"))[0]
    run_out = os.path.join(out_folder, sim_name)
    flt_dir = os.path.dirname(flt_file)

    sshmax_file = os.path.join(run_out, "eWave.2D.sshmax")
    ssh_file = os.path.join(run_out, "eWave.poi.ssh")

    nc_main = os.path.join(flt_dir, "resultado_easywave.nc")
    nc_eta = os.path.join(flt_dir, "resultado_ts_easywave.nc")

    if os.path.exists(sshmax_file):
        generar_netcdf(grd_file, sshmax_file, run_out, nc_main)
    if os.path.exists(ssh_file):
        generar_netcdf_eta(ssh_file, nc_eta)

print("🏁 Todos los NetCDF se generaron correctamente.")
