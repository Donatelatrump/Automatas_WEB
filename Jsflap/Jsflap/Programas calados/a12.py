import tkinter as tk
from tkinter import messagebox, simpledialog
from Pytomatas.dfa import DFA
from Pytomatas.nfa import NFA

contador_estados = 0
eliminar_estado = False
eliminar_conexion = False
arrastrando = False
seleccionado = None
offset_x = 0
offset_y = 0

def toggle_agregar_estado():
    global agregar_estado, agregar_conexion, eliminar_estado, eliminar_conexion
    agregar_estado = not agregar_estado
    agregar_conexion = False
    eliminar_estado = False
    eliminar_conexion = False
    check_agregar_estado.select()
    check_agregar_conexion.deselect()
    check_eliminar_estado.deselect()
    check_eliminar_conexion.deselect()

def toggle_agregar_conexion():
    global agregar_conexion, agregar_estado, eliminar_conexion, eliminar_estado
    agregar_conexion = not agregar_conexion
    agregar_estado = False
    eliminar_conexion = False
    eliminar_estado = False
    check_agregar_conexion.select()
    check_agregar_estado.deselect()
    check_eliminar_conexion.deselect()
    check_eliminar_estado.deselect()

def toggle_eliminar_estado():
    global eliminar_estado, agregar_estado, eliminar_conexion, agregar_conexion
    eliminar_estado = not eliminar_estado
    agregar_estado = False
    eliminar_conexion = False
    agregar_conexion = False
    check_eliminar_estado.select()
    check_agregar_estado.deselect()
    check_eliminar_conexion.deselect()
    check_agregar_conexion.deselect()

def toggle_eliminar_conexion():
    global eliminar_conexion, agregar_estado, eliminar_estado, agregar_conexion
    eliminar_conexion = not eliminar_conexion
    agregar_estado = False
    eliminar_estado = False
    agregar_conexion = False
    check_eliminar_conexion.select()
    check_agregar_estado.deselect()
    check_eliminar_estado.deselect()
    check_agregar_conexion.deselect()

def dibujar_estado(event):
    global contador_estados
    if agregar_estado:
        global contador_estados
        estado = f"q{contador_estados}"
        contador_estados += 1
        canvas.create_oval(event.x-20, event.y-20, event.x+20, event.y+20, fill="white", outline="black")
        canvas.create_text(event.x, event.y, text=estado)
        estados.append({"nombre": estado, "x": event.x, "y": event.y})
        estados_dict[estado] = {"x": event.x, "y": event.y}

def iniciar_arrastre(event):
    global arrastrando, seleccionado, offset_x, offset_y
    if not (agregar_estado or agregar_conexion or eliminar_estado or eliminar_conexion):
        for estado in estados:
            centro_x = estado["x"]
            centro_y = estado["y"]
            radio = 20
            distancia = ((event.x - centro_x)**2 + (event.y - centro_y)**2)**0.5
            if distancia <= radio:
                arrastrando = True
                seleccionado = estado
                offset_x = event.x - centro_x
                offset_y = event.y - centro_y

def mover_estado(event):
    if arrastrando and seleccionado:
        estados_dict[seleccionado["nombre"]]["x"] = event.x - offset_x
        estados_dict[seleccionado["nombre"]]["y"] = event.y - offset_y
        redraw_canvas()

def finalizar_arrastre(event):
    global arrastrando
    arrastrando = False

def dibujar_conexion(event):
    global primer_estado, segundo_estado
    if agregar_conexion:
        if not eliminar_conexion:
            for estado in estados:
                centro_x = estado["x"]
                centro_y = estado["y"]
                radio = 20
                distancia = ((event.x - centro_x)**2 + (event.y - centro_y)**2)**0.5
                if distancia <= radio:
                    if primer_estado is None:
                        primer_estado = estado
                        break
                    elif segundo_estado is None and estado != primer_estado:
                        segundo_estado = estado
                        caracter = simpledialog.askstring("Agregar Caracter", "Caracter:")
                        if(caracter == ""):
                            caracter = 'a'
                        if caracter:
                            conexiones.append((primer_estado["nombre"], segundo_estado["nombre"], caracter))
                            primer_estado = None
                            segundo_estado = None
                            redraw_canvas()
                            break
        else:
            for conexion in conexiones:
                punto_medio_x = (estados_dict[conexion[0]]["x"] + estados_dict[conexion[1]]["x"]) / 2
                punto_medio_y = (estados_dict[conexion[0]]["y"] + estados_dict[conexion[1]]["y"]) / 2
                distancia = ((event.x - punto_medio_x)**2 + (event.y - punto_medio_y)**2)**0.5
                if distancia <= 10:
                    mensaje = "¿Estás seguro de que deseas eliminar esta conexión?"
                    respuesta = messagebox.askyesno("Eliminar Conexión", mensaje)
                    if respuesta:
                        conexiones.remove(conexion)
                        redraw_canvas()
                    break
    else:
        messagebox.showwarning("Agregar Conexión", "Primero selecciona 'Agregar Conexión' antes de crear una conexión.")

    # Eliminar estado
    if eliminar_estado or eliminar_conexion:
        detectar_clic(event)

    # Eliminar conexión
    elif eliminar_conexion:
        detectar_clic(event)

