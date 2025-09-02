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
En la carpeta Datos/HySEA/GrdNetCDF deben colocarse las grillas con la estructura de nombre:
```
grilla_NetCDF_n.grd
```
donde n corresponde al número de cada input.

En la carpeta Datos/HySEA/ParametersTXT deben ubicarse los archivos de condiciones iniciales con la estructura de nombre:
```
data_parameters_n.txt
```
### 5. Transformar los inputs de HySEA a EasyWave
Ejecutar el notebook Input_transformer.ipynb.

Al correrlo, se transformarán automáticamente todos los inputs de HySEA en archivos compatibles con EasyWave, los cuales quedarán almacenados en la carpeta:
```
Datos/EasyWave
```
### 6. Ejecutar el modelo
Con los inputs ya transformados, correr el notebook Main.ipynb.

Este se encargará de ejecutar el modelo de forma automática para cada input disponible en la carpeta correspondiente, generando:

- Archivos .ssh en Datos/EasyWave/Outputs
- Imágenes de resultados (alturas y propagación) en la carpeta Resultados

# Estructura de Carpetas

```plaintext
Memoria-de-Titulo-de-Italo/
│
├── Datos/                     
│   ├── EasyWave/              
│   │   ├── GrdASCII/          
│   │   │   ├── salida_ascii1.grd
│   │   │   ├── salida_ascii2.grd
│   │   ├── Outputs/           
│   │   ├── ParametersFLT/     
│   │   │   ├── data_parameters_1.flt
│   │   │   ├── data_parameters_2.flt
│   │
│   ├── HySEA/                 
│   │   ├── GrdNetCDF/         
│   │   │   └── grilla_NetCDF_1.grd
│   │   │   ├── grilla_NetCDF_2.grd
│   │   ├── ParametersTXT/     
│   │   |   └── data_parameters_1.txt
│   │   |   └── data_parameters_2.txt
│
├── EasyWave_Model/            
│   └── easywave/
│       ├── bin/
│       ├── tools/
│       └── examples/
│
├── Resultados/                
│
├── Input_transformer.ipynb    # Notebook para transformar inputs de HySEA a EasyWave
├── Main.ipynb                 # Notebook para ejecutar el modelo
└── .gitignore                 
