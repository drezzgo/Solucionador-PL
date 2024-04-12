import flet as ft

def main(page: ft.Page):
    page.title = "Programacion lineal UD"
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0

    texto_metodo = ft.Text("Metodo")
    input_pregunta = ft.Dropdown(
        width=200,
        options = [
            ft.dropdown.Option("Simplex"),
            ft.dropdown.Option("Grafico"),            
        ],
    )
    texto_variables = ft.Text("¿Cuántas variables de decisión tiene el problema?")
    input_variables = ft.TextField(width=200, label="Inserte un numero")
    texto_restricciones = ft.Text("¿Cuantas restricciones?")
    input_restricciones = ft.TextField(width=200, label="Inserte un numero")

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
        ),
    )

    ##contenedor = ft.Container(col, width = 720, height = 1280, alignment = ft.alignment.top_center )
    ##page.add(contenedor)

ft.app(target=main)
