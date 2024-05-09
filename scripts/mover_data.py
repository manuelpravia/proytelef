
archivo_texto = "/opt/airflow/data/archivo.txt"

with open(archivo_texto, 'a') as archivo:
    # Escribe una cadena en una nueva línea en el archivo
    archivo.write('\nMoviendo la data al servidor 3...')
