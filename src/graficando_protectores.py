# -- coding: utf-8 --
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

import H_prt
import H_prima_prt
import datos_protectores

# jrenum protección personal Atenuación Asumida APV
sk_ld_10= [5.0,5.8,10.6,14.7,23.8,0.0,28.8,0.0,32.4,0.0,36.2] # desde 63Hz hasta 8kHz
sk_ld_18= [16.8,20.2,21.4,23.9,26.,0.0,29.7,0.0,34.4,0.0,37.5]
sk_ld_26= [24.6,27.8,26.,29.5,29.9,0.0,32.2,0.0,37.9,0.0,39.] # respuesta mas plana.

# ER 15 tapones para músicos con respuesta plana - APV
er_15= [0.0,15.7,14.6,12.6,13,0.0,12.4,0.0,12.2,0.0,16.8]
er_25= [0.0,22.2,22.,20.,20.4,0.0,20.1,0.0,20.4,0.0,25.1]
# ACS PRO 17
acs_pro_17= [0.0,17.94,17.92,15.95,15.85,0.0,14.73,0.0,17.4,0.0,16.58]

# 3M desechables - APV
tres_m_1100= [2.61,28.1,28.9,32.2,33.1,0.0,35.4,0.0,43.8,0.0,40.]
tres_m_1281= [11.5,14.6,14.7,15.5,17.6,0.0,23.6,0.0,22.6,0.0,28.5]
# 3M con banda - APV
tres_m_1310= [17.6,17.1,17.3,19.3,22.1,0.0,31.6,0.0,36.2,0.0,39.1]
# 3M orejeras - APV
tres_m_1430= [11.4,8.7,10.7,15.5,26.2,0.0,31.8,0.0,39.5,0.0,30.8]
tres_m_1435= [8.1,8.1,14.5,18.6,27.,0.0,25.,0.0,31.3,0.0,29.8]
tres_m_1445= [14.6,17.2,21.8,26.7,31.7,0.0,29.8,0.0,36.,0.0,37.7]
# 3M orejeras para casco - APV
tres_m_1455= [10.8,16.4,20.7,25.1,31.1,0.0,29.9,0.0,35.5,0.0,37.]

# Bilsom orejeras
bilsom_807= [8.1,12.4,21.2,25.,20.4,0.0,23.8,0.0,26.,0.0,28.4]
bilsom_808= [8.9,12.3,19.1,22.3,21.9,0.0,26.6,0.0,26.6,0.0,30.3]

# Elvex SuperSonic™ protectores de ruido impulsivo
hb_650=[15.5,16.6,23.3,31.4,36.4,0.0,32.1,0.0,40.6,0.0,33.7]
hb_5000=[0.0,17.7,23.6,34.8,37.3,0.0,34.1,33.8,40.2,39.,38.3]

# edad= 80
# sexo= 'M'
# fractil = 0.05
# tiempo_exposicion = 60
# nivel_exposicion = 100.

# edad= 60
# sexo= 'M'
# fractil = 0.05
# tiempo_exposicion = 40
# nivel_exposicion = 100.

edad= 19
sexo= 'F'
fractil = 0.95
tiempo_exposicion = 1
nivel_exposicion = 75.



# atenuacion_h_prima= H_prima_prt.h_prima(19,'F',1,75.,0.95)
atenuacion_h_prima= H_prima_prt.h_prima(edad,sexo,tiempo_exposicion,nivel_exposicion,fractil)
atenuacion_protegido= atenuacion_h_prima
# atenuacion_h= H_prt.h(19,'F',0.95)
atenuacion_h= H_prt.h(edad,sexo,fractil)
interpolado_protectores = datos_protectores.interpolando_tres_frec(sk_ld_10)

