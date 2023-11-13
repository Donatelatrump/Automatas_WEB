import tkinter as tk
from tkinter import messagebox, simpledialog
from Pytomatas.dfa import DFA

numeros_disponibles = list(range(100))
nombres_disponibles = set([f"q{i}" for i in range(100)])  # Lista de nombres disponibles para estados
contador_estados = 0
eliminar_estado = False
eliminar_conexion = False

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
        estados_dict[estado] = {"x": event.x, "y": event.y}  # Agregar estado a estados_dict

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

    # Eliminar estado
    elif eliminar_estado or eliminar_conexion:
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
            mensaje = "¿Estás seguro de que deseas eliminar este estado?"
            respuesta = messagebox.askyesno("Eliminar Estado", mensaje)
            if respuesta:
                if eliminar_estado:
                    estados.remove(seleccionado)
                elif eliminar_conexion:
                    conexiones_temp = conexiones.copy()
                    for conexion in conexiones_temp:
                        if seleccionado["nombre"] == conexion[0] or seleccionado["nombre"] == conexion[1]:
                            conexiones.remove(conexion)
                    # Actualizar el contador de estados
                    global contador_estados
                    contador_estados = max([int(estado["nombre"][1:]) for estado in estados]) + 1
                redraw_canvas()

def generar_y_configurar_dfa():
    global my_dfa
    my_dfa = DFA()

    estados_set = set()
    max_numero_estado = -1

    for estado in estados:
        estados_set.add(estado["nombre"])
        numero_estado = int(estado["nombre"][1:])
        if numero_estado > max_numero_estado:
            max_numero_estado = numero_estado

    my_dfa.setStates(estados_set)
    
    alfabeto_set = set()
    for conexion in conexiones:
        alfabeto_set.add(conexion[2])
    my_dfa.setAlphabet(alfabeto_set)

    my_dfa.setInitial("q0")

    finales_set = set()
    finales_set.add(f"q{max_numero_estado}")
    my_dfa.setFinals(finales_set)

    for conexion in conexiones:
        inicio = conexion[0]
        caracter = conexion[2]
        fin = conexion[1]
        my_dfa.addTransition((inicio, caracter, fin))

    my_dfa.show()

def mostrar_informacion():
    if seleccionado:
        messagebox.showinfo("Información del Estado", f"Nombre: {seleccionado['nombre']}\nPosición: ({seleccionado['x']}, {seleccionado['y']})")
    else:
        messagebox.showinfo("Información del Estado", "Ningún estado seleccionado")

def probar_cadena():
    if my_dfa:
        word = entrada.get()
        aceptado = my_dfa.accepts(word)
        messagebox.showinfo("Resultado", f"¿La cadena '{word}' es aceptada? {aceptado}")
    else:
        messagebox.showwarning("DFA no configurado", "Primero configura el DFA antes de probar una cadena.")

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

root = tk.Tk()
root.title("Interfaz DFA")
root.geometry("800x600")

agregar_estado = False
agregar_conexion = False
estados = []
conexiones = []
primer_estado = None
segundo_estado = None
seleccionado = None
estados_dict = {}

check_agregar_estado = tk.Checkbutton(root, text="Agregar Estado", command=toggle_agregar_estado)
check_agregar_estado.pack()

check_agregar_conexion = tk.Checkbutton(root, text="Agregar Conexion", command=toggle_agregar_conexion)
check_agregar_conexion.pack()

check_eliminar_estado = tk.Checkbutton(root, text="Eliminar Estado", command=toggle_eliminar_estado)
check_eliminar_estado.pack()

check_eliminar_conexion = tk.Checkbutton(root, text="Eliminar Conexion", command=toggle_eliminar_conexion)
check_eliminar_conexion.pack()

canvas = tk.Canvas(root, bg="white", width=800, height=600)
canvas.pack()
canvas.bind("<Button-1>", dibujar_estado)
canvas.bind("<Button-2>", detectar_clic)
canvas.bind("<Button-3>", dibujar_conexion)

etiqueta = tk.Label(root, text="Cadena:")
etiqueta.pack()

entrada = tk.Entry(root)
entrada.pack()

boton_generar_dfa = tk.Button(root, text="Generar y Configurar DFA", command=generar_y_configurar_dfa)
boton_generar_dfa.pack()

boton_mostrar_info = tk.Button(root, text="Mostrar Información del Estado", command=mostrar_informacion)
boton_mostrar_info.pack()

boton_probar_cadena = tk.Button(root, text="Probar Cadena", command=probar_cadena)
boton_probar_cadena.pack()

root.mainloop()
