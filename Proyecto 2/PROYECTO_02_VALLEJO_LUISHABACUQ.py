# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 19:18:42 2020

@author: Habacuq
"""
import csv
def imprimirLista(lista): #esta función imprime listas bonitas
    for elemento in lista:
        print(elemento)
    
while True:
    print("\nBienvenido al asistente de opciones para Synergy\
          \n1. Rutas de importación y exportación\
          \n2. Medio de transporte utilizado\
          \n3. Valor total de importaciones y exportaciones\
          \n0. Salir")
    nMenu = input("Ingrese el número correspondiente a la opción que desea explorar: ")
    with open("synergy_logistics_database.csv", "r") as datos_csv:
        lector = csv.reader(datos_csv)
        datos = []
        for linea in lector:
            datos.append(linea) #guardo todo en una gran lista
    del(datos[0]) #quita los encabezados
    if nMenu == "0":
        print("¡Hasta luego!")
        break
    elif nMenu == "1":
        rutas = [] #Aquí meteré todas las rutas
        montos = [] #Aquí el monto de todas esas rutas
        for dato in datos:
            ruta = [dato[1], dato[2], dato[3]]
            if ruta not in rutas: #Y revisa si ya está
                rutas.append(ruta)
            dato.append(ruta) #Esto hará más fácil el conteo, añade la ruta
        for ruta in rutas:
            montos.append(0)
            for dato in datos: #Así no considera los encabezados
                if dato[-1] == ruta:
                    montos[-1] += int(dato[9])
        #Ya tenemos las rutas en una lista y los montos totales en otra
        #Ahora crearemos un diccionario con esos datos
        dicc = []
        for i in range(len(rutas)):
            dicc.append({'ruta':rutas[i],'monto':montos[i]})
        dicc = sorted(dicc, key = lambda i: i['monto'], reverse=True)
        #Ya tenemos las 10 rutas con más ingresos, ahora vamos a sumar los montos
        sumatop10 = 0
        for i in range(10):
            sumatop10 += dicc[i]['monto']
        porcentajerutas = sumatop10/sum(montos)
        print("Las 10 rutas con más concurrencia representan el " +
             "{0:.00%}".format(porcentajerutas) + " de los ingresos totales.")
        imprimirLista(dicc[0:10])
        #Ahora crearemos las listas de top 10 por impo y expo
        topImpo = []
        while True:
            for registro in dicc:
                if len(topImpo) == 10:
                    break
                if registro['ruta'][0] == "Imports":
                    topImpo.append(registro)
            break
        topExpo = []
        while True:
            for registro in dicc:
                if len(topExpo) == 10:
                    break
                if registro['ruta'][0] == "Exports":
                    topExpo.append(registro)
            break   
        sumatopImpo = 0         
        for impo in topImpo:
            sumatopImpo += impo['monto']
        porcentajeImpo = sumatopImpo/sum(montos)
        print("\nLas 10 rutas de importación con más concurrencia representan el " +
             "{0:.00%}".format(porcentajeImpo) + " de los ingresos totales.")
        imprimirLista(topImpo)
        sumatopExpo = 0
        for expo in topExpo:
            sumatopExpo += expo['monto']
        porcentajeExpo = sumatopExpo/sum(montos)
        print("\nLas 10 rutas de exportación con más concurrencia representan el " +
             "{0:.00%}".format(porcentajeExpo) + " de los ingresos totales.")
        imprimirLista(topExpo)
    elif nMenu == '2':
        #Primero crearemos una lista con todos los medios de transporte
        transportes = []
        for dato in datos:
            transporte = [dato[1], dato[7]]
            if transporte not in transportes:
                transportes.append(transporte)
            dato.append(transporte) #De nuevo, hará más fácil las comparaciones
        montos=[]
        for transporte in transportes:
            montos.append(0)
            for dato in datos:
                if dato[-1] == transporte:
                    montos[-1] += int(dato[9])
        #Ya tenemos las rutas y los montos en sus respectivas listas
        #De nuevo resumiremos est info en un diccionario
        dicc = []
        for i in range(len(montos)):
            dicc.append({'transporte':transportes[i], 'monto':montos[i], \
                         'porcentaje':"{0:.00%}".format(montos[i]/sum(montos))})
        dicc = sorted(dicc, key = lambda i: i['monto'], reverse=True)
        print("Los medios ordenados por uso y recaudación son los siguientes")
        imprimirLista(dicc)
        #Aquí no me pareció necesario ordenarlos o formar los top porque solo
        #hay 8 entradas entonces fácilmente se aprecia todo sobre la consigna
    elif nMenu == '3':
        paises = []
        for dato in datos:
            pais = dato[2]
            if pais not in paises:
                paises.append(pais)
        montos = []
        for pais in paises:
            montos.append(0)
            for dato in datos:
                if dato[2] == pais:
                    montos[-1] += int(dato[9])
        dicc = []
        for i in range(len(montos)):
            dicc.append({'pais':paises[i],'monto':montos[i]})
        dicc = sorted(dicc, key = lambda i: i['monto'], reverse=True)
        
        porcentajeAcumulado = 0
        montoTotal = sum(montos)
        for pais in dicc: #Añadimos el porcetaje acumulado
            porcentajeAcumulado += pais['monto']/montoTotal
            pais['Acumulado'] = porcentajeAcumulado
        print("Los países ordenados por recaudación son los siguientes")
        imprimirLista(dicc)
        #Ahora exportamos a un nuevo CSV que me llevaré a otro software para hacer
        #gráficas y cosas bonitas. 
        keys = dicc[0].keys()
        with open('paises.csv', 'w', newline='') as nuevoarchivo:
            dict_writer = csv.DictWriter(nuevoarchivo, keys)
            dict_writer.writeheader()
            dict_writer.writerows(dicc)
        #Debí haber hecho esto antes pero no se me ocurrió :( apenas le estoy
        #entendiendo a la utilidad de los diccionarios y la paquetería CSV
        #Esto lo abrí en Excel solo para hacer una tabla y copiarla en el word
    else:
        print('Error. No ha ingresado un número válido.')
                        
                        
                        
        