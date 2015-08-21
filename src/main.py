#!/usr/bin/env python
# -- coding: utf-8 --

""" 
    Esta es una herramienta para la estimación de pérdida auditiva debido al deterioro natural causado
    por la edad y el deterioro causado por la exposición al ruido ocupacional. 

    Además ayuda a educar al trabajador en el uso de protectores auditivos personales, por medio de la 
    visualización de gráficas y la audición de archivos de sonido que le permitirán notar una eventual
    pérdida auditiva a futuro en caso de no utilizar los mecanismos de protección adecuados.

    Para la realización de este software se utilizaron las siguientes normas:
        * ISO 1999 Acoustics – Determination of occupational noise exposure and estimation of
          noise induced hearing loss. 
        * ISO 4869 Acoustics - Hearing protectors.
    
    Sus equivalentes Españolas son:
        * UNE 74-023-92 Acústica - Determinación de la exposición al ruido en el trabajo y estimación 
          de las pérdidas auditivas inducidas por el ruido.
        * UNE-EN ISO 4869 Acústica - Protectores auditivos contra el ruido.

    Este código ha sido escrito por David Manuel Buitrago Montañez, como Trabajo de Fin de Maestría del
    posgrado titulado Máster Universitario en Ingeniería Acústica en la Industria y el Transporte, 
    cursado en la ESCUELA TÉCNICA SUPERIOR DE INGENIEROS INDUSTRIALES dependencia de la 
    UNIVERSIDAD POLITÉCNICA DE MADRID.

    Copyright (C) <2013>  <David Manuel Buitrago Montañez>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

# Importando librerias.
import kivy
kivy.require('1.7.1')
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel 
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup 
from kivy.properties import ListProperty
from kivy.uix.listview import ListView, ListItemLabel
from kivy.atlas import Atlas

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np 
from scipy.io import wavfile
from scipy.signal import butter, buttord, lfilter
from pygame.mixer import Sound
from pygame.mixer import Channel
from pygame.mixer import init
from collections import namedtuple
import os
import xlwt
import time
from datetime import datetime
from PIL import Image

import graficando_octavas
import graficando_protectores
import datos_protectores
import H
import H_prima
import H_prt
import H_prima_prt
import butter_tercio

import FileDialog
from scipy.special import _ufuncs_cxx

from kivy.resources import resource_add_path
resource_add_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images"))


__author__ = "David Manuel Buitrago Montañez"
__copyright__ = "Copyright 2013, David Manuel Buitrago Montañez, Trabajo Fin de Máster, Universidad Politécnica de Madrid"
__credits__ = ["David Manuel Buitrago Montañez", "Alvaro Javier Buitrago Montañez", 
                "Angela Patricia Giraldo Chaparro", "http://www.freesound.org/" ]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "David Manuel Buitrago Montañez"
__email__ = "caustico.acustico@gmail.com"
__status__ = "Prototype"

init(frequency=44100, size=-16, channels=2, buffer=4096) # inicialindo pygame.mixer
DatosIntroducidos = namedtuple("DatosIntroducidos", ["edad", "sexo", "fractil", "tiempo_exposicion", "nivel_exposicion" ])
resultado = None
datos_introducidos = None
directorio_audio = ''
audio_original = None


class Pestanas(TabbedPanel):
    pass

class ListaNumeros(ListItemLabel):
    pass

class ErrorEntrada(Exception):
    pass
#_________________________________________CALCULE_______________________________________________________________________________________________________
class CajaUnoUno(FloatLayout):

    textinput_edad= ObjectProperty()
    spinner= ObjectProperty()
    textinput_fractil= ObjectProperty()
    textinput_tiempo_exposicion= ObjectProperty()
    textinput_nivel_equivalente= ObjectProperty()

    list_wrapper= ObjectProperty()

    frecuencias = ListProperty()
    atenuacion_h_prima = ListProperty()
    atenuacion_h = ListProperty()

    frecuencias_widg = ListProperty()
    atenuacion_h_prima_widg = ListProperty()
    atenuacion_h_widg = ListProperty()

    imagen = ObjectProperty()

    def add_column(self,widget, lista):
        bl = BoxLayout(orientation="vertical")
        for element in lista[0]:
            lab = ListaNumeros(text=str(element))
            lista[1].append(lab)
            bl.add_widget(lab)
        widget.add_widget(bl)

    def add_lists(self, widget, *args):
        for i in args:
            self.add_column(widget, i)

    def redondeo(self,lista):
        """ Recibe una lista.

            Retorna cada valor redondeado al entero más próximo.
        """
        i= 0
        L = []
        while i < len(lista):
            lista[i] = int(round(float(lista[i]),0))
            L.append(lista[i])
            i+= 1
        return L

    def __init__(self,*args,**kwargs):
        super(CajaUnoUno,self).__init__(*args,**kwargs)
   
        self.frecuencias = ['125','250','500','1000','1500','2000','3000','4000','6000','8000']
        self.atenuacion_h_prima = ['0','0','0','0','0','0','0','0','0','0']
        self.atenuacion_h = ['0','0','0','0','0','0','0','0','0','0']
        Clock.schedule_once(self.on_carga, 1)

    def on_carga(self,instance):
        self.add_lists(self.list_wrapper,
            (self.frecuencias, self.frecuencias_widg),
            (self.atenuacion_h_prima, self.atenuacion_h_prima_widg),
            (self.atenuacion_h, self.atenuacion_h_widg)
        )
        self.imagen.source = os.path.join('images', 'bienvenido.png')

    def on_atenuacion_h_prima(self, instance, value):
        for index, labl in enumerate(self.atenuacion_h_prima_widg):
           labl.text = str(value[index]) 
       
    def on_atenuacion_h(self, instance, value):
        for index, labl in enumerate(self.atenuacion_h_widg):
           labl.text = str(value[index]) 

    def calcular(self):
        global resultado
        """ Verifica los parámetros de entrada y Retorna dos listas: 
            H y H'
            Según los parámetros de entrada ingresados por el usuario.
        """
        try:
            edad,sexo,tiempo_exposicion,nivel_exposicion,fractil = self.leer_entradas()
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return

        self.atenuacion_h_prima = self.redondeo(H_prima.h_prima(edad, sexo, tiempo_exposicion, nivel_exposicion, fractil))
        ate_h = self.atenuacion_h_prima[:]
        self.atenuacion_h = self.redondeo(H.h(edad, sexo, fractil))

        # LLENANDO LAS BANDAS FALTANTES DE H CON LOS DATOS DE LAS BANDAS DE H'
        for i,v in enumerate(ate_h):
            if v == 0:
                ate_h[i] = self.atenuacion_h[i]

        resultado = ate_h

        graficando_octavas.grafica_octavas(self.atenuacion_h_prima, self.atenuacion_h)
        self.imagen.source = os.path.join('images', 'H_y_Hprima_octavs.png')
        self.imagen.reload()

    def leer_entradas(self):
        #lee los parametros del text input y lo pasa a verificar parametros
        global datos_introducidos
        edad = self.textinput_edad.text
        sexo = self.spinner.text
        tiempo_exposicion = self.textinput_tiempo_exposicion.text
        nivel_exposicion = self.textinput_nivel_equivalente.text
        fractil = self.textinput_fractil.text

        self.verificar_parametros(edad,tiempo_exposicion,nivel_exposicion,fractil)
        
        edad = int(edad)
        sexo = str(sexo)
        tiempo_exposicion = int(tiempo_exposicion)
        nivel_exposicion = float(nivel_exposicion)
        fractil = float(fractil)

        datos_introducidos = DatosIntroducidos(edad, sexo, fractil, tiempo_exposicion, nivel_exposicion)

        return edad, sexo, tiempo_exposicion, nivel_exposicion, fractil

    def verificar_parametros(self, edad, tiempo_exposicion, nivel_exposicion, fractil):
        """ Esta función verifica que los parámetros de entrada sean correctos, es decir, que se encuentren en el
            rango aceptado por las demás funciones. Los parámetros de entrada son 
            -> tiempo_exposicion, nivel_exposicion <-

            Retorna un -1 si hay algún error, si no es así llama y ejecuta la siguiente función 
            n(tiempo_exposicion, nivel_exposicion).
        """
        t_exp = range(1,61,1)
        
        Q = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]  

        entradas_vacias= []
        if edad == '':
            entradas_vacias.append(u"\nIntroduzca Edad.")
        if fractil == '':
            entradas_vacias.append(u"\nIntroduzca Fráctil.")
        if tiempo_exposicion == '':
            entradas_vacias.append(u"\nIntroduzca Tiempo de Exposición.")
        if nivel_exposicion == '':
            entradas_vacias.append(u"\nIntroduzca Nivel de Exposición.")

        if entradas_vacias:
            raise ErrorEntrada('\n'.join(entradas_vacias))   
        
        entradas_erradas= []
        if not edad.isdigit():
            entradas_erradas.append(u"\nIntroduzca un valor válido para Edad.")
        try:
            fractil=float(fractil)
        except:
            entradas_erradas.append(u"\nIntroduzca un valor válido para Fráctil.")

        if not tiempo_exposicion.isdigit():
            entradas_erradas.append(u"\nIntroduzca un valor válido para Tiempo de Exposición.")
        
        try:
            nivel_exposicion=float(nivel_exposicion)
        except:
            entradas_erradas.append(u"\nIntroduzca un valor válido para Nivel de Exposición.")

        if entradas_erradas:
            raise ErrorEntrada('\n'.join(entradas_erradas))   

        edad= int(edad)
        tiempo_exposicion= int(tiempo_exposicion)
        nivel_exposicion= float(nivel_exposicion)
        fractil= float(fractil)
        
        Lex_8h = 0
        if nivel_exposicion >= 75 and nivel_exposicion <= 100:
            Lex_8h = nivel_exposicion

        lista_errores= []
        if edad < 19:
            lista_errores.append("\nLa edad debe estar entre 19 y 80 años.")
        if edad > 80:
            lista_errores.append("\nLa edad debe estar entre 19 y 80 años.")
        if fractil not in Q:
            lista_errores.append("\nEl fráctil debe estar en un rango desde 0.05 hasta 0.95\nen pasos de 0.05.")
        if edad < tiempo_exposicion:
            lista_errores.append("\nEl tiempo de exposición debe ser menor a la edad.")
        if edad - tiempo_exposicion < 18:
            lista_errores.append("\nEl tiempo de exposición no concuerda con la edad.")
        if tiempo_exposicion not in t_exp:
            lista_errores.append("\nEl tiempo de exposición debe estar entre 1 y 60 años.")
        if nivel_exposicion != Lex_8h:
            lista_errores.append("\nEl nivel de exposición debe estar entre 75dB y 100dB.\n")

        if lista_errores:
            raise ErrorEntrada('\n'.join(lista_errores))

        return edad,tiempo_exposicion,nivel_exposicion,fractil
    
    def show_popup(self, mensaje_error):
        # mensaje_error = self.gestionar_errores()
        btnclose = Button(text='Aceptar', size_hint_y=None, height='50sp')
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=mensaje_error))
        content.add_widget(btnclose)
        popup = Popup(content=content, title='¡¡ERROR!!\nPor Favor Verifique los Valores Ingresados.',
                      size_hint=(None, None), size=('400dp', '350dp'))
        btnclose.bind(on_release=popup.dismiss)
        popup.open()
        col = AnchorLayout()
        return col   

    def limpiar(self):
        self.textinput_edad.text = ''
        self.textinput_fractil.text = ''
        self.textinput_tiempo_exposicion.text= ''
        self.textinput_nivel_equivalente.text = ''
        self.atenuacion_h_prima = [0,0,0,0,0,0,0,0,0,0]
        self.atenuacion_h = [0,0,0,0,0,0,0,0,0,0]
        self.imagen.source = os.path.join('images', 'H_y_Hprima_octavs_clear.png')

#_____________________________________ESCUCHE________________________________________________________________________________________________________
class LoadButton(BoxLayout):
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Seleccione un Audio", content=content, size_hint=(0.8, 0.8))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.parent.parent.parent.parent.parent.filtrar_y_graficar_audio(0,filename[0])
        self.dismiss_popup()

class LoadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Escuchalo(BoxLayout):
    imagen_waveform =  ObjectProperty()
    imagen_espectro = ObjectProperty()
    texto_path_audio = ObjectProperty()

    def __init__(self,*args,**kwargs):
        super(Escuchalo,self).__init__(*args,**kwargs)
        self.original = None
        Clock.schedule_once(self.en_carga, 1)

    def en_carga(self,instance):    
        self.imagen_waveform.source = os.path.join('images', 'fondo_forma_onda.png')
        self.imagen_espectro.source = os.path.join('images', 'escuchelo.png')

    def filtrar_y_graficar_audio(self, instance, value):
        global resultado
        global audio_original
        try:
            self.verificar_parametros(resultado)
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return

        self.path= value
        self.datos = resultado
        butter_tercio.filtrar(self.datos,self.path)
        self.original = Sound(self.path)
        audio_original = self.original
        self.filtrado = Sound(os.path.join('audios', 'audio_filtrado', 'filtrado_butter_tercio.wav'))
        
        self.graficando_forma_de_onda()
        self.imagen_waveform.source = os.path.join('images', 'forma_de_onda.png')
        self.imagen_waveform.reload()
        
        fs,audio= butter_tercio.leer_audio(self.path)
        audio_filtrado= butter_tercio.leer_audio(os.path.join('audios', 'audio_filtrado', 'filtrado_butter_tercio.wav'))[1]
        self.plotear_espectro(audio,audio_filtrado,fs, os.path.join('images', 'espectros.png'))
        self.imagen_espectro.source = os.path.join('images', 'espectros.png')
        self.imagen_espectro.reload()
        global directorio_audio
        directorio_audio = self.path
        self.texto_path_audio.text = os.path.basename(directorio_audio)


    def verificar_parametros(self, resultado):
        entradas_vacias= []
        if resultado == None:
            entradas_vacias.append(u"\nDiríjase a la pestaña 'Calcúlelo'e ingrese los datos.\nNO OLVIDE PRESIONAR EL BOTÓN -Calcular- \n")
        if entradas_vacias:
            raise ErrorEntrada('\n'.join(entradas_vacias)) 
        
    def show_popup(self, mensaje_error):
        btnclose = Button(text='Aceptar', size_hint_y=None, height='50sp')
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=mensaje_error))
        content.add_widget(btnclose)
        popup = Popup(content=content, title='¡¡ERROR!!',
                      size_hint=(None, None), size=('400dp', '180dp'))
        btnclose.bind(on_release=popup.dismiss)
        popup.open()
        col = AnchorLayout()
        return col   

    def graficando_forma_de_onda(self):
        """ No recibe nada, los datos los toma directamente desde la clase.

            Retorna una gráfica con las formas de onda por separado de los canales L y R o 
            un solo canal si es MONO.
        """
        sonido_entrada= wavfile.read(self.path)
        freq_sampleo= sonido_entrada[0]
        dt= 256   

        estereo = sonido_entrada[1]
        azul= (54/255.,169/255.,177/255.)
        rojo= (207/255.,63/255.,67/255.)

        if len(estereo.shape) == 2:
            canal_l= estereo[:,0]
            canal_r= estereo[:,1]
            longitud = np.arange(0,len(estereo),dt)
            canal_l= canal_l[range(0,len(canal_l),dt)]
            canal_r= canal_r[range(0,len(canal_r),dt)]
            
            fig = plt.figure(frameon=False)
            fig.set_size_inches(2.5,1.25)
            plt.subplots_adjust(hspace = 0)

            plt.subplot(211)
            plt.plot(longitud,canal_l,color=rojo,label='L')
            frame1 = plt.gca()
            frame1.axes.get_xaxis().set_visible(False)
            frame1.axes.get_yaxis().set_visible(False)
            plt.xlim(min(longitud),max(longitud))
            plt.legend(loc='lower left',prop={'size':5})
            
            plt.subplot(212)
            plt.plot(longitud,canal_r,color=azul,label='R')
            frame1 = plt.gca()
            frame1.axes.get_xaxis().set_visible(False)
            frame1.axes.get_yaxis().set_visible(False)
            plt.xlim(min(longitud),max(longitud))
            plt.legend(loc='lower left',prop={'size':5})
            plt.savefig(os.path.join('images', 'forma_de_onda.png'))

        elif len(estereo.shape) == 1:
            canal_l= estereo
            longitud = np.arange(0,len(canal_l),dt)
            canal_l= canal_l[range(0,len(canal_l),dt)]
            
            fig = plt.figure(frameon=False)
            fig.set_size_inches(2.5,1.25)

            frame1 = plt.gca()
            frame1.axes.get_xaxis().set_visible(False)
            frame1.axes.get_yaxis().set_visible(False)

            plt.step(longitud,canal_l,color=rojo)
            plt.xlim(min(longitud),max(longitud))
            plt.savefig(os.path.join('images', 'forma_de_onda.png'))

    def plotear_espectro(self, y1, y2, Fs, nombre_salida):
        """ Recibe como entrada y = Data de audio sin filtrar.
                               y2 = Data de audio filtrado.
                               Fs = Frecuencia de Muestreo.
                    nombre_salida = nombre con el que se guardará la imagen.

            Retorna una grafica del espectro de la señal.
        """
        plt.figure(figsize= (10,6), dpi= 80)
        plt.axes([.005,0.085,0.99,0.91])
        # Colores RGBA
        azul= (54/255.,169/255.,177/255.)
        rojo= (207/255.,63/255.,67/255.)

        n= len(y1)
        dt= 128
        k= np.arange(n)
        T= n/Fs
        frq= k/T
        frq= frq[range(0,n/2,dt)]

        if len(y1.shape) == 2:
            Y1= np.fft.rfft(y1[:,0])
            Y2= np.fft.rfft(y2[:,0])
            Y1= (20*np.log10((Y1)))/n
            Y2= (20*np.log10((Y2)))/n
            Y1= abs(Y1[range(0,n/2,dt)])
            Y2= abs(Y2[range(0,n/2,dt)])
            plt.xlim((45,11314)) # (frec. mín. menos (-) su propio ancho de banda, frec.max. mas (+) ancho de su propia banda.)
            plt.xscale('log')
            plt.step(frq,Y1,color=azul,label=u'Original')
            plt.step(frq,Y2,color=rojo,label=u'Filtrado')
            plt.legend(loc='lower left',prop={'size':12})
            plt.xlabel('Frecuencia (Hz)')
            plt.xticks([63,125,250,500,1000,1500,2000,3000,4000,6000,8000], 
            [r'$63$',r'$125$',r'$250$', r'$500$',r'$1000$',r'$1500$',r'$2000$',r'$3000$',r'$4000$',r'$6000$',r'$8000$'])
            plt.grid(True)
            plt.savefig(nombre_salida)

        elif len(y1.shape) == 1:
            Y1= np.fft.rfft(y1)
            Y2= np.fft.rfft(y2)
            Y1= (20*np.log10((Y1)))/n
            Y2= (20*np.log10((Y2)))/n
            Y1= abs(Y1[range(0,n/2,dt)])
            Y2= abs(Y2[range(0,n/2,dt)])
            plt.xlim((45,11314))
            plt.xscale('log')
            plt.step(frq,Y1,color=azul,label=u'Original')
            plt.step(frq,Y2,color=rojo,label=u'Filtrado')
            plt.legend(loc='lower left',prop={'size':12})
            plt.xlabel('Frecuencia (Hz)')
            plt.ylabel('Y')
            plt.xticks([63,125,250,500,1000,1500,2000,3000,4000,6000,8000], 
            [r'$63$',r'$125$',r'$250$', r'$500$',r'$1000$',r'$1500$',r'$2000$',r'$3000$',r'$4000$',r'$6000$',r'$8000$'])
            plt.grid(True)
            plt.savefig(nombre_salida) 

    canal_uno= Channel(1)
    canal_dos= Channel(3)

    def revisar_audio_cargado(self):
        if self.original == None:
            raise ErrorEntrada('\nNo se ha seleccionado ningún Audio.\n')

    def play_original(self):
        try:
            self.revisar_audio_cargado()
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return

        self.canal_uno.stop()
        self.canal_uno.queue(self.original)

        if not self.canal_uno.get_busy(): # si no está ocupado reproduzca
            self.canal_uno.play()
        else:
            self.canal_uno.unpause()

    def pause_original(self):

        if self.canal_uno.get_busy():
            self.canal_uno.pause()

    def stop_original(self):

        if self.canal_uno.get_busy():
            self.canal_uno.stop()
#___________________________________________________#_
    def play_filtrado(self):
        try:
            self.revisar_audio_cargado()
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return

        self.canal_dos.stop()
        self.canal_dos.queue(self.filtrado)

        if not self.canal_dos.get_busy(): # si no está ocupado reproduzca
            self.canal_dos.play()
        else:
            self.canal_dos.unpause()

    def pause_filtrado(self):
        if self.canal_dos.get_busy():
            self.canal_dos.pause()

    def stop_filtrado(self):
        if self.canal_dos.get_busy():
            self.canal_dos.stop()

#________________________________PREVENGA______________________________________________________________________________________________________________________________________
class Protegete(BoxLayout):

    spinner_prt= ObjectProperty()
    list_wrapper= ObjectProperty()

    frecuencias_prt = ListProperty()
    interpolado_protectores = ListProperty()
    atenuacion_protegido = ListProperty()

    frecuencias_prt_widg = ListProperty()
    interpolado_protectores_widg = ListProperty()
    atenuacion_protegido_widg = ListProperty()

    imagen_prt = ObjectProperty()
    imagen_prt_epi= ObjectProperty()

    sesentaytres = ObjectProperty()
    cientoveinticinco = ObjectProperty()
    doscientoscincuenta = ObjectProperty()
    quinientos = ObjectProperty()
    mil = ObjectProperty()
    dosmil = ObjectProperty()
    cuatromil = ObjectProperty()
    ochomil = ObjectProperty()


    def add_column(self, widget, lista):
        bl = BoxLayout(orientation="vertical")
        for element in lista[0]:
            lab = ListaNumeros(text=str(element))
            lista[1].append(lab)
            bl.add_widget(lab)
        widget.add_widget(bl)

    def add_lists(self, widget, *args):
        for i in args:
            self.add_column(widget, i)

    def redondeo(self,lista):
        """ Recibe una lista.

            Retorna cada valor redondeado al entero más próximo.
        """

        i= 0
        L = []
        while i < len(lista):
            lista[i] = int(round(float(lista[i]),0))
            L.append(lista[i])
            i+= 1
        return L

    def __init__(self,*args,**kwargs):
        super(Protegete,self).__init__(*args,**kwargs)
   
        self.frecuencias_prt = ['63','125','250','500','1000','1500','2000','3000','4000','6000','8000']
        self.interpolado_protectores = ['0','0','0','0','0','0','0','0','0','0','0']
        self.atenuacion_protegido = ['0','0','0','0','0','0','0','0','0','0','0']
        Clock.schedule_once(self.in_carga, 1)

    def in_carga(self,instance):
        self.add_lists(self.list_wrapper,
            (self.frecuencias_prt, self.frecuencias_prt_widg),
            (self.interpolado_protectores, self.interpolado_protectores_widg),
            (self.atenuacion_protegido, self.atenuacion_protegido_widg)
        )

        self.imagen_prt_epi.source = os.path.join('images', 'protector.png')
        self.imagen_prt.source = os.path.join('images', 'protejase.png')
        self.spinner_prt.bind(text = self.the_spinner_prt)
        self.protector_usuario = ['','','','','','','','','','','']
        self.sesentaytres.text = ''
        self.cientoveinticinco.text = ''
        self.doscientoscincuenta.text = ''
        self.quinientos.text = ''
        self.mil.text = ''
        self.dosmil.text = ''
        self.cuatromil.text = ''
        self.ochomil.text = ''   
    
    def the_spinner_prt(self, instance, value):
        """ Recibe la instancia y el valor, son dados por el observer

            Retorna una imagen que corresponde a la imagen del Protector.
        """
        if self.spinner_prt.text == "Seleccione un Protector":
            self.imagen_prt_epi.source = os.path.join('images', 'protector.png' )
        else:
            self.imagen_prt_epi.source = os.path.join('images', '%s.jpg' % value)
            self.imagen_prt_epi.reload()

    def on_interpolado_protectores(self, instance, value):
        for index, labl in enumerate(self.interpolado_protectores_widg):
            labl.text = str(value[index]) 

    def on_atenuacion_protegido(self, instance, value):
        for index, labl in enumerate(self.atenuacion_protegido_widg):
            labl.text = str(value[index]) 

    def seleccionar_protector(self):
        """ Lee lo que envía el Observer en el Spinner y extrae el texto.

            Retorna la lista con los datos del protector que se desea evaluar.
        """
        self.protector_usuario = [self.sesentaytres.text, self.cientoveinticinco.text,
                             self.doscientoscincuenta.text,self.quinientos.text,
                             self.mil.text, '0',
                             self.dosmil.text,'0',
                             self.cuatromil.text, '0', self.ochomil.text]

        if self.protector_usuario == ['','','','','','0','','0','','0',''] or self.protector_usuario == None:
            protectores={'sk_ld_10':[5.0,5.8,10.6,14.7,23.8,0.0,28.8,0.0,32.4,0.0,36.2],
                        'sk_ld_18':[16.8,20.2,21.4,23.9,26.,0.0,29.7,0.0,34.4,0.0,37.5],
                        'sk_ld_26':[24.6,27.8,26.,29.5,29.9,0.0,32.2,0.0,37.9,0.0,39.],
                        'er_15':[0.0,15.7,14.6,12.6,13,0.0,12.4,0.0,12.2,0.0,16.8],
                        'er_25':[0.0,22.2,22.,20.,20.4,0.0,20.1,0.0,20.4,0.0,25.1],
                        'acs_pro_17':[0.0,17.94,17.92,15.95,15.85,0.0,14.73,0.0,17.4,0.0,16.58],
                        'tres_m_1100':[2.61,28.1,28.9,32.2,33.1,0.0,35.4,0.0,43.8,0.0,40.],
                        'tres_m_1281':[11.5,14.6,14.7,15.5,17.6,0.0,23.6,0.0,22.6,0.0,28.5],
                        'tres_m_1310':[17.6,17.1,17.3,19.3,22.1,0.0,31.6,0.0,36.2,0.0,39.1],
                        'tres_m_1430':[11.4,8.7,10.7,15.5,26.2,0.0,31.8,0.0,39.5,0.0,30.8],
                        'tres_m_1435':[8.1,8.1,14.5,18.6,27.,0.0,25.,0.0,31.3,0.0,29.8],
                        'tres_m_1445':[14.6,17.2,21.8,26.7,31.7,0.0,29.8,0.0,36.,0.0,37.7],
                        'tres_m_1455':[10.8,16.4,20.7,25.1,31.1,0.0,29.9,0.0,35.5,0.0,37.],
                        'bilsom_817':[8.1,12.4,21.2,25.,20.4,0.0,23.8,0.0,26.,0.0,28.4],
                        'bilsom_818':[8.9,12.3,19.1,22.3,21.9,0.0,26.6,0.0,26.6,0.0,30.3],
                        'hb_650':[15.5,16.6,23.3,31.4,36.4,0.0,32.1,0.0,40.6,0.0,33.7],
                        'hb_5000':[0.0,17.7,23.6,34.8,37.3,0.0,34.1,33.8,40.2,39.,38.3]}

            protector= self.spinner_prt.text
            if protector in protectores.keys():
                return protectores[protector]
            else:
                return None
            
        else:
            self.spinner_prt.text = "Protector Personalizado"
            self.imagen_prt_epi.source = os.path.join('images', 'protector.png' )
            lista_errores = ['','-','-0']
            prot_usuario_numeros = []
            for i,v in enumerate(self.protector_usuario):
                if v in lista_errores:
                    v = 0
                numero = float(v)
                prot_usuario_numeros.append(numero)

            protector = prot_usuario_numeros
            return protector

        
    def show_popup(self, mensaje_error):
        btnclose = Button(text='Aceptar', size_hint_y=None, height='50sp')
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=mensaje_error))
        content.add_widget(btnclose)
        popup = Popup(content=content, title='¡¡ERROR!!',
                      size_hint=(None, None), size=('400dp', '180dp'))
        btnclose.bind(on_release=popup.dismiss)
        popup.open()
        col = AnchorLayout()
        return col   

    def verificar_parametros(self, resultado):
        global datos_introducidos

        entradas_vacias= []
        if datos_introducidos == None:
            entradas_vacias.append(u"\nDiríjase a la pestaña 'Calcúlelo'e ingrese los datos.\nNo olvide hacer click en el botón -Calcular-\n")
        if self.seleccionar_protector() in [None,"Seleccione un Protector"] and self.protector_usuario == ['','','','','','0','','0','','0','']:
            raise ErrorEntrada(u"\nNo se ha seleccionado ningún Protector\nNo se han introducido datos del Protector\n")

        if entradas_vacias:
            raise ErrorEntrada('\n'.join(entradas_vacias))   

    def revisar_audio_cargado(self):
        global audio_original
        if audio_original == None:
            raise ErrorEntrada('\nNo se ha seleccionado ningún Audio.\n')

    def calcular_prt(self): 
        global datos_introducidos

        try:
            self.verificar_parametros(datos_introducidos)
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return

        try:
            self.verificar_parametros(self.seleccionar_protector)
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return
           
        edad=  datos_introducidos.edad      
        sexo = datos_introducidos.sexo     
        tiempo_exposicion = datos_introducidos.tiempo_exposicion     
        nivel_exposicion =  datos_introducidos.nivel_exposicion
        fractil =   datos_introducidos.fractil
        protector_lst = self.seleccionar_protector()
        self.atenuacion_h_prt = H_prt.h(edad, sexo, fractil)
        self.atenuacion_h_prima_prt = H_prima_prt.h_prima(edad, sexo, tiempo_exposicion, nivel_exposicion, fractil)
        self.atenuacion_protegido = self.atenuacion_h_prima_prt
        self.interpolado_protectores = datos_protectores.interpolando_tres_frec(protector_lst)
        self.atenuacion_protegido = np.array(self.atenuacion_protegido) - np.array(self.interpolado_protectores)
        graficando_protectores.grafica_octavas_protectores(self.atenuacion_h_prima_prt, 
                                                            self.atenuacion_h_prt,
                                                            self.interpolado_protectores,
                                                            self.atenuacion_protegido)
        self.imagen_prt.source = os.path.join('images', 'grafica_protectores.png')
        self.imagen_prt.reload()
        return self.atenuacion_h_prt, self.atenuacion_h_prima_prt, self.interpolado_protectores, self.atenuacion_protegido
    

    def limpiar_prt(self):
        self.interpolado_protectores = [0,0,0,0,0,0,0,0,0,0,0]
        self.atenuacion_protegido = [0,0,0,0,0,0,0,0,0,0,0]
        self.imagen_prt_epi.source = os.path.join('images', 'protector.png' )
        self.imagen_prt.source = os.path.join('images', 'protectores_octavas_clear.png')

        self.sesentaytres.text = ''
        self.cientoveinticinco.text= ''
        self.doscientoscincuenta.text= ''
        self.quinientos.text= ''
        self.mil.text = ''
        self.dosmil.text = ''
        self.cuatromil.text = ''
        self.ochomil.text = ''      

        self.spinner_prt.text = 'Seleccione un Protector'


    def guardar_informe(self):
        # GESTION DE ERRORES
        global datos_introducidos

        try:
            self.verificar_parametros(datos_introducidos)
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return

        try:
            self.revisar_audio_cargado()
        except ErrorEntrada as e:
            self.show_popup(e.message)
            return
        
        frecuencias = [63,125,250,500,1000,1500,2000,3000,4000,6000,8000]
        h,h_prima,atenuacion_h,atenuacion_h_prima = self.calcular_prt()

        wbk = xlwt.Workbook(encoding='utf-8')
        hoja_datos = wbk.add_sheet('1. DATOS', cell_overwrite_ok=True)
        hoja_datos.protect = True
        sheet = wbk.add_sheet(u'2. CALCÚLE', cell_overwrite_ok=True)
        sheet.protect = True
        sheet1 = wbk.add_sheet(u'3. ESCÚCHE', cell_overwrite_ok=True)
        sheet1.protect = True
        sheet2 = wbk.add_sheet(u'4. PREVÉNGA', cell_overwrite_ok=True)
        sheet2.protect = True

        alignment = xlwt.Alignment() # Create Alignment 
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        borders = xlwt.Borders() # Create Borders 
        borders.left = xlwt.Borders.MEDIUM
        borders.right = xlwt.Borders.MEDIUM 
        borders.top = xlwt.Borders.MEDIUM 
        borders.bottom = xlwt.Borders.MEDIUM
        borders.left_colour = 0x40 
        borders.right_colour = 0x40 
        borders.top_colour = 0x40 
        borders.bottom_colour = 0x40

        estilobg = xlwt.XFStyle() 
        pattern = xlwt.Pattern() # Create the Pattern 
        pattern.pattern = xlwt.Pattern.NO_PATTERN 
        pattern.pattern_fore_colour = xlwt.Style.colour_map['white']

        # ENCABEZADOS 1 -ARIAL 13- -BOLD- -IZQUIERDA- -CON BORDES-
        estilo11 = xlwt.XFStyle() 
        font = xlwt.Font()
        font.name = 'Arial'
        font.height = 260
        font.bold = True
        estilo11.font = font
        estilo11.borders = borders

        # TÍTULO -ARIAL 15- -BOLD- -CENTRADO-
        estilo = xlwt.XFStyle()
        font = xlwt.Font()
        font.height = 300
        font.bold = True
        estilo.font = font
        estilo.alignment = alignment

        # ENCABEZADOS 2 -ARIAL 13- -BOLD- -CENTRADO- -SIN BORDES-
        estilo12 = xlwt.XFStyle()
        font.height = 260
        font.bold = True
        estilo12.font = font
        estilo12.alignment = alignment

        # FRECUENCIAS -ARIAL 13- -BOLD- -CENTRADO- -CON BORDES-
        estilo1 = xlwt.XFStyle()
        font.height = 260
        font.bold = True
        estilo1.font = font
        estilo1.alignment = alignment
        estilo1.borders = borders

        # VALORES -ARIAL 13- -CENTRADO- -CON BORDES-
        estilo2 = xlwt.XFStyle()
        font = xlwt.Font()
        font.height = 260
        estilo2.font = font
        estilo2.alignment = alignment
        estilo2.borders = borders

        # VALORES -ARIAL 13- -CENTRADO- -SIN BORDES-
        estilo21 = xlwt.XFStyle()
        font = xlwt.Font()
        font.height = 260
        estilo21.font = font
        estilo21.alignment = alignment

        fecha_hora = datetime.now().strftime('%d/%m/%y %H:%M')
        # DATOS INTRODUCIDOS ___________________________________________________
        
        edad=  datos_introducidos.edad      
        sexo = datos_introducidos.sexo     
        tiempo_exposicion = datos_introducidos.tiempo_exposicion     
        nivel_exposicion =  datos_introducidos.nivel_exposicion
        fractil =   datos_introducidos.fractil

        hoja_datos.write_merge(0,4,0,13,'',estilobg)
        hoja_datos.write_merge(5,9,0,5,'',estilobg)
        hoja_datos.write_merge(5,9,8,13,'',estilobg)
        hoja_datos.write_merge(10,11,0,13,'',estilobg)

        hoja_datos.write_merge(0,0,0,13,u'INFORME SOFTWARE CALCÚLE, ESCÚCHE Y PREVÉNGA',estilo)
        hoja_datos.write_merge(1,1,0,13,'Fecha: '+ fecha_hora + ' - Página 1/4',estilo12)
        hoja_datos.write_merge(3,3,0,13,u'DATOS',estilo12)
        hoja_datos.write(5,6,'Edad:',estilo11)
        hoja_datos.write(6,6,'Sexo:',estilo11)
        hoja_datos.write(7,6,u'Fráctil:',estilo11)
        hoja_datos.write(8,6,u'Tiempo de Exposición:',estilo11)
        hoja_datos.write(9,6,u'Nivel de Exposición:',estilo11) 

        hoja_datos.write(5,7,edad,estilo2)
        hoja_datos.write(6,7,sexo,estilo2)
        hoja_datos.write(7,7,fractil,estilo2)
        hoja_datos.write(8,7,tiempo_exposicion,estilo2)
        hoja_datos.write(9,7,nivel_exposicion,estilo2)

        hoja_datos.col(6).width = 256*28
        hoja_datos.col(7).width = 256*7

        i=0
        while i < 6:
            hoja_datos.col(i).width = 256*6
            i+=1
        i=8
        while i < 14:
            hoja_datos.col(i).width = 256*6
            i+=1

        hoja_datos.write_merge(12,12,0,13,'Continúe a la página 2 >>>>', estilo21)
        # hoja_datos.write_merge(12,12,0,13,'Con ɔopyleft', estilo21)

        # INFORME CALCÚLE ______________________________________________________
        sheet.write_merge(0,4,0,13,'',estilobg)
        sheet.write_merge(5,7,0,0,'',estilobg)
        sheet.write_merge(5,7,13,13,'',estilobg)
        sheet.write_merge(8,35,0,13,'',estilobg)

        sheet.write_merge(0,0,0,13,u'INFORME SOFTWARE CALCÚLE, ESCÚCHE Y PREVÉNGA',estilo)
        sheet.write_merge(1,1,0,13,'Fecha: '+ fecha_hora + ' - >>> Página 2/4 <<<',estilo12)
        sheet.write_merge(3,3,0,13,u'ESTIMACIÓN DE PÉRDIDA AUDITIVA H Y H\'',estilo12)
        sheet.write(5,1,'Frec. (Hz)',estilo11)
        sheet.write(6,1,'H',estilo11)
        sheet.write(7,1,'H\'',estilo11)

        for i,x in enumerate(frecuencias):
            sheet.write(5,i+2,frecuencias[i],estilo1) # Freq
            sheet.write(6,i+2,h[i],estilo2) # H
            sheet.write(7,i+2,h_prima[i],estilo2) # H'

        # ancho columnas
        sheet.col(0).width = 256*7 # una pulgada
        sheet.col(1).width = 256*13 # 256 * Nro caracteres
        sheet.col(2).width = 256*6
        sheet.col(3).width = 256*6
        sheet.col(4).width = 256*6

        i=5
        while i < 14:
            sheet.col(i).width = 256*7
            i+=1

        ancho = 605
        alto = 454
        imagen = Image.open(os.path.join('images', 'H_y_Hprima_octavs.png')).resize((ancho,alto),Image.ANTIALIAS).convert('RGB').save(os.path.join('images', 'H_y_Hprima_octavs.bmp'))
        sheet.insert_bitmap(os.path.join('images', 'H_y_Hprima_octavs.bmp'),9,1)

        # INFORME ESCÚCHE __________________________________________________________________
        sheet1.write_merge(0,39,0,13,'',estilobg)

        sheet1.write_merge(0,0,0,13,u'INFORME SOFTWARE CALCÚLE, ESCÚCHE Y PREVÉNGA',estilo)
        sheet1.write_merge(1,1,0,13,'Fecha: '+ fecha_hora + ' - >>> Página 3/4 <<<',estilo12)
        global directorio_audio
        audio_seleccionado= directorio_audio
        sheet1.write_merge(3,3,0,13,'Audio: '+ os.path.basename(audio_seleccionado),estilo21)
        sheet1.write_merge(5,5,0,13,u'FORMA DE ONDA',estilo12)
        sheet1.write_merge(12,12,0,13,u'ESPÉCTRO',estilo12)

        alto1= 95
        ancho1= 296 + 100
        imagen1 = Image.open(os.path.join('images', 'forma_de_onda.png')).resize((ancho1,alto1),Image.ANTIALIAS).convert('RGB').save(os.path.join('images', 'forma_de_onda.bmp'))
        sheet1.insert_bitmap(os.path.join('images', 'forma_de_onda.bmp'),6,3)

        ancho11= ancho + 165
        imagen11 = Image.open(os.path.join('images', 'espectros.png')).resize((ancho11,alto),Image.ANTIALIAS).convert('RGB').save(os.path.join('images', 'espectros.bmp'))
        sheet1.insert_bitmap(os.path.join('images', 'espectros.bmp') ,13,1)

        sheet1.col(0).width = 256*7 # una pulgada
        sheet1.col(1).width = 256*13 # 256 * Nro caracteres
        sheet1.col(2).width = 256*6
        sheet1.col(3).width = 256*6
        sheet1.col(4).width = 256*6
        i=5
        while i < 14:
            sheet1.col(i).width = 256*7
            i+=1

        # INFORME PREVÉNGA _______________________________________________________________
        sheet2.write_merge(0,4,0,13,'',estilobg)
        sheet2.write_merge(5,7,0,0,'',estilobg)
        sheet2.write_merge(5,7,13,13,'',estilobg)
        sheet2.write_merge(8,39,0,13,'',estilobg)

        sheet2.write_merge(0,0,0,13,u'INFORME SOFTWARE CALCÚLE, ESCÚCHE Y PREVÉNGA',estilo)
        sheet2.write_merge(1,1,0,13,'Fecha: '+ fecha_hora + ' - >>> Página 4/4 <<<',estilo12)
        sheet2.write_merge(3,3,0,13,u'ATENUACIÓN PROTECTORES AUDITIVOS',estilo12)
        sheet2.write(5,1,'Frec. (Hz)',estilo11)
        sheet2.write(6,1,'At. EPI',estilo11)
        sheet2.write(7,1,'At. Est. H\'',estilo11)

        protector_auditivo= self.spinner_prt.text
        sheet2.write_merge(9,9,0,6,u'Protector Auditivo: '+ protector_auditivo,estilo21)

        for i,x in enumerate(frecuencias):
            sheet2.write(5,i+2,frecuencias[i],estilo1)
            sheet2.write(6,i+2,atenuacion_h[i],estilo2)
            sheet2.write(7,i+2,atenuacion_h_prima[i],estilo2)

        sheet2.col(0).width = 256*7 # una pulgada
        sheet2.col(1).width = 256*13 # 256 * Nro caracteres
        sheet2.col(2).width = 256*6
        sheet2.col(3).width = 256*6
        sheet2.col(4).width = 256*6

        i=5
        while i < 14:
            sheet2.col(i).width = 256*7
            i+=1

        ancho2= 76
        alto2= 76

        imagen2 = Image.open(os.path.join('images', 'grafica_protectores.png')).resize((ancho,alto),Image.ANTIALIAS).convert('RGB').save(os.path.join('images', 'grafica_protectores.bmp'))
        sheet2.insert_bitmap(os.path.join('images', 'grafica_protectores.bmp'),13,1)

        imagen_protector= self.imagen_prt_epi.source

        imagen22 = Image.open(imagen_protector).resize((ancho2,alto2),Image.ANTIALIAS).convert('RGB').save(os.path.join('images', 'protector_seleccionado.bmp'))
        sheet2.insert_bitmap(os.path.join('images', 'protector_seleccionado.bmp') ,9,11)


        wbk.save('Informe_CEP.xls')
        os.system('start excel.exe "Informe_CEP.xls"')



class CEPApp(App):
    def on_start(self):
        self._app_window.size = 875,620
    def build(self):
        return Pestanas()

if __name__ == '__main__':
    CEPApp().run()
