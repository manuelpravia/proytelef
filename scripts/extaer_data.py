# Abre un archivo de texto en modo escritura ('w')
archivo_texto = "/opt/airflow/dags/scripts/archivo.txt"

with open(archivo_texto, 'w') as archivo:
    # Escribe una cadena en el archivo
    archivo.write('Extrayendo la data de Oracle...! ')

#with open(archivo_texto, 'a') as archivo:
    # Escribe una cadena en una nueva línea en el archivo
#    archivo.write('\nExtaryendo data de Oracle... ')
