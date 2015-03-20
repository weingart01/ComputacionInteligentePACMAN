#! /usr/bin/env python


import sys
import os
from collections import defaultdict

if sys.version_info >= (3,0):
	print("Sorry, requires Python 2.x, not Python 3.x")
	sys.exit(1)

#Importamos el corpus a analizar
input_file = sys.argv[1]
entrada = open(input_file, "r")

#Creamos el fichero de salida "lexic.txt"
output_file = "lexic.txt"
salida = file(output_file, "w")

print ('Lectura del corpus')

#Creamos dos diccionarios auxiliares para crear el lexico
#El diccionario1 contendra cada par diferente de palabras y etiquetas; el diccionario2 cada palabra+etiqueta diferente seguido de sus ocurrencias
dict1 = defaultdict(list)
dict2 = {} 

#Para cada linea del corpus analizamos la palabra y su etiqueta
for l in entrada:
	l = l.split()
	palabra = l[0]
	tag = l[1]

	lista1 = []
	auxString = palabra+tag

	#Si la palabra no se encuentra en el diccionario1, la anadimos junto con su etiqueta en el diccionario1 y anadimos la primera ocurrencia de palabra+etiqueta en el diccionario2
	if (dict1.has_key(palabra) == False):
		dict1[palabra].append(tag)
		dict2[auxString] = 1

    #Si la entrada palabra+etiqueta no se encuentra en el diccionario2, anadimos la palabra junto con su etiqueta en el diccionario1 y anadimos la primera ocurrencia de palabra+etiqueta en el diccionario2 
	elif(dict2.has_key(auxString) == False):
		dict1[palabra].append(tag)
		dict2[auxString] = 1

    #Si la palabra existe en el diccionario1 y palabra+etiqueta existe en el diccionario2
    # aumentamos el numero de ocurrencias de esa palabra con esa etiqueta
	else:
		auxNumber = int (dict2.get(auxString))
		auxNumber += 1
		dict2[auxString] = auxNumber
	print "Otra palabra leida"

#Guardamos toda la informacion de los diccionarios en el fichero de salida "lexic.txt"
for x in dict1.keys():
	listaKeys = dict1.get(x)
	for y in listaKeys:
		auxSS = x+y
		num = dict2.get(auxSS)
		print >> salida, x + ' ' + y + ' ' + str(num)
	print "Otra palabra hecha: " + x

