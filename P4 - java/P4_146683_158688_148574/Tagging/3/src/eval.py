#! /usr/bin/env python

import sys
import os
from collections import defaultdict

#Importamos primero el archivo creado seguido del que debemos comparar
input_file1 = sys.argv[1]
ftest1 = open(input_file1, "r", encoding="ISO-8859-1")

input_file2 = sys.argv[2]
fgold1 = open(input_file2, "r", encoding="ISO-8859-1")

input_file3 = sys.argv[3]
ftest2 = open(input_file3, "r", encoding="ISO-8859-1")

input_file4 = sys.argv[4]
fgold2 = open(input_file4, "r", encoding="ISO-8859-1")

#Ficheros de salida con los resultados
output1 = open("output1.txt", "w")
output2 = open("output2.txt", "w")

#Inicializamos contadores para la comparacion
diff = 0
total = 0
# string para mostrar las diferencias
diffstr = "";

#Lectura de una linea para cada iteracion
t = ftest1.readline().split()
g = fgold1.readline().split()

#Comparamos linea a linea ambos ficheros y vemos si las etiquetas son diferentes. En ese caso aumentamos el contador diff
while( t and g ):

	total = total + 1

	if( not((t[0] == g[0]) and (t[1] == g[1]))
	    and( len(t) == len(g) )) :

		diff = diff + 1
		diffstr += "[ %s, %s ] vs [ %s, %s ]\n" %(t[0],t[1],g[0],g[1])

	# Leemos la siguiente linea para la siguiente iteracion
	t = ftest1.readline().split()
	g = fgold1.readline().split()

#Calculamos el porcentaje ([0,1]) de aciertos entre el total de comparaciones
print ("fichero1, aciertos:",round(1 - diff / total, 2),"%","\n\n", file=output1)
print ("diff:\n" + diffstr, file=output1)


# Inicializamos contadores para la comparacion
diff = 0
total = 0
# string para mostrar las diferencias
diffstr = ""

#Lectura de una linea para cada iteracion
t = ftest2.readline().split()
g = fgold2.readline().split()

#Comparamos linea a linea ambos ficheros y vemos si las etiquetas son diferentes. En ese caso aumentamos el contador diff
while( t and g ):

	total = total + 1

	if( not((t[0] == g[0]) and (t[1] == g[1]))
	    and( len(t) == len(g) )) :

		diff = diff + 1
		diffstr += "[ %s, %s ] vs [ %s, %s ]\n" %(t[0],t[1],g[0],g[1])

	# Leemos la siguiente linea para la siguiente iteracion
	t = ftest2.readline().split()
	g = fgold2.readline().split()

#Calculamos el porcentanje ([0,1]) de aciertos entre el total de comparaciones
print ("fichero1, aciertos:",round(1 - diff / total, 2),"%", "\n\n", file=output2)
print ("diff:\n" + diffstr, file=output2)
