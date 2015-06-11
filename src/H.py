# -- coding: utf-8 --
def verificar_parametros(edad, sexo, fractil):
	""" Esta función tiene como parámetros de entrada -> edad, sexo, fractil <- con el ánimo de verificar los datos de entrada

		Si no se cumple con lo especificado imprime un mensaje de error y retorna un -1. 
	"""
	Q = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]	

	if edad < 19:
		print "La edad debe estar entre 19 y 80 años."
		return -1
	elif edad > 80:
		print "La edad debe estar entre 19 y 80 años."
		return -1		
	elif sexo not in ["M","F","m","f"]:
		print "El sexo debe ser Masculino (M) o Femenino (F)"
		return -1
	elif fractil not in Q:
		print "El fráctil debe estar en un rango desde 0.05 hasta 0.95 en pasos de 0.05"
		return -1
	else:
		return 1


def h(edad, sexo, fractil):
	""" Funcion h (H: Es el nivel umbral de audición, en dB asociado con la edad también conocido como HTLA.)
		Como parámetros de entrada recibe -> (edad, sexo, fractil) Edad (Y): desde los 19 a los 60 años, 
		Sexo: Masculino o Femenino, Fráctil (Q): Posición entre 0.05 hasta 0.95 en un paso de 0.05.


		Retorna una lista de valores correspondientes a los valores de frecuencia que se muestran aquí:
		[125,250,500,1000,1500,2000,3000,4000,6000,8000]. Los valores se muestran en el mismo orden de la 
		lista anterior y describe las bandas en tercio de octava excluyendo las bandas de 63Hz y 16kHz, 
		pero agregando	las bandas de 1.5kHz, 3kHz y 6kHz, según la norma. 
		"""
	verificado = verificar_parametros(edad,sexo,fractil)

	if verificado == -1:
		return

	if 0.05 <= fractil < 0.50:
		return ((hq_menor_a_0_50(edad,sexo,fractil)))
	elif 0.50 < fractil <= 0.95:
		return ((hq_mayor_a_0_50(edad,sexo,fractil)))
	elif fractil == 0.50:
		return ((h0_50(edad,sexo)))


def h0_50(edad, sexo):
	""" Esta función halla el H para el fráctil de 0.50, como parámetros de entrada recibe -> edad, sexo <-

		Retorna una lista llamada H_05 que contiene los valores de H0.50 pero no las frecuencias.
	"""	
	# VARIABLES
	H05_18 = 0 ## H05_18 es el valor de la mediana del umbral para personas otológicamente normales, del 
	## mismo sexo y 18 años, a efectos prácticos, se toma como cero. ##

	# Tabla de valores de a
	aM = [(125, 0.003), (250, 0.003), (500, 0.0035), (1000, 0.004), (1500, 0.0055),
		 (2000, 0.007), (3000, 0.0115), (4000, 0.016), (6000, 0.018), (8000, 0.022)]

	aF = [(125, 0.003),	(250, 0.003), (500, 0.0035), (1000, 0.004), (1500, 0.005),
		 (2000, 0.006), (3000, 0.0075), (4000, 0.009), (6000, 0.012), (8000, 0.015)]

	if sexo == "M":
		a = aM
	elif sexo == "F":
		a = aF

	# Resolviendo la ecuación de Q = 0.5 ------------------------------------------------------------
	# fractil == 0.50:
	#H05 = a*(edad - 18)**2 + H05_18 
	H05 = []
	i = 0
	while i < len(a):
		producto = a[i][1]*(edad - 18)**2 + H05_18
		producto = round(producto,2) # este redondeo es el que se usará en futuros cálculos
		H05.append(producto)
		i +=1
	return H05 # Esta lista solo muestra los valores pero no las frecuencias.


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


def hq_menor_a_0_50(edad, sexo, fractil):
	""" Esta función halla el H para fráctiles menores a 0.50, como párametros de entrada recibe -> edad, sexo, fractil <-

		Retorna una lista llamada HQ que contiene los valores de HQ, pero no las frecuencias.
	"""
	
	# Valores de bu para Masculino y Femenino
	buM= [(125, 7.23), (250, 6.67), (500, 6.12), (1000, 6.12), (1500, 6.67),
		 (2000, 7.23), (3000, 7.78), (4000, 8.34), (6000, 9.45), (8000, 10.56)]

	buF= [(125, 6.67), (250, 6.12), (500, 6.12), (1000, 6.12), (1500, 6.67),
		 (2000, 6.67), (3000, 7.23), (4000, 7.78), (6000, 8.9), (8000, 10.56)]

	if sexo == "M":
		bu = buM
	elif sexo == "F":
		bu = buF

	# Resolviendo para Q menor a 0.5 --------------------------------------------------------
	# Su = bu + 0.445*H50
	Su = []
	i = 0
	while i < len(bu):
		respuesta = bu[i][1] + 0.445*h0_50(edad,sexo)[i]
		Su.append(respuesta)
		i +=1
	#print Su # Esta lista muestra solamente los valores, pero no las frecuencias.
	
	# Hfractil = H05 + k*Su
	HQ = []
	j = 0
	while j < len(Su):
		Hq = h0_50(edad,sexo)[j] + valor_k(fractil)*Su[j]
		HQ.append(Hq)
		j+=1
	return HQ


def hq_mayor_a_0_50(edad, sexo, fractil):
	""" Esta Función halla el H para fráctiles mayores a 0.50, como párametros de entrada recibe -> edad, sexo, fractil <-

		Retorna una lista llamada HQ que contiene los valores de HQ, pero no las frecuencias.
	"""
	# Valores de b1 para Masculino y Femenino
	b1M= [(125, 5.78), (250, 5.34), (500, 4.89), (1000, 4.89), (1500, 5.34),
		 (2000, 5.78), (3000, 6.23), (4000, 6.67), (6000, 7.56), (8000, 8.45)]

	b1F= [(125, 5.34), (250, 4.89), (500, 4.89), (1000, 4.89), (1500, 5.34),
		 (2000, 5.34), (3000, 5.78), (4000, 6.23), (6000, 7.12), (8000, 8.45)]
	
	if sexo == "M":
		b1 = b1M
	elif sexo == "F":
		b1 = b1F

	# Resolviendo para Q mayor a 0.5 --------------------------------------------------------
	# S1 = b1 + 0.356*H50
	S1 = []
	i = 0
	while i < len(b1):
		respuesta = b1[i][1] + 0.356*h0_50(edad,sexo)[i]
		S1.append(respuesta)
		i +=1
	#print S1 # Esta lista muestra solamente los valores, pero no las frecuencias.
	
	# Hfractil = H05 - k*S1
	HQ = []
	j = 0
	while j < len(S1):
		Hq = h0_50(edad,sexo)[j] - valor_k(fractil)*S1[j]
		HQ.append(Hq)
		j+=1
	return HQ

# print h(28,"M",0.3)
# print h(28,"F",0.8)
# print h(48,"F",0.9)
# print h(80,"M", 0.05)
# print h(80,"M", 0.05)
