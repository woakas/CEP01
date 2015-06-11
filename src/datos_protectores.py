# -- coding: utf-8 --
import math

# Interpolar frecuencias de 1.5kHz, 3kHz y 6kHz
def interpolando_una_frec(lista,frec_a_interpolar):
	""" Esta función recibe como parámetros de entrada: 
		lista= una lista de 11 elementos, 
		frec_a_interpolar= la frecuencia a interpolar

		Retorna como resultado una lista con el valor perteneciente a 
		la frecuencia y  interpolada linealmente entre la frecuencia 
		anterior (x1) y la frecuencia posterior (x2).
	"""
	if frec_a_interpolar in [1500,'1.5k']:
		h_p = (lista[6]-lista[4]) * (((math.log10(1500))-math.log10(1000))/(math.log10(2000)-math.log10(1000))) + lista[4]
		lista[5] = round(h_p,1)
	elif frec_a_interpolar in [3000,'3k']:
		h_p = (lista[8]-lista[6]) * (((math.log10(1500))-math.log10(1000))/(math.log10(2000)-math.log10(1000))) + lista[6]
		lista[7] = round(h_p,1)
	elif frec_a_interpolar in [6000,'6k']:
		h_p = (lista[10]-lista[8]) * (((math.log10(1500))-math.log10(1000))/(math.log10(2000)-math.log10(1000))) + lista[8]
		lista[9] = round(h_p,1)

	return lista

def interpolando_tres_frec(lista):
	""" Recibe la lista y 3 valores de frecuencia a ser interpolados.

		Retorna una lista (c) con los tres valores de frecuencia interpolados.
	""" 
	a=interpolando_una_frec(lista,1500)
	b=interpolando_una_frec(a,3000)
	c=interpolando_una_frec(b,6000)
	return c

# INTERPOLADO

# # jrenum protección personal Atenuación Asumida APV
# sk_ld_10= interpolando_tres_frec(sk_ld_10,1500,3000,6000)
# sk_ld_18= interpolando_tres_frec(sk_ld_18,1500,3000,6000)
# sk_ld_26= interpolando_tres_frec(sk_ld_26,1500,3000,6000)# respuesta mas plana.

# # ER 15 tapones para músicos con respuesta plana - APV
# er_15= interpolando_tres_frec(er_15,1500,3000,6000)
# er_25= interpolando_tres_frec(er_25,1500,3000,6000)
# # ACS PRO 17
# acs_pro_17= interpolando_tres_frec(acs_pro_17,1500,3000,6000)

# # 3M desechables - APV
# tres_m_1100= interpolando_tres_frec(tres_m_1100,1500,3000,6000)
# tres_m_1281= interpolando_tres_frec(tres_m_1281,1500,3000,6000)
# # 3M con banda de mentón - APV
# tres_m_1310= interpolando_tres_frec(tres_m_1310,1500,3000,6000)

# # 3M orejeras - APV
# tres_m_1430= interpolando_tres_frec(tres_m_1430,1500,3000,6000)
# tres_m_1435= interpolando_tres_frec(tres_m_1435,1500,3000,6000)
# tres_m_1445= interpolando_tres_frec(tres_m_1445,1500,3000,6000)
# # 3M orejeras para casco - APV
# tres_m_1455= interpolando_tres_frec(tres_m_1455,1500,3000,6000)

# # Bilsom orejeras
# bilsom_817= interpolando_tres_frec(bilsom_817,1500,3000,6000)
# bilsom_818= interpolando_tres_frec(bilsom_818,1500,3000,6000)

# # Elvex SuperSonic™ protectores de ruido impulsivo
# hb_650= interpolando_tres_frec(hb_650,1500,3000,6000)
# hb_5000= interpolando_tres_frec(hb_5000,1500,3000,6000)