def detectar_clic(event):
    global seleccionado
    if eliminar_estado or eliminar_conexion:
        for estado in estados:
            centro_x = estado["x"]
            centro_y = estado["y"]
            radio = 20
            distancia = ((event.x - centro_x)**2 + (event.y - centro_y)**2)**0.5
            if distancia <= radio:
                seleccionado = estado
                break
        if seleccionado:
            if eliminar_estado:
                mensaje = "¿Estás seguro de que deseas eliminar este estado?"
                respuesta = messagebox.askyesno("Eliminar Estado", mensaje)
                if respuesta:
                    estados.remove(seleccionado)
                    del estados_dict[seleccionado["nombre"]]  # Eliminar estado de estados_dict
                    contador_estados = max([int(estado["nombre"][1:]) for estado in estados]) + 1  # Actualizar contador
                    redraw_canvas()
            elif eliminar_conexion:
                mensaje = "¿Estás seguro de que deseas eliminar esta conexión?"
                respuesta = messagebox.askyesno("Eliminar Conexión", mensaje)
                if respuesta:
                    conexiones_temp = conexiones.copy()
                    for conexion in conexiones_temp:
                        if seleccionado["nombre"] == conexion[0] or seleccionado["nombre"] == conexion[1]:
                            conexiones.remove(conexion)
                    redraw_canvas()

def redraw_canvas():
    canvas.delete("all")
    for estado in estados:
        canvas.create_oval(estado["x"]-20, estado["y"]-20, estado["x"]+20, estado["y"]+20, fill="white", outline="black")
        canvas.create_text(estado["x"], estado["y"], text=estado["nombre"])
    for conexion in conexiones:
        x_medio = (estados_dict[conexion[0]]["x"] + estados_dict[conexion[1]]["x"]) / 2
        y_medio = (estados_dict[conexion[0]]["y"] + estados_dict[conexion[1]]["y"]) / 2
        canvas.create_line(estados_dict[conexion[0]]["x"], estados_dict[conexion[0]]["y"], estados_dict[conexion[1]]["x"], estados_dict[conexion[1]]["y"], arrow=tk.LAST)
        canvas.create_text(x_medio, y_medio, text=conexion[2], font=("Arial", 10, "bold"))

def generar_y_configurar_dfa():
    global my_dfa
    my_dfa = DFA()

    # Define to "my_dfa" a set of states names:
    estados_set = set()
    for estado in estados:
        estados_set.add(estado["nombre"])
    my_dfa.setStates(estados_set)

    # Define to "my_dfa" a set of states characters of the alphabet:
    alfabeto_set = set()
    for conexion in conexiones:
        alfabeto_set.add(conexion[2])
    my_dfa.setAlphabet(alfabeto_set)

    # Set the "Initial state" name of "my_dfa":
    my_dfa.setInitial(estados[0]["nombre"])

    # Define to "my_dfa" the set of "Final states" names:
    finales_set = set()
    for estado in estados:
        if estado["nombre"].startswith("q"):
            finales_set.add(estado["nombre"])
    if finales_set:
        max_final_state = max(finales_set, key=lambda x: int(x[1:]))
        my_dfa.setFinals({max_final_state})

    # Add transitions to the DFA:
    for conexion in conexiones:
        inicio = conexion[0]
        caracter = conexion[2]
        fin = conexion[1]
        my_dfa.addTransition((inicio, caracter, fin))

    # Imprimir información del DFA
    my_dfa.show()

def mostrar_informacion():
    if seleccionado:
        messagebox.showinfo("Información del Estado", f"Nombre: {seleccionado['nombre']}\nPosición: ({seleccionado['x']}, {seleccionado['y']})")
    else:
        messagebox.showinfo("Información del Estado", "Ningún estado seleccionado")

def probar_cadena():
    if not my_dfa:
        messagebox.showinfo("Error", "Primero debes generar y configurar el DFA.")
        return

    word = entrada.get()
    aceptado = my_dfa.accepts(word)
    messagebox.showinfo("Resultado", f"¿La cadena '{word}' es aceptada? {aceptado}")

# Crear la ventana de la interfaz
root = tk.Tk()
root.title("Interfaz DFA")
root.geometry("800x600")  # Cambiamos el tamaño de la ventana

# Variables
agregar_estado = False
agregar_conexion = False
estados = []
conexiones = []
primer_estado = None
segundo_estado = None
estados_dict = {}

# Checkbuttons
check_agregar_estado = tk.Checkbutton(root, text="Agregar Estado", command=toggle_agregar_estado)
check_agregar_estado.pack()

check_agregar_conexion = tk.Checkbutton(root, text="Agregar Conexion", command=toggle_agregar_conexion)
check_agregar_conexion.pack()

check_eliminar_estado = tk.Checkbutton(root, text="Eliminar Estado", command=toggle_eliminar_estado)
check_eliminar_estado.pack()

check_eliminar_conexion = tk.Checkbutton(root, text="Eliminar Conexion", command=toggle_eliminar_conexion)
check_eliminar_conexion.pack()

# Canvas para dibujar estados y conexiones
canvas = tk.Canvas(root, bg="white", width=700, height=300)
canvas.pack()
canvas.bind("<Button-1>", dibujar_estado)
canvas.bind("<Button-2>", detectar_clic)  # Botón central para detectar clic
canvas.bind("<Button-3>", dibujar_conexion)  # Usamos el botón derecho para dibujar conexiones
canvas.bind("<B1-Motion>", mover_estado)  # Arrastrar estado

# Etiqueta y campo de entrada para la cadena
etiqueta = tk.Label(root, text="Cadena:")
etiqueta.pack()

entrada = tk.Entry(root)
entrada.pack()

# Botón para generar y configurar el DFA
boton_generar_dfa = tk.Button(root, text="Generar y Configurar DFA", command=generar_y_configurar_dfa)
boton_generar_dfa.pack()

# Botón para mostrar información del estado seleccionado
boton_mostrar_info = tk.Button(root, text="Mostrar Información del Estado", command=mostrar_informacion)
boton_mostrar_info.pack()

# Botón para probar cadena
boton_probar_cadena = tk.Button(root, text="Probar Cadena", command=probar_cadena)
boton_probar_cadena.pack()

# Iniciar el bucle de la interfaz
root.mainloop()
