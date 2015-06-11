# -- coding: utf-8 --
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import H
import H_prima

def grafica_octavas(atenuacion_h_prima, atenuacion_h):
	ancho = 350
	n = 10
	X = [1998-ancho,3996-ancho,5994-ancho,7992-ancho,9990-ancho,11988-ancho,13986-ancho,15984-ancho,17982-ancho,19980-ancho]
	X1 = [1998+ancho,3996+ancho,5994+ancho,7992+ancho,9990+ancho,11988+ancho,13986+ancho,15984+ancho,17982+ancho,19980+ancho]
	Y1 = atenuacion_h
	Y2 = atenuacion_h_prima

	# h_prima(edad, sexo, tiempo_exposicion, nivel_exposicion, fractil)
	# h(edad, sexo, fractil)

	plt.figure(figsize= (10,6), dpi= 80)
	plt.axes([0.08,0.085,0.9,0.89])  # ([0.08,0.1,0.9,0.85])  ([borde izq, borde inf, borde der, borde sup])

	# Establece el ancho de las barras según la pendiente de los valores de X.
	# width = []
	# for i in X:
	# 	resp = (i* 0.001072181)*250
	# 	resp = round(resp,0)
	# 	width.append(resp)
	width = ancho*2

	# Etiqueta los ejes y el título
	ax= plt.gca()
	ax.set_xlabel(u'Frecuencia (Hz)')
	ax.set_ylabel(u'Desplazamiento del Umbral (dB)')

	# Establecer los límites de la imagen
	# plt.xlim(min(X)*.75,max(X)*1.25)
	plt.xlim(min(X)*.75,21978)
	# plt.ylim(min(Y2)*1.1,max(Y2)*1.1)
	# plt.ylim(0,164*0.5)
	for i in Y1:
		if i < 0:
			plt.ylim(-15,0*0.5)
			plt.yticks(range(-15,3,3))
		elif 0 <= i <= 86:
			plt.ylim(0,85*0.5)
			plt.yticks(range(0,86,5))
		else:
			plt.ylim(0,165)
			plt.yticks(range(0,166,10))


	# Volver el eje x logarítmico
	# plt.xscale('log')
	plt.gca().invert_yaxis() # Invirtiendo el eje Y
	plt.grid(True)
	# Ajustar las etiquetas en los ejes x e y.
	plt.xticks([1998,3996,5994,7992,9990,11988,13986,15984,17982,19980], 
	[r'$125$',r'$250$', r'$500$',r'$1000$',r'$1500$',r'$2000$',r'$3000$',r'$4000$',r'$6000$',r'$8000$'])

	# las etiquetas en el eje y estan dadas por los valores mínimo y máximo + 5 en pasos de 5
	# plt.yticks(-14,85)
	# plt.yticks(range(int(round(min(Y2),0)),int(round(max(Y2),0))+10,5))
	# plt.yticks(range(int(round(min(Y2),0)),int(round(max(Y1)+5,0)),5))
	
	# colores graficación
	azul= (54/255.,169/255.,177/255.)
	rojo= (207/255.,63/255.,67/255.)

	plt.bar(X, Y2, width= width, facecolor=rojo, edgecolor='white', align='center',label=u'Pérdida por Ruido H\'')
	plt.bar(X1, Y1, width= width, facecolor=azul, edgecolor='white', align='center',label=u'Pérdida por Edad H') 
	plt.legend(loc='lower left',prop={'size':12})
	plt.savefig('images/H_y_Hprima_octavs.png') # Guardando la gráfica como un archivo PNG
	# plt.show()

# edad= 80
# sexo= 'M'
# fractil = 0.05
# tiempo_exposicion = 60
# nivel_exposicion = 100

# edad= 60
# sexo= 'M'
# fractil = 0.05
# tiempo_exposicion = 40
# nivel_exposicion = 100

# edad= 19
# sexo= 'F'
# fractil = 0.95
# tiempo_exposicion = 1
# nivel_exposicion = 75

# grafica_octavas(H_prima.h_prima(edad, sexo, tiempo_exposicion, nivel_exposicion, fractil),H.h(edad,sexo,fractil))