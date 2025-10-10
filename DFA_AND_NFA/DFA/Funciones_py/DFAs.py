from Pytomatas.dfa import DFA
from Pytomatas.nfa import NFA
from Pytomatas.tm import TM
from Pytomatas.pda import PDA


def calcular_dfa(estados, conexiones, palabra, inicio2, fin2):
    my_dfa = DFA()

    # Define to "my_dfa" a set of states names:
    estados_set = set()
    for estado in estados:
        estados_set.add(estado["nombre"])
    my_dfa.setStates(estados_set)

    # Define to "my_dfa" a set of states characters of the alphabet:
    alfabeto_set = set()
    for conexion in conexiones:
        simbolos = conexion[1].split(',')
        for simbolo in simbolos:
            alfabeto_set.add(simbolo.strip())
 
    my_dfa.setAlphabet(alfabeto_set)

    # Set the "Initial state" name of "my_dfa":
    my_dfa.setInitial(inicio2[0])
    my_dfa.setFinals(fin2)
    # Add transitions to the DFA:
    for conexion in conexiones:
        inicio = conexion[0]
        caracter = conexion[1]
        fin = conexion[2]

        if ',' in caracter:  # Si hay comas en el caracter
            simbolos = caracter.split(',')
            for simbolo in simbolos:
                my_dfa.addTransition((inicio, simbolo.strip(), fin))
        else:
            my_dfa.addTransition((inicio, caracter, fin))
    # Check if the DFA accepts the string "cadena":
    print(my_dfa.show())
    print(my_dfa.accepts(palabra))
    return my_dfa.accepts(palabra)



def calcular_nfa(estados, conexiones, palabra, inicios, finales):
    # Crea una instancia de NFA
    my_nfa = NFA()

    # Define los estados del NFA
    estados_set = set()
    for estado in estados:
        estados_set.add(estado["nombre"])
    my_nfa.setStates(estados_set)

    # Define el alfabeto del NFA
    alfabeto_set = set()
    for conexion in conexiones:
        simbolos = conexion[1].split(',')
        for simbolo in simbolos:
            alfabeto_set.add(simbolo.strip())

    my_nfa.setAlphabet(alfabeto_set)

    # Establece los estados iniciales y finales
    my_nfa.setInitial(inicios[0])
    my_nfa.setFinals(finales)

    # Agrega transiciones al NFA
    for conexion in conexiones:
        inicio = conexion[0]
        caracter = conexion[1]
        fin = conexion[2]

        if ',' in caracter:  # Si hay comas en el caracter
            simbolos = caracter.split(',')
            for simbolo in simbolos:
                my_nfa.addTransition((inicio, simbolo.strip(), fin))
        else:
            my_nfa.addTransition((inicio, caracter, fin))
    # Verifica si el NFA acepta la cadena
    print(my_nfa.show())
    print(my_nfa.accepts(palabra))
    return my_nfa.accepts(palabra)


def calcular_tm(estados, conexiones, palabra, inicios, finales):
    
    # Define los estados del TM
    
    estados_set = set()
    for estado in estados:
        estados_set.add(estado["nombre"])
    

    # Define el alfabeto del TM a partir de las conexiones
    # Define el alfabeto del NFA
    alfabeto_set = set()
    for conexion in conexiones:
        if isinstance(conexion[1], list):
            alfabeto_set.update(set(conexion[1]))
        else:
            alfabeto_set.add(conexion[1])

    alfabeto = normalizar(alfabeto_set)
    
    # Define las transiciones
    transiciones = []
    for conexion in conexiones:
        inicio = conexion[0]
        simbolos = conexion[1]
        fin = conexion[2]

        if isinstance(simbolos, list):
            for simbolo in simbolos:
                transiciones.append((inicio, simbolo, fin))
        else:
            transiciones.append((inicio, simbolos, fin))

    trans = normalizar_dos(transiciones)

    my_tm = TM(estados_set,alfabeto,trans,inicios[0],finales)
    my_tm.show()
    

    return my_tm.accepts(palabra,stepByStep=True)


def normalizar(simbolos_set):
    simbolos_normalizados = set()

    for simbolo in simbolos_set:
        simbolos = simbolo.split(',')
        simbolos_normalizados.update(simbolos)

    return simbolos_normalizados

def normalizar_dos(transiciones):
    transiciones_normalizadas = []
    for transicion in transiciones:
        inicio, simbolos, fin = transicion
        simbolos_lista = simbolos.split(',')
        transicion_normalizada = (inicio,) + tuple(simbolos_lista) + (fin,)
        transiciones_normalizadas.append(transicion_normalizada)
    return transiciones_normalizadas