def grafica_octavas_protectores(atenuacion_h_prima, 
								atenuacion_h, 
								interpolado_protectores,
								atenuacion_protegido
								):

	plt.figure(figsize= (10,6), dpi= 80)
	ancho = 500
	n = 11
	X = [1998-ancho,3996-ancho,5994-ancho,7992-ancho,9990-ancho,11988-ancho,13986-ancho,15984-ancho,17982-ancho,19980-ancho,21978-ancho]
	X1 = [1998,3996,5994,7992,9990,11988,13986,15984,17982,19980,21978]
	X2 = [1998+ancho,3996+ancho,5994+ancho,7992+ancho,9990+ancho,11988+ancho,13986+ancho,15984+ancho,17982+ancho,19980+ancho,21978+ancho]
	Y1 = atenuacion_h
	Y2 = atenuacion_h_prima
	Y3 = interpolado_protectores
	Y4 = atenuacion_protegido
	# print Y4

	# h_prima(edad, sexo, tiempo_exposicion, nivel_exposicion, fractil)
	# h(edad, sexo, fractil)

	# plt.axes([0.055,0.085,0.93,0.89]) ORIGINAL
	plt.axes([0.075,0.085,0.91,0.89])

	# Establece el ancho de las barras según la pendiente de los valores de X.
	# width = []
	# for i in X:
	# 	resp = (i* 0.001072181)*250
	# 	resp = round(resp,0)
	# 	width.append(resp)
	width = ancho

	# Etiqueta los ejes y el título
	ax= plt.gca()
	ax.set_xlabel('Frecuencia (Hz)')
	ax.set_ylabel('Desplazamiento del Umbral (dB)')

	# Establecer los límites de la imagen
	# plt.xlim(min(X)*.75,max(X)*1.25)
	plt.xlim(0.1,23976)
	# ylim(min(Y4)*1.1,max(Y4)*1.1)
	maximo_y3 = int(round(max(Y3)*1.1,0)) # At. EPI
	minimo_y4 = int(round(min(Y1)*1.1,0)) # At. Est. H'
	for i in Y1:
		if i < 0:
			plt.ylim(minimo_y4,maximo_y3*1.1)
			plt.yticks(range(minimo_y4,maximo_y3,5))
		elif 0 <= i <= 86:
			plt.ylim(0,86*0.5)
			plt.yticks(range(0,86,5))
		else:
			plt.ylim(0,165)
			plt.yticks(range(0,166,10))

	# if max(Y3) > max(Y2):
	# 	# print "entro 1"
	# 	plt.ylim(0,max(Y3)*1.1)
	# 	plt.yticks(range(0,int(round(max(Y3),0))+10,2))
	# elif max(Y2) > max(Y3): # Plotea solo la atenuación del protector
	# 	# print "entro 2"
	# 	plt.ylim(0,max(Y2)*1.1)
	# 	plt.yticks(range(0,int(round(max(Y2),0))+1,2))		
	# elif min(Y4) < min(Y3) and max(Y2) < min (Y3):
	# 	# print "entro 3"
	# 	plt.ylim(0,max(Y3)*1.1)
	# 	plt.yticks(range(0,int(round(max(Y3),0))+1,2))

	# las etiquetas en el eje y estan dadas por los valores mínimo y máximo + 5 en pasos de 5
	# yticks(range(int(round(min(Y4),0)),int(round(max(Y4),0))+10,5))
	# yticks(range(int(round(min(Y3),0)),int(round(max(Y3),0))+10,5))

	# Volver el eje x logarítmico
	# plt.xscale('log')
	plt.gca().invert_yaxis() # Invirtiendo el eje Y

	# Ajustar las etiquetas en los ejes x e y.
	plt.xticks([1998,3996,5994,7992,9990,11988,13986,15984,17982,19980,21978], 
	[r'$63$',r'$125$',r'$250$', r'$500$',r'$1000$',r'$1500$',r'$2000$',r'$3000$',r'$4000$',r'$6000$',r'$8000$'])

	verde= (54/255.,169/255.,177/255.)
	rojo= (207/255.,63/255.,67/255.)
	verde_fosforo= (51/255.,1.,0.)
	amarillo= (255/255.,222/255.,79/255.)

	plt.grid(True)
	plt.bar(X1, Y1, width= width, facecolor=verde, edgecolor='white', align='center', label=u'Pérdida por Edad H') 
	plt.bar(X, Y2, width= width, facecolor=rojo, edgecolor='white', align='center', label=u'Pérdida por Ruido H\'')
	plt.plot(X1,Y3, '-s', linewidth=2.,color=verde_fosforo, label=u'Atenuación EPI')
	plt.bar(X2, Y4, width= width, facecolor=amarillo, edgecolor='white', align='center', label=u'Estimación de Perdida con uso de EPI') 
	plt.legend(loc='lower left',prop={'size':12})

	plt.savefig('images/grafica_protectores.png') # Guardando la gráfica como un archivo PNG
	# plt.show()

# grafica_octavas_protectores(atenuacion_h_prima, atenuacion_h, interpolado_protectores, atenuacion_protegido)