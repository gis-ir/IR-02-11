import customtkinter as ctk
from datos_tartas import tartas, stock

def calcular_tarta():
    nombre_tarta = entry_tarta.get().lower()
    try:
        unidades = int(entry_unidades.get())
    except ValueError:
        output_text.set("Por favor, introduce un número válido de unidades.")
        return

    if nombre_tarta not in tartas:
        output_text.set(f"La tarta '{nombre_tarta}' no está disponible.")
        return
    
    receta = tartas[nombre_tarta]
    stock_temporal = {
        'semielaborados': stock['semielaborados'].copy(),
        'materias_primas': stock['materias_primas'].copy()
    }
    
    # Inicializar diccionarios para tracking
    a_preparar = {}
    a_comprar = {}
    consumidos = {'semielaborados': {}, 'materias_primas': {}}

    # Procesar semielaborados
    for semi, datos in receta['semielaborados'].items():
        cantidad_necesaria = datos['cantidad'] * unidades
        if stock_temporal['semielaborados'][semi] >= cantidad_necesaria:
            consumidos['semielaborados'][semi] = cantidad_necesaria
            stock_temporal['semielaborados'][semi] -= cantidad_necesaria
        else:
            # Si no hay suficiente stock del semielaborado
            if 'materias_primas' in datos:
                a_preparar[semi] = {
                    'cantidad': cantidad_necesaria - stock_temporal['semielaborados'][semi],
                    'materias_primas': {}
                }
                # Calcular materias primas necesarias para el semielaborado
                for mp, cant in datos['materias_primas'].items():
                    cant_total = cant * (cantidad_necesaria - stock_temporal['semielaborados'][semi])
                    a_preparar[semi]['materias_primas'][mp] = cant_total
            consumidos['semielaborados'][semi] = stock_temporal['semielaborados'][semi]
            stock_temporal['semielaborados'][semi] = 0

    # Procesar materias primas directas
    for mp, cantidad in receta['materias_primas'].items():
        cantidad_necesaria = cantidad * unidades
        if stock_temporal['materias_primas'][mp] >= cantidad_necesaria:
            consumidos['materias_primas'][mp] = cantidad_necesaria
            stock_temporal['materias_primas'][mp] -= cantidad_necesaria
        else:
            a_comprar[mp] = cantidad_necesaria - stock_temporal['materias_primas'][mp]
            consumidos['materias_primas'][mp] = stock_temporal['materias_primas'][mp]
            stock_temporal['materias_primas'][mp] = 0

    # Generar salida
    salida = "Consumido\n\n"
    
    # Sección Semielaborados
    salida += "Semielaborados:\n"
    if a_preparar:
        salida += "Preparar:\n"
        for semi, info in a_preparar.items():
            salida += f"{semi}:\n"
            for mp, cant in info['materias_primas'].items():
                salida += f"  {mp}: {cant} gramos\n"

    # Sección Materias Primas
    if a_comprar:
        salida += "\nMaterias primas:\n"
        salida += "Comprar:\n"
        for mp, cant in a_comprar.items():
            salida += f"{mp}: {cant}\n"

    # Stock restante
    salida += "\nStock restante\n"
    salida += "Semielaborados:\n"
    for semi, cantidad in stock_temporal['semielaborados'].items():
        salida += f"{semi}: {cantidad}\n"

    salida += "\nMaterias primas:\n"
    for mp, cantidad in stock_temporal['materias_primas'].items():
        salida += f"{mp}: {cantidad}\n"

    output_text.set(salida)

# Configuración de la interfaz
app = ctk.CTk()
app.title("Gestión de Tartas")

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20)

# Entradas
label_tarta = ctk.CTkLabel(frame, text="Introduzca el nombre de la tarta")
label_tarta.grid(row=0, column=0, padx=10, pady=10)
entry_tarta = ctk.CTkEntry(frame)
entry_tarta.grid(row=0, column=1, padx=10, pady=10)

label_unidades = ctk.CTkLabel(frame, text="Cantidad a producir")
label_unidades.grid(row=1, column=0, padx=10, pady=10)
entry_unidades = ctk.CTkEntry(frame)
entry_unidades.grid(row=1, column=1, padx=10, pady=10)

# Botón calcular
btn_calcular = ctk.CTkButton(frame, text="Calcular", command=calcular_tarta)
btn_calcular.grid(row=2, column=0, columnspan=2, pady=10)

# Salida
output_text = ctk.StringVar()
output_label = ctk.CTkLabel(app, textvariable=output_text, justify='left')
output_label.pack(pady=20)

app.mainloop()