import flet as ft
import numpy as np
import matplotlib.pyplot as plt
from pulp import LpVariable, LpMaximize, LpProblem
from scipy.optimize import linprog
from itertools import combinations

def main(page: ft.Page):
    page.title = "Programacion lineal UD"
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    
    #Definir elementos de la aplicacion - Primera parte
    texto_metodo = ft.Text("Metodo")
    input_pregunta = ft.Dropdown(
        width=200,
        options = [ ft.dropdown.Option("Simplex"), ft.dropdown.Option("Grafico") ],
        value="Grafico",
    )
    texto_variables = ft.Text("¿Cuántas variables de decisión tiene el problema?")
    input_variables = ft.TextField(width=200, label="Inserte un numero")
    texto_restricciones = ft.Text("¿Cuantas restricciones?")
    input_restricciones = ft.TextField(width=200, label="Inserte un numero")
    boton_continuar = ft.ElevatedButton("Continuar")

    #Definir elementos de la aplicacion - Segunda parte
    texto_objetivo = ft.Text("¿Cual es el objetivo de la funcion?")
    input_objetivo = ft.Dropdown(
        width=200,
        options = [
            ft.dropdown.Option("Maximizar"),
            ft.dropdown.Option("Minimizar"),            
        ],
        value="Maximizar",
    )
    texto_funcion = ft.Text("Funcion : ")
    input_x1 = ft.TextField(width=100, height=20)
    texto_funcion2 = ft.Text(" X1 + ")
    input_x2 = ft.TextField(width=100, height=20)
    texto_funcion3 = ft.Text(" X2")

    # Listas para almacenar los datos ingresados
    restricciones = []
    equivalencias_restriccion = []
    resultados_restriccion = []

    # Listas para almacenar controles de entrada
    controles_const_x1 = []
    controles_const_x2 = []
    controles_equivalencia = []
    controles_z = []

    def continuar(e):
        metodo = input_pregunta.value
        variables = int(input_variables.value)
        restricciones_num = int(input_restricciones.value)

        # Deshabilitar los campos de entrada y el dropdown
        input_pregunta.disabled = True
        input_variables.disabled = True
        input_restricciones.disabled = True
        boton_continuar.disabled = True

        if (metodo == "Grafico") :
            page.add(
                ft.Row(
                    controls=[ ft.Text("Metodo " + metodo, style="headlineMedium") ]
                ),
                ft.Row(
                    controls=[ texto_objetivo, input_objetivo ]
                ),
                ft.Row(
                    controls=[ texto_funcion, input_x1, texto_funcion2, input_x2, texto_funcion3]
                )
            )

            for i in range(restricciones_num):
                # Preguntas para cada restricción
                input_const_x1 = ft.TextField(width=40, height=20)
                input_const_x2 = ft.TextField(width=40, height=20)
                input_equivalencia = ft.Dropdown(
                    width=100,
                    options=[
                        ft.dropdown.Option("<="),
                        ft.dropdown.Option(">="),
                        ft.dropdown.Option("="),
                    ],
                    value= "<=",
                )
                input_z = ft.TextField(width=40, height=20)

                # Añadir controles a las listas
                controles_const_x1.append(input_const_x1)
                controles_const_x2.append(input_const_x2)
                controles_equivalencia.append(input_equivalencia)
                controles_z.append(input_z)

                page.add(
                    ft.Row(
                        controls = [ ft.Text(f"Restricción {i + 1} : "), input_const_x1, ft.Text(" X1 + "), input_const_x2, ft.Text(" X2"), input_equivalencia,  ft.Text(" "), input_z ]
                    )
                )

            boton_guardar_datos = ft.ElevatedButton("Guardar datos", on_click=guardar_datos)
            page.add(ft.Row(controls=[boton_guardar_datos]))

        else :
            page.add(
                ft.Row(
                    controls=[ ft.Text("Metodo " + metodo, style="headlineMedium")]
                )
            )

        # Actualizar la página para reflejar los cambios
        page.update()

    def guardar_datos(e):
        # Guardar datos ingresados de las restricciones en las listas
        restricciones.clear()
        equivalencias_restriccion.clear()
        resultados_restriccion.clear()
        
        for i in range(len(controles_const_x1)):
            coeficiente_x1 = float(controles_const_x1[i].value)
            coeficiente_x2 = float(controles_const_x2[i].value)
            equivalencia = controles_equivalencia[i].value
            resultado = float(controles_z[i].value)

            restricciones.append([coeficiente_x1, coeficiente_x2])
            equivalencias_restriccion.append(equivalencia)
            resultados_restriccion.append(resultado)

        print("Datos guardados:")
        print("Restricciones:", restricciones)
        print("Equivalencias:", equivalencias_restriccion)
        print("Resultados:", resultados_restriccion)

        restricciones_numpy = np.array(restricciones)
        equivalencias_restriccion_numpy = np.array(equivalencias_restriccion)
        resultados_restriccion_numpy = np.array(resultados_restriccion)

        restricciones_pulp = []
        x1 = LpVariable("x1",lowBound=0)
        x2 = LpVariable("x2",lowBound=0)

        def iniciar_problema():
            # Crear un nuevo problema de optimización
            problem = LpProblem("MiProblema", LpMaximize)
            return problem

        problem = iniciar_problema()
        problem += 22*x1 + 45*x2
        # Itera sobre cada restricción
        for i in range(int(input_restricciones.value)):
            # Obtiene los coeficientes, equivalencias y resultados de la restricción actual
            coeficiente_x1 = restricciones[i][0]
            coeficiente_x2 = restricciones[i][1]
            equivalencia = equivalencias_restriccion[i]
            resultado = resultados_restriccion[i]

            # Crear la restricción en formato PuLP
            restriccion_pulp = coeficiente_x1 * x1 + coeficiente_x2 * x2

            # Agregar la restricción al problema según el tipo de equivalencia
            if equivalencia == '<=':
                problem += restriccion_pulp <= resultado
            elif equivalencia == '>=':
                problem += restriccion_pulp >= resultado
            elif equivalencia == '=':
                problem += restriccion_pulp == resultado

        print(problem)
        problem.solve()
        print("El optimo se obtiene con x1 siendo ", x1.varValue," y x2 siendo igual a ",x2.varValue)

        #Continuar con los resultados
        page.add(
            ft.Row(
                controls = [ ft.Text("Resultado", style="headlineMedium") ]
            ),
            ft.Row(
                controls = [ ft.Text("El optimo se obtiene con x1 siendo " + str(x1.varValue) + "\n y x2 siendo igual a " + str(x2.varValue), style="headlineMedium") ]
            )
        )
        page.update()
    
    # Configurar eventos
    boton_continuar.on_click = continuar

    #Vista de la tabla
    page.add(
        ft.Row(
            controls=[
                ft.Text("Solucionador Programacion Lineal", style="headlineMedium"), 
            ]
        ),
        ft.Row(
            controls=[
                texto_metodo,
                input_pregunta,
            ]
        ),
        ft.Row(
            controls=[
                texto_variables,
                input_variables,
            ]
        ),
        ft.Row(
            controls=[
                texto_restricciones,
                input_restricciones,
            ]
        ),
        ft.Row(
            controls=[
                boton_continuar,
            ]
        ),
    )
    
ft.app(target=main)
