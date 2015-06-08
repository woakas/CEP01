# -*- coding: utf-8 -*- 
import math
import scipy
import H_prima
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, buttord, lfilter


# datos= H_prima.h_prima(60,"M",40, 100, 0.05)
# print datos

def mapeo_frecuencia(y,x,valor_y):
	""" Recibe: 
		y= máximo valor de la escala de atenuacion y 
		x= máximo valor permitido por el filtro

		Retorna: 
		valor_lista=
		El valor que relaciona las dos escalas. 
		(Que ajusta una escala a la otra)
	"""

	valor_lista = 1.
	if valor_y < 0: # con fines de filtrado se igualan todos los valores menores a 0 al valor mínimo de la escala del filtro.
		valor_lista == 1.
	else:
		m = (y-0.)/(x-1.) # (x-1.)
		b = float(y-m*x)
		valor_lista= (valor_y-b)/m
	# print valor_lista
	return valor_lista


def filtro_por_banda(Fc,Rs): # Calculo Banda de Octava
	# Tercio de octava 	Fi = float(Fc/math.sqrt(1.25992105))         Fs = float(Fi*1.25992105)
	# Ws = np.array([60, 200])/22050.; Wp = np.array([50, 250])/22050.
	# Octava
	Fi = float(Fc/math.sqrt(2.0))
	Fs = float(Fi*2.0)
	ws1= Fi ;ws2= Fs ; wp1= Fi-(Fi*0.1) ; wp2= Fs+(Fs*0.1)
	Ws = np.array([ws1, ws2])/22050. 
	Wp = np.array([wp1, wp2])/22050.
	Rp = 1; #Rs = 2
	n, Wn = buttord(Wp,Ws,Rp,Rs)
	# print n, Wn
	b,a = butter(n, Wn, btype='bandstop')
	# plotear(b,a)
	# mfreqz(b,a)
	# print Fi,Fs
	# print b,a
	# print n, Wn
	return b,a


def aplicar_filtros(coeficientes, audio):

	for coeficiente in coeficientes:
		b,a = coeficiente
		audio = lfilter(b,a,audio).astype('int16')

	return audio


def guardar_audio(audio, archivo_salida, fs = 44100):
	wavfile.write(archivo_salida, fs, audio)


def leer_audio(path_audio):
	return wavfile.read(path_audio)

def disenar_filtros(mapeo_butterworth):

	bandas = [125, 250, 500, 1000, 1500, 2000, 3000, 4000, 6000, 8000]

	coeficientes_filtros = []
	for indice, banda in enumerate(bandas):
		resultado = filtro_por_banda(banda, mapeo_butterworth[indice])
		coeficientes_filtros.append(resultado)
	return coeficientes_filtros



def mapear_a_butter(atenuaciones_hp):

	valores_standard = [(32, 3.4), (31, 3.4), (41, 4.7), (48, 4.5),
		(61, 6.4), (71, 8.3), (94, 12.7), (120, 15.4), (136, 21.6),
		(164, 30.0)
	]

	mapeo_butterworth = []
	for indice, atenuacion  in enumerate(atenuaciones_hp):
		valor_max_atenuacion, valor_max_filtro = valores_standard[indice]
		resultado = mapeo_frecuencia(valor_max_atenuacion, valor_max_filtro, atenuacion)
		mapeo_butterworth.append(resultado)

	return mapeo_butterworth


def filtrar(atenuaciones_hp, path_audio):
	'''
	Los datos son el resultado de aplicar h', arreglo de 10 valores
	sonido es un path a un archivo .wav
	'''
	mapeo_butterworth = mapear_a_butter(atenuaciones_hp)
	coeficientes = disenar_filtros(mapeo_butterworth)
	fs, audio = leer_audio(path_audio)
	audio_filtrado = aplicar_filtros(coeficientes, audio)
	guardar_audio(audio_filtrado, 'audios/audio_filtrado/filtrado_butter_tercio.wav', fs = 44100)

# filtrar(datos, 'audios/03_Barridos_Frecuencia/barrido_Lineal_20Hz-20kHz.wav')