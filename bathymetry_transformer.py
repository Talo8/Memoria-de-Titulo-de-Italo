import numpy as np
import xarray as xr
import os

def convert_netcdf_to_grd(nc_file, grd_file, x_var='longitude', y_var='latitude', z_var='elevation'):
    try:
        with xr.open_dataset(nc_file) as ds:
            x = ds[x_var].values
            y = ds[y_var].values
            z = ds[z_var].values

            if y[0] > y[-1]:
                y = y[::-1]
                z = np.flipud(z)

            ncols = len(x)
            nrows = len(y)
            xmin, xmax = np.min(x), np.max(x)
            ymin, ymax = np.min(y), np.max(y)
            zmin, zmax = np.min(z), np.max(z)

            os.makedirs(os.path.dirname(grd_file), exist_ok=True)

            with open(grd_file, 'w') as f:
                f.write('DSAA\n')
                f.write(f'{ncols} {nrows}\n')
                f.write(f'{xmin:.8f} {xmax:.8f}\n')
                f.write(f'{ymin:.8f} {ymax:.8f}\n')
                f.write(f'{zmin:.8f} {zmax:.8f}\n')
                for i in range(nrows):
                    row_str = ' '.join(f'{val:.8f}' for val in z[i, :])
                    f.write(row_str + '\n')

        print(f"✅ Convertido: {os.path.basename(nc_file)} → {os.path.basename(grd_file)}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    input_file = r"Datos/HySEA/GrdNetCDF/grilla_NetCDF.grd"
    output_file = r"Datos/EasyWave/GrdASCII/grilla_ascii.grd"
    convert_netcdf_to_grd(input_file, output_file, x_var='x', y_var='y', z_var='z')
