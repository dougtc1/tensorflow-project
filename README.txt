# README.txt

Aquí se explica lo que se necesita para ejecutar el código. Instalar tensorflow y demás librerías usadas a través de pip3, con el siguiente comando: 
pip3 install pandas numpy tensorflow

Cabe destacar que la versión de TensorFlow usada es la versión 1.0. en python 3.4

Para ejecutar el código debe tener en la misma carpeta los dataset en formato .csv (dos por cada tipo de modelo, en total 6 .csv) y correr en un terminal:

python3 proyectofinal-<número de modelo> <número de modelo> <iteraciones> <learning rate>

dónde:

<número de modelo>: es un número entre 1, 2 o 3

<iteraciones>: Cantidad de veces que se desea correr el algoritmo 

<learning rate>: es la tasa de apredizaje deseada.

Al finalizar el programa imprimirá en el terminal el tiempo en segundos que tardó en ejecutarse y se crearán dos archivos, uno con los resultados de la evaluación y otro con la predicción realizada con dicho modelo para los pitchers que lanzaron durante la campaña 2016 y cómo se desempeñarán en la temporada
regular de 2017.

NOTA: Al correr el modelo 2 ocurría un error de "Int not iterable", por ello se comentaron las dos líneas de código que lo causaban y devolvían un archivo con las predicciones de la próxima temporada obtenidas con ese modelo

##### ¿Cómo obtener el dataset? #####

1) Descargar la versión .sql desde la página web: http://seanlahman.com/files/database/lahman2016-sql.zip
2) Descomprimir la base de datos.
3) Entrar en mysql y seleccionar lahman2016 con el siguiente comando: use lahman2016
4) Ejecutar el optimizador de búsqueda en la base de datos con: \. indices.sql
5) Ejecutar la consulta para el modelo deseado (modelo 1, 2 o 3)
6) Recuperar el archivo que tiene como lugar de salida por defecto en /var/lib/mysql-files/ (Se necesita permiso de Root)
7) Correr código del modelo deseado como se explica más arriba

De igual forma se adjuntan los csv obtenidos de estos pasos para cada modelo.