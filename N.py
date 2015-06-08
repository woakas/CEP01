# -- coding: utf-8 --
import math

def verificar_parametros(tiempo_exposicion, nivel_exposicion, fractil):
	""" Esta función verifica que los parámetros de entrada sean correctos, es decir, que se encuentren en el
		rango aceptado por las demás funciones. Los parámetros de entrada son 
		-> tiempo_exposicion, nivel_exposicion <-

		Retorna un -1 si hay algún error, si no es así llama y ejecuta la siguiente función 
		n(tiempo_exposicion, nivel_exposicion).
	"""
	t_exp = range(1,61,1)
	if nivel_exposicion >= 75 and nivel_exposicion <= 100:
		Lex_8h = nivel_exposicion

	
	Q = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]	

	if tiempo_exposicion not in t_exp:
		print "El tiempo de exposición debe estar entre 1 y 60 años."
		return -1
	elif nivel_exposicion != Lex_8h:
		print "El nivel de exposición debe estar entre 75-100dB."
		return -1
	elif fractil not in Q:
		print "El fráctil debe estar en un rango desde 0.05 hasta 0.95 en pasos de 0.05"
		return -1
	else:
		return 1


def n(tiempo_exposicion, nivel_exposicion, fractil):
	""" Esta Función permite calcular los niveles del desplazamiento del umbral inducido por el ruido (NIPTS)
		Recibe como parámetros de entrada -> tiempo_exposicion, nivel_exposicion <-, el tiempo de exposición 
		se refiere al tiempo en años durante los cuales es expuesto el trabajador, y el nivel de exposición
		es el valor en dB del ruido referido a una jornada laboral de 8h (LEX,8h).

		La función retorna una lista de valores en dB correspondientes a los valores que se muestrán a 
		continuación: [125,250,500,1000,1500,2000,3000,4000,6000,8000], los valores se muestran en el orden
		correspondiente a la lista acá mostrada.
	"""
	verificado = verificar_parametros(tiempo_exposicion, nivel_exposicion, fractil)

	if verificado == -1:
		return

	if 0.05 <= fractil < 0.50:
		return (nq_menor_05(tiempo_exposicion, nivel_exposicion, fractil))
	elif 0.50 < fractil <= 0.95:
		return (nq_mayor_05(tiempo_exposicion, nivel_exposicion, fractil))
	elif fractil == 0.50:
		return ((n0_50(tiempo_exposicion, nivel_exposicion)))


def n0_50(tiempo_exposicion, nivel_exposicion):
	""" Recibe -> tiempo_exposicion, nivel_exposicion <- justo como en la función anterior.

		Retorna la mediana de los valores potenciales del desplazamiento permanente del umbral inducido por
		el ruido (NIPTS), retorna los valores pero no las frecuencias.

		Si el valor del tiempo de exposición es menor a 10 años se retorna una extrapolación de N.
	"""
	# VARIABLES

	t_expo_referencia = 1
	u = [(125, 0), (250, 0), (500, -0.033), (1000, -0.020), (1500, 0), (2000, -0.045), (3000, 0.012), (4000, 0.025), (6000, 0.019), (8000, 0)]
	v = [(125, 0), (250, 0), (500, 0.110), (1000, 0.070), (1500, 0), (2000, 0.066), (3000, 0.037), (4000, 0.025), (6000, 0.024), (8000, 0)]
	L0= [(125, 0), (250, 0), (500, 93), (1000, 89), (1500, 0), (2000, 80), (3000, 77), (4000, 75), (6000, 77), (8000, 0)]
	
	if not type(nivel_exposicion) == list:
		nivel_exposicion = [nivel_exposicion]*10
		for i,val in enumerate(L0):
			if nivel_exposicion[i] < val[1]:
				nivel_exposicion[i] = val[1]

	if tiempo_exposicion >= 10:
		j = 0
		N0_50 = []
		while j < len(u):

			respuesta = (u[j][1] + v[j][1] * math.log10(tiempo_exposicion/t_expo_referencia))*(nivel_exposicion[j] - L0[j][1])**2
			N0_50.append(respuesta)
			j += 1
		return N0_50

	elif tiempo_exposicion < 10:
		i = 0
		N0_50 = []
		while i < len(u):
			respuesta = ((math.log10(tiempo_exposicion + 1))/(math.log10(11))) * ((u[i][1] + v[i][1] * math.log10(10))*(nivel_exposicion[i] - L0[i][1])**2)
			N0_50.append(respuesta)
			i += 1
		return N0_50


def valor_k(fractil):
	""" Esta función recibe como parámetro de entrada el valor del fráctil -> fractil <-, que es un valor que puede estar desde
		0.05 hasta 0.95 en pasos de 0.05.

		Retorna el valor correspondiente al mismo índice pero de la lista k, el cual corresponde al valor de k para 
		dicho fráctil
	"""
	Q = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
	k = [1.645, 1.282, 1.036, 0.842, 0.675, 0.524, 0.385, 0.253, 0.126, 0, 0.126, 0.253, 0.385, 0.524, 0.675, 0.842, 1.036, 1.282, 1.645]
	
	if fractil in Q:
		indice = Q.index(fractil)
		return k[indice]


