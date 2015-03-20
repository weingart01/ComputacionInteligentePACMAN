#! /usr/bin/env python


import sys
import os
from collections import defaultdict

#Importamos los archivos a etiquetar
input_file1 = sys.argv[1]
entrada1 = open(input_file1, "r")

input_file2 = sys.argv[2]
entrada2 = open(input_file2, "r")

#Importamos el archivo del Modelo de Lenguaje
input_file3 = sys.argv[3]
entradacorpus = open(input_file3, "r")

#Creamos los archivos de salida 
output_file1 = "etiquetext1.txt"
salida1 = file(output_file1, "w")

output_file2 = "etiquetext2.txt"
salida2 = file(output_file2, "w")

#Creamos un diccionario donde se almancearan todas las palabras con sus respectivas etiquetas y ocurrencias y una lista que contiene las diferentes etiquetas posibles
dict1 = {}
listaTags = ["Abr", "Adj", "Adv", "Conj", "Data", "Det", "Fin", "Int", "NC", "NP", "Num", "Prep", "Pron", "Punt", "V", "Vaux"]

#A partir del Modelo de Lenguaje llenamos el diccionario con cada par de palabras y etiquetas diferentes y sus ocurrencias
for l in entradacorpus:
	l = l.split()
	auxString = l[0]+l[1]
	dict1[auxString] = l[2] 

#Analizamos el primer test
for l in entrada1:
	l = l.split()
    #Miramos la palabra con cada posible etiqueta, si existe en el diccionario y el numero de ocurrencias es mayor que el que tenemos nos    quedamos con la nueva etiqueta
	etiqueta = "Desc"
	for x in listaTags:
		auxString2 = l[0]+x
		numOcu = 0
		if (dict1.has_key(auxString2)):
			if (numOcu < dict1.get(auxString2)):
				etiqueta = x
				numOcu = dict1.get(auxString2)
    #Vamos guardando los resultados en el fichero de salida
	print >> salida1, l[0] + " " + etiqueta

#Analizamos el segundo test
for l in entrada2:
	l = l.split()
	etiqueta = "Desc"
    #Miramos la palabra con cada posible etiqueta, si existe en el diccionario y el numero de ocurrencias es mayor que el que tenemos nos quedamos con la nueva etiqueta
	for x in listaTags:
		auxString2 = l[0]+x
		numOcu = 0
		if (dict1.has_key(auxString2)):
			if (numOcu < dict1.get(auxString2)):
				etiqueta = x
				numOcu = dict1.get(auxString2)
    #Vamos guardando los resultados en el fichero de salida
	print >> salida2, l[0] + " " + etiqueta

