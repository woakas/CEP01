# -- coding: utf-8 --
import H
import N
import math

def h_prima(edad, sexo, tiempo_exposicion, nivel_exposicion, fractil):
	""" Esta función recibe como parámetros de entrada -> edad,sexo,tiempo_exposicion, nivel_exposicion, fractil <-
		para calcular el RIESGO DE PÉRDIDA AUDITIVA OCASIONADO POR EL RUIDO. 

		Retorna una lista de tuplas que tienen la siguiente configuración: (frecuencia, valor)
	"""
	h = H.h(edad,sexo,fractil)
	n = N.n(tiempo_exposicion, nivel_exposicion, fractil)

	return (rechaza_frecuencias(interpolando(calculo_h_prima(h,n))))


def calculo_h_prima(h, n):
	""" Esta función suma cada uno de los valores de N con los valores de H, recibe como parámetros de entrada:
		-> h,n <-, que corresponden a los valores calculados en los archivos H.py y N.py.

		Retorna una lista de valores ordenados de modo que cada valor corresponde a cada uno de estas frecuencias
		ordenadas: [125,250,500,1000,1500,2000,3000,4000,6000,8000].
	"""
	i = 0
	h_pr = []
	while i < len(h):
		if h[i] + n[i] >= 40:
			n[i] = n[i] - h[i] * n[i] / 120
	 	
	 	resultado = h[i]+n[i] - (h[i]*n[i])/120
	 	# import pdb
		# pdb.set_trace()
	 	resultado = round(resultado,2)
	 	h_pr.append(resultado)
	 	i+=1
	return h_pr


def interpolando(hPrima):
	""" Esta función recibe como parámetro de entrada la lista H' -> hPrima <- que es el resultado de la función calculo_h_prima.

		Retorna como resultado una lista con la frecuencia de 1.5 kHz interpolada linealmente entre la frecuencia anterior (1 kHz)
		y la frecuencia posterior (2 kHz).
	"""
	h_p = (hPrima[5]-hPrima[3]) * (((math.log10(1500))-math.log10(1000))/(math.log10(2000)-math.log10(1000))) + hPrima[3]
	hPrima[4] = round(h_p,0)
	return hPrima


def rechaza_frecuencias(hPrima):
	""" Recibe -> hPrima <- la cual es una lista de valores resultado de la función calculo_h_prima(), la función
		cambia los resultados de las frecuencias de 125, 250 y 8000 Hz por ceros (0), para ajustarse a la norma.

		Retorna una lista de valores, sin las bandas de frecuencia, con los valores corregidos en las bandas mencionadas.
	"""
	hPrima[0] = 0
	hPrima[1] = 0
	hPrima[9] = 0
	return hPrima


def agregar_frecuencias(lista):
	""" Esta función recibe como parámetro -> lista <-, que como su nombre lo indíca es una lista que
		tiene 10 valores que se relacionarán con los valores de frecuencia siguientes:
		[125,250,500,1000,1500,2000,3000,4000,6000,8000].

		Retorna una lista de tuplas cuya configuración es de este modo (frecuencia Hz, Valor).
	"""
	F = [125,250,500,1000,1500,2000,3000,4000,6000,8000]
	HQ = [(F[ind], lista[ind]) for ind in range(len(F))]
	return HQ

def redondeo(lista):
	""" Recibe una lista.

		Retorna cada valor redondeado al entero más próximo.
	"""

	i= 0
	L = []
	while i < len(lista):
		lista[i] = round(lista[i],0)
		L.append(lista[i])
		i+= 1
	return L

# print calculo_h_prima(H.h(50,"M",0.9),N.n(30, 90, 0.9))
# print calculo_h_prima(H.h(50,"M",0.5),N.n(30, 90, 0.5))
# print calculo_h_prima(H.h(50,"M",0.1),N.n(30, 90, 0.1))
# print rechaza_frecuencias(interpolando(calculo_h_prima(H.h(50,"M",0.1),N.n(30, 90, 0.1))))
# print h_prima(50,"M",30, 90, 0.1)
# print H.h(50,"M",0.1)
# print redondeo(H.h(50,"M",0.1))
# print h_prima(60,"M",1, 75, 0.05)
# print h_prima(60,"M",30, 75, 0.05)