def nq_menor_05(tiempo_exposicion, nivel_exposicion, fractil):
	""" Esta función recibe -> tiempo_exposicion, nivel_exposicion, fractil <- como parámetros de entrada

		Retorna una lista de valores de N cuando el fráctil está por debajo de 0.5, solo retorna la lista de valores.
		pero no de frecuencias.
	"""

	# VARIABLES
	Xu = [(125, 0), (250, 0), (500, 0.044), (1000, 0.022), (1500, 0), (2000, 0.031), (3000, 0.007), (4000, 0.005), (6000, 0.013), (8000, 0)]
	Yu = [(125, 0), (250, 0), (500, 0.016), (1000, 0.016), (1500, 0), (2000, -0.002), (3000, 0.016), (4000, 0.009), (6000, 0.008), (8000, 0)]
	L0 = [(125, 0), (250, 0), (500, 93), (1000, 89), (1500, 0), (2000, 80), (3000, 77), (4000, 75), (6000, 77), (8000, 0)]

	if not type(nivel_exposicion) == list:
		nivel_exposicion = [nivel_exposicion]*10
		for m,val in enumerate(L0):
			if nivel_exposicion[m] < val[1]:
				nivel_exposicion[m] = val[1]


	# Calculando du
	# du = [Xu +Yu lg(tiempo_exposicion/1)] * (nivel_exposicion - L0)**2
	i = 0
	du = []
	while i < len(Xu):
		resultado = (Xu[i][1] + Yu[i][1] * math.log10(tiempo_exposicion/1)) * (nivel_exposicion[i] - L0[i][1])**2
		du.append(resultado)
		i += 1
	# Diferencia de el EXCEL y la NORMA, en el EXCEL en ves de tiempo_exposicion toman la edad.
	# Calculando NQ
	# NQ = n0_50(tiempo_exposicion, nivel_exposicion) + k * du
	j = 0
	NQ = []
	N0_50 = n0_50(tiempo_exposicion, nivel_exposicion)
	while j < len(du):
		respuesta = N0_50[j] + (valor_k(fractil) * du[j])
		# respuesta = round(respuesta,0)
		NQ.append(respuesta)
		j+=1
	return NQ


def nq_mayor_05(tiempo_exposicion, nivel_exposicion, fractil):
	""" Esta función recibe -> tiempo_exposicion, nivel_exposicion, fractil <- como parámetros de entrada

		Retorna una lista de valores de N cuando el fráctil está por encima de 0.5, solo retorna la lista de valores.
		pero no de frecuencias.
	"""
	# VARIABLES
	X1 = [(125, 0), (250, 0), (500, 0.033), (1000, 0.020), (1500, 0), (2000, 0.016), (3000, 0.029), (4000, 0.016), (6000, 0.028), (8000, 0)]
	Y1 = [(125, 0), (250, 0), (500, 0.002), (1000, 0.000), (1500, 0), (2000, 0.000), (3000, -0.010), (4000, -0.002), (6000, -0.007), (8000, 0)]
	L0= [(125, 0), (250, 0), (500, 93), (1000, 89), (1500, 0), (2000, 80), (3000, 77), (4000, 75), (6000, 77), (8000, 0)]

	if not type(nivel_exposicion) == list:
		nivel_exposicion = [nivel_exposicion]*10
		for m,val in enumerate(L0):
			if nivel_exposicion[m] < val[1]:
				nivel_exposicion[m] = val[1]

	# Calculando d1
	# d1 = [X1 +Y1 lg(tiempo_exposicion/1)] * (nivel_exposicion - L0)**2
	i = 0
	d1 = []
	while i < len(X1):
		resultado = (X1[i][1] + Y1[i][1] * math.log10(tiempo_exposicion/1)) * (nivel_exposicion[i] - L0[i][1])**2
		d1.append(resultado)
		i+=1

	# Calculando NQ
	# NQ = n0_50(tiempo_exposicion, nivel_exposicion) - k * d1
	j = 0
	NQ = []
	while j < len(d1):
		# import pdb
		# pdb.set_trace()
		respuesta = n0_50(tiempo_exposicion, nivel_exposicion)[j] - valor_k(fractil) * d1[j]
		# respuesta = round(respuesta,0)
		NQ.append(respuesta)
		j+=1
	return NQ
	



# print n(10,85,0.9)
# print n(10,85,0.5)
# print n(10,85,0.1)
# print "--------------------------------------------------------------------------------------"
# print n(30,90,0.9)
# print n(30,90,0.5)
# print n(30,90,0.1)
# print n(30, 90, 0.9)
# print n(60, 100, 0.05)
