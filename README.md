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
