# contasaurioBot

## Descripción

Bot de Telegram para controlar la recepción de documentos, control de timbrados, gestion de carpetas fisicas, exportacion de datos para la R-90.

## Funciones

- /ayuda
    - Tendrá todas la funciones enlistadas
- /nuevocliente
    - Agrega un nuevo cliente a la BBDD
- /listaclientes
    - Genera una lista
    
### Editar Clientes

- /agregartimbrado
    - N°
    - fecha fin
- /recepciondocumentos
    - obs
    - /retirodocumentos
        - obs
- /colorcarpeta

## Busqueda

- /buscar_ci
    - Recibe un numero de ci, lo busca entre los archivos de RUC descargados de Marangatu y compara con otra busqueda para saber si es contribuyente o no.

## Exportacion - Descargas

- /export
    - Formatea los datos del archivo xls, lo convierte en txt tabulado y exporta en zip para adjuntarlo a la R-90 - Marangatu
- /downloadruc
    - Descarga los zip de RUC actualizados a la fecha, de la pagina de la set para descomprimirlos y dejarlo en txt para tratado de archivo. 
