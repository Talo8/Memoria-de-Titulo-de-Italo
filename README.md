# Guía de Ejecución del Proyecto

## Pasos

### 1. Acceder al WSL
Ejecutar en la terminal el comando:
```
cd Memoria-de-Titulo-de-Italo
```
para ingresar a la carpeta principal del proyecto.

### 2. Configurar la variable de entorno
Editar el archivo de configuración de WSL con:
```
nano ~/.bashrc
```
y añadir la siguiente línea:
```
export PATH=$PATH:/EasyWave_Model/easywave/bin
```
Esto asegura que el modelo EasyWave se ejecute correctamente al estar en el PATH del sistema.
### 3. Abrir Visual Studio Code desde WSL
Desde la misma terminal de WSL, ejecutar:
```
code .
```
para abrir el proyecto en Visual Studio Code.
### 4. Ingresar archivos de entrada de HySEA
En la carpeta Datos/HySEA/GrdNetCDF deben colocarse la grilla, utilizando la siguiente estructura de nombre:
```
grilla_NetCDF.grd
```

En la carpeta Datos/HySEA/simulaciones-tsunami-hysea/mw_n/XXXX/ deben ubicarse los archivos de condiciones iniciales, con la siguiente convención de nombres:
```
XXXX.txt
```
Donde n corresponde al número de la magnitud de la simulación y XXXX corresponde al identificador de la simluación

### 5. Transformar los inputs de HySEA a EasyWave
Ejecutar el notebook Input_transformer.ipynb.

Al correrlo, se transformarán automáticamente todos los inputs de HySEA en archivos compatibles con EasyWave, para el caso de los parametros, estos quedarán almacenados en la misma carpeta de origen, en cambio la grilla se almacenará en:
```
Datos/EasyWave/GrdASCII/grilla_ascii.grd
```
### 6. Ejecutar el modelo
Con los inputs ya transformados, correr el notebook Main.ipynb.

Este se encargará de ejecutar el modelo de forma automática para cada input disponible en la carpeta correspondiente, generando:

- Archivos .ssh en Datos/EasyWave/Outputs
- Imágenes de resultados (alturas y propagación) y un archivo netCDF ubicados en las carpetas de cada simulación 

# Estructura de Carpetas

```plaintext
Memoria-de-Titulo-de-Italo/
│
├── Datos/                     
│   ├── EasyWave/              
│   │   ├── GrdASCII/          
│   │   │   ├── grilla_ascii.grd
│   │   ├── Outputs/           
│   │
│   ├── HySEA/                 
│   │   ├── GrdNetCDF/         
│   │   │   └── grilla_NetCDF.grd
│   │
│   ├── simulaciones-tsunami-hysea/
│   │   ├── mw_8.1/         
│   │   │   │── XXXX/
│   │   │   │   ├── XXXX.flt
│   │   │   │   ├── resultado_easywave.nc
│   │   │
│   │   ├── mw_n/         
│   │   │   │── XXXX/
│   │   │   │   ├── XXXX.flt
│   │   │   │   ├── resultado_easywave.nc
│
│
├── EasyWave_Model/            
│   └── easywave/
│       ├── bin/
│       ├── tools/
│       └── examples/
│           
│
├── Input_transformer.ipynb    # Notebook para transformar inputs de HySEA a EasyWave
├── Main.ipynb                 # Notebook para ejecutar el modelo
└── .gitignore                 
