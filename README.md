# Diagramador de tableros de ajedrez
## Autor: Hiram Ehecatl Lujano Pastrana

Este programa fue hecho con python 3, tambien se necesita de 2 bibliotecas para
funcionar dearpygui y Pillow, para instalarlas solo basta ejecutar

> pip install dearpygui Pillow

el programa se ejecuta de la siguiente forma

> python main.py

Los archivos que obtenemos al guardar el tablero son dos, uno con terminación
.mrq que contiene los caracteres para la fuente de letra Marroquin, y el
segundo con terminación .sv es el archivo que el programa toma al cargar
un tablero, estos archivos se guardan donde se encuentra el archivo main.py, la
imagen tambien se guarda en ese lugar. Si no se agrega un nombre a los archivos,
por defecto se llamaran save.mrq, save.sv y img_save.jpg

Al momento de querer eliminar una flecha, uno debe dar click en el
principio o en el final de la flecha.

Al seleccionar la acción de la barra de controles, se debe dar un click extra
en el tablero justo despues de haber dado click en la acción. Esto es
un problema en la implementación de la biblioteca dearpygui que por el momento,
no se puede evitar.

La opción para leer un archivo PGN se encuentra en el menu Herramientas.
