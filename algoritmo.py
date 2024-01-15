#Emparejamiento
import itertools
import random
from turtle import heading
import numpy as np
import tkinter as tk
from tkinter import Label, Entry, Button,StringVar, OptionMenu
import matplotlib.pyplot as plt
import math

intervalo =[-4,4]
Resolución= 0.05
poblacion_inicial=15
cantidad_generaciones=5
posibilidad_de_cruza=70
posibilidad_de_mutacion_individuo=50
posibilidad_de_mutacion_gen=25
limite_poblacion=15
maximos=[]
minimos=[]
generaciones = []
promedios=[]


opcion_max_min ="maximizar"

def main ():
    tamaño_generaciones=[]
    iteracion_gen=[]
    def calculo_rango(intervalo):
        # Asegurémonos de que el intervalo tiene exactamente dos elementos
        if len(intervalo) != 2:
            return "El intervalo debe contener exactamente dos valores"

        # Calcula el rango usando la fórmula rango = b - a
        a, b = intervalo
        rango = b - a
        return rango
    
    resultado_rango= calculo_rango(intervalo)

    def calcular_bits (resultado_rango,Resolución):

        num_saltos= (resultado_rango/Resolución)+1

        # Calcula la potencia de 2 según la regla 2^(n-1) <= # puntos <= 2^n
        n = 1

        while not (2*n - 1 <= num_saltos <= 2**n):
            n += 1

            # Incrementa n para probar con un nuevo valor
            print(n)
        bits=n

        return bits

    puntos_bits = calcular_bits(resultado_rango,Resolución)
    print(f"El número de puntos para un rango de y resolución de {Resolución} es: {puntos_bits}")

    def Delta_x(resultado_rango,puntos_bits):
        DeltaX= (resultado_rango/(2**puntos_bits-1))

        return DeltaX
    
    Calculo_DeltaX= round(Delta_x(resultado_rango,puntos_bits),4)
    print(f"{Calculo_DeltaX}")


    def generar_poblacion_inicial(bits, poblacion_inicial):
        poblacion = []

        for _ in range(poblacion_inicial):
            numero_binario = ''.join(random.choice('01') for _ in range(bits))
            poblacion.append(numero_binario)
        
        return poblacion
    poblacion_generada = generar_poblacion_inicial(puntos_bits, poblacion_inicial)
    tamaño_generaciones.append(len(poblacion_generada))

    for i in range(cantidad_generaciones):
        print(f"generacion: {generaciones}")
        iteracion_gen.append(i)
        generaciones.append(i)
        print(f"------------------------------------{poblacion_generada}")
        #Se genera todas la parejas posibles
        def seleccion_parejas_posibles (poblacion_generada):
            parejas_posibles= []
            parejas_posibles = list(itertools.combinations(poblacion_generada, 2))
            return parejas_posibles
        resultado_parejas = seleccion_parejas_posibles(poblacion_generada)
        print("parejas posibles: ",resultado_parejas)

        #Posibilidad de cruza de las parejass generadas
        def posibilidad_cruza (parejas_posibles, posibilidad):
            aux_parejasPosible = []
            for parejas in parejas_posibles:
                randow_cruza = int(random.uniform(0, 1) * 100) 
                #posibilidad de cruza chequeo
                if (randow_cruza <= posibilidad):
                    aux_parejasPosible.append(parejas)
            return aux_parejasPosible
        resultado_posibilidad_cruza = posibilidad_cruza(resultado_parejas,posibilidad_de_cruza)
        print("parejas que cumplen con la posibilida: ",resultado_posibilidad_cruza)

        #Se prepara para la cruza se dividen valores
        def dividir_datos (aux_parejasPosible):
            arreglo_divisionParejas = [((parejas[0][:len(parejas[0])//2], parejas[0][len(parejas[0])//2:]), (parejas[1][:len(parejas[1])//2], parejas[1][len(parejas[1])//2:])) for parejas in aux_parejasPosible]
            return arreglo_divisionParejas
        resultado_dividir_datos = dividir_datos(resultado_posibilidad_cruza)
        print("se dividen datos para hacer la cruza",resultado_dividir_datos)

        #Resultado de la cruza(hijos)
        def medoto_punto_fijo(arreglo_divisionParejas):
            arreglo_hijos = [((hijos[0][0], hijos[1][1]), (hijos[0][1], hijos[1][0])) for hijos in arreglo_divisionParejas]
            return arreglo_hijos
        resultado_punto_fijo = medoto_punto_fijo(resultado_dividir_datos)
        print("resultado del metodo punto fijo: ",resultado_punto_fijo)

        #Se limpia el resultado de la cruza es decir ((01),(01)) queda (0101)
        def union_datos_cruza(arreglo_hijos):
            aux_hijos = []
            for aux in arreglo_hijos:
                cadena1 = aux[0][0] + aux[0][1]
                cadena2 = aux[1][0] + aux[1][1]
                aux_hijos.append(cadena1)
                aux_hijos.append(cadena2)
            return aux_hijos
        resultado_union_cruza = union_datos_cruza(resultado_punto_fijo)
        print("Resultado final de la cruza",resultado_union_cruza)

        #Posiblidad de mutacion del individuo
        def posibilidad_mutacion_individuo (aux_hijos,posibilidad):
            aux_individuo_posubilidad = []
            for individuo in aux_hijos:
                randow_individuo = int(random.uniform(0, 1) * 100) 
                if (randow_individuo <= posibilidad):
                    aux_individuo_posubilidad.append(individuo)
            return aux_individuo_posubilidad
        resultado_mutacion_individuo = posibilidad_mutacion_individuo(resultado_union_cruza, posibilidad_de_mutacion_individuo)
        print("resultado de la posibilidad del indivio",resultado_mutacion_individuo)



        #Mutacion del gen del indivio como posibilidad de mutacion del gen
        def mutacion_cambio_valor(aux_hijos,posiblidad):
            mutacion_gen = []
            for mutacion in aux_hijos:
                mutacion_nueva =''
                for caracter in mutacion:
                    randow_mutacion = int(random.uniform(0, 1) * 100) 
                    if (randow_mutacion <= posiblidad):
                        #print("caracter intacto",caracter)
                        if(caracter == '1'):
                            caracter = '0'
                        elif(caracter == '0'):
                            caracter = '1'
                        #print("caracter modificado",caracter)
                    mutacion_nueva += caracter   
                mutacion_gen.append(mutacion_nueva)
            return mutacion_gen
        resultado_mutacion_gen = mutacion_cambio_valor(resultado_mutacion_individuo, posibilidad_de_mutacion_gen)
        print("Resultado del gen por el metodo de cambio de valor",resultado_mutacion_gen)

        def Union_padres_hijos(mutacion_gen, poblacion_ini_separa):
            mutacion_gen.extend(poblacion_ini_separa)
            return mutacion_gen
        #modificar y hacer que se unan los dos arreglos y posteriormente modificar mutacion_gen por resultado_padre_hijo
        resultado_padres_hijos=Union_padres_hijos(resultado_mutacion_gen,poblacion_generada)
        print(f"esto es union papá hijo: {resultado_padres_hijos}")
        
        def cambiar_valor_a_entero(resultado_padres_hijos):
            enteros = []
            binarios_enteros = []

            for binario in resultado_padres_hijos:
                entero = int(binario, 2)
                enteros.append(entero)
                binarios_enteros.append((binario, entero))

            return binarios_enteros
        
        resultado_binario=cambiar_valor_a_entero(resultado_mutacion_gen)
        print("Conversion a enteros: ",resultado_binario)

        def Calculo_X(Calculo_DeltaX, resultado_enteros):
            for i in range(len(resultado_enteros)):
                entero = resultado_enteros[i][1]  # Accedemos al valor entero en la posición 1
                X = intervalo[0] + entero * Calculo_DeltaX
                resultado_enteros[i] = (resultado_enteros[i][0], entero, round(X, 4))

        Calculo_X(Calculo_DeltaX, resultado_binario)
        print(resultado_binario)

        def calcular_fx(Resultados_X):
            resultados_fx = []

            for elemento in Resultados_X:
                resultado = ((elemento[2]**3 * math.sin(elemento[2])))/100 + elemento[2]**2 * math.cos(elemento[2])
                resultados_fx.append(elemento + (round(resultado, 4),))

            return resultados_fx
        Resultados_fx = calcular_fx(resultado_binario)
        print(Resultados_fx)


        def encontrar_maximo(arreglo):
            if not arreglo:
                return None  # Si el arreglo está vacío, retorna None

            maximo = arreglo[0][3]
            for elemento in arreglo:
                if elemento[3] > maximo:
                    maximo = elemento[3]
            maximos.append(maximo)
            return maximos

        def encontrar_minimo(arreglo):
            if not arreglo:
                return None  # Si el arreglo está vacío, retorna None
            print(arreglo)
            minimo = arreglo[0][3]
            for elemento in arreglo:
                if elemento[3] < minimo:
                    minimo = elemento[3]
            minimos.append(minimo)
            return minimos

        def calcular_promedio(arreglo):
            if not arreglo:
                return None  # Si el arreglo está vacío, retorna None

            suma = sum(elemento[3] for elemento in arreglo)
            promedio = suma / len(arreglo)
            promedios.append(promedio)
            return promedios
        
        resultado_maximo=encontrar_maximo(Resultados_fx)
        resultado_promedio=calcular_promedio(Resultados_fx)
        resultado_minimo=encontrar_minimo(Resultados_fx)
     

        print(maximos)
        print(minimos)
        print(promedios)
        tamaño_generaciones.append(len(poblacion_generada))
        def poda_aleatoria(poblacion, limite_poblacion):
            while len(poblacion) > limite_poblacion - 1:
                # Elige aleatoriamente un individuo para eliminar
                individuo_a_eliminar = random.choice(poblacion)
                poblacion.remove(individuo_a_eliminar)

            return poblacion
        # Después de tus generaciones...
        # Suponiendo que 'resultado_padres_hijos' es tu población después de las generaciones
        Resultado_Poda = poda_aleatoria(resultado_padres_hijos, limite_poblacion)
        print("aaaaaa",Resultado_Poda)
        print(f"||||||||||||||||||||||||||||||||{len(poblacion_generada)}")
 

        def encontrar_valor_min_max_binario(indice,opcion_max_min,Resultados_fx,maximos,minimos):
            resultadoss = []
            # Bucle principal
            for dato in Resultados_fx:
                if opcion_max_min == "minimizar" and dato[3] == minimos[indice]:
                    resultadoss.append(dato[0])
                    indice += 1
                elif opcion_max_min == "maximizar" and dato[3] == maximos[indice]:
                    resultadoss.append(dato[0])
                    indice += 1

                # Verificar si se alcanzó el final de los arreglos
                if indice == len(maximos) or indice == len(minimos):
                    break

            return resultadoss
        resultado_max_min_binario = encontrar_valor_min_max_binario(i,opcion_max_min,Resultados_fx,maximos,minimos)
        print("Resultado de busqueda del binario: ", resultado_max_min_binario)

        def nueva_poblacion(resultado_max_min_binario,Resultado_Poda):
            Resultado_Poda.extend(resultado_max_min_binario)
            return Resultado_Poda
        resultado_nueva_poblacion = nueva_poblacion(resultado_max_min_binario,Resultado_Poda)
        print("LOL",resultado_nueva_poblacion)

        poblacion_generada = resultado_nueva_poblacion
    print(f"maximos aaaaaaaa {Resultados_fx}")
    graficacion_resultados(maximos, minimos, promedios,tamaño_generaciones,iteracion_gen)
    reset_variables()

def reset_variables():
        global maximos, minimos, promedios
        maximos = []
        minimos = []
        promedios = []

def graficacion_resultados(maximos, minimos, promedios,tamaño_generaciones,iteracion_gen):

        fig, axs = plt.subplots(2, 1, figsize=(10, 12))
        generaciones = range(1, cantidad_generaciones + 1)
        axs[0].plot(generaciones, maximos, label='Mejor', marker='o', linestyle='-', color='green')
        axs[0].plot(generaciones, minimos, label='Peor', marker='o', linestyle='-', color='red')
        axs[0].plot(generaciones, promedios, label='Promedio', marker='o', linestyle='-', color='orange')
        axs[0].set_title('Evolucion de la aptidud de los individuos')
        axs[0].set_xlabel('Generacion')
        axs[0].set_ylabel('Fitness')
        axs[0].legend()
        axs[0].grid(True)

        # Subplot para el incremento de la población
        generacionesP = range(1, cantidad_generaciones + 2)
        axs[1].plot(generacionesP, tamaño_generaciones, marker='o', linestyle='-', color='blue')
        axs[1].set_title('Incremento de la Población por Generacion')
        axs[1].set_xlabel('Generacion')
        axs[1].set_ylabel('Tamaño de la Poblacion')
        axs[1].grid(True)

        # Ajustar el layout y mostrar las gráficas
        plt.tight_layout()
        plt.show()
  
# Función para actualizar las variables globales con los valores ingresados por el usuario
def actualizar_variables_globales():
    global intervalo, Resolucion, poblacion_inicial, cantidad_generaciones
    global posibilidad_de_cruza, posibilidad_de_mutacion_individuo, posibilidad_de_mutacion_gen
    global limite_poblacion, opcion_max_min

    intervalo = [float(entry_intervalo_min.get()), float(entry_intervalo_max.get())]
    Resolucion = float(entry_resolucion.get())
    poblacion_inicial = int(entry_poblacion_inicial.get())
    cantidad_generaciones = int(entry_cantidad_generaciones.get())
    posibilidad_de_cruza = int(entry_posibilidad_cruza.get())
    posibilidad_de_mutacion_individuo = int(entry_posibilidad_mutacion_individuo.get())
    posibilidad_de_mutacion_gen = int(entry_posibilidad_mutacion_gen.get())
    limite_poblacion = int(entry_limite_poblacion.get())
    opcion_max_min = var_opcion_max_min.get()

# Creación de la interfaz gráfica
root = tk.Tk()
root.title("Algoritmo Genético GUI")

# Etiquetas y campos de entrada para las variables
Label(root, text="Intervalo (min):").grid(row=0, column=0)
entry_intervalo_min = Entry(root)
entry_intervalo_min.grid(row=0, column=1)

Label(root, text="Intervalo (max):").grid(row=1, column=0)
entry_intervalo_max = Entry(root)
entry_intervalo_max.grid(row=1, column=1)

Label(root, text="Resolución:").grid(row=2, column=0)
entry_resolucion = Entry(root)
entry_resolucion.grid(row=2, column=1)

Label(root, text="Población Inicial:").grid(row=3, column=0)
entry_poblacion_inicial = Entry(root)
entry_poblacion_inicial.grid(row=3, column=1)

Label(root, text="Cantidad de Generaciones:").grid(row=4, column=0)
entry_cantidad_generaciones = Entry(root)
entry_cantidad_generaciones.grid(row=4, column=1)

Label(root, text="Probabilidad de Cruza (%):").grid(row=5, column=0)
entry_posibilidad_cruza = Entry(root)
entry_posibilidad_cruza.grid(row=5, column=1)

Label(root, text="Probabilidad de Mutación Individuo (%):").grid(row=6, column=0)
entry_posibilidad_mutacion_individuo = Entry(root)
entry_posibilidad_mutacion_individuo.grid(row=6, column=1)

Label(root, text="Probabilidad de Mutación Gen (%):").grid(row=7, column=0)
entry_posibilidad_mutacion_gen = Entry(root)
entry_posibilidad_mutacion_gen.grid(row=7, column=1)

Label(root, text="Límite de Población:").grid(row=8, column=0)
entry_limite_poblacion = Entry(root)
entry_limite_poblacion.grid(row=8, column=1)

Label(root, text="Opción (maximizar/minimizar):").grid(row=9, column=0)
var_opcion_max_min = StringVar(value="maximizar")
option_menu = OptionMenu(root, var_opcion_max_min, "maximizar", "minimizar")
option_menu.grid(row=9, column=1)

# Botón para ejecutar el algoritmo genético
Button(root, text="Ejecutar Algoritmo Genético", command=lambda: [actualizar_variables_globales(), main()]).grid(row=10, column=0, columnspan=2)

# Iniciar la interfaz gráfica
root.mainloop()
