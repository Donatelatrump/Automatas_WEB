from Pytomatas.dfa import DFA
from Pytomatas.nfa import NFA

def calcular_dfa(estados, conexiones, palabra, inicio, finales, mostrar_pasos=False):
    """
    Procesa un DFA usando Pyomatas.
    
    estados: lista de dicts {"nombre": "q0"}
    conexiones: lista de tuplas (inicio, simbolo, fin)
    palabra: string a evaluar
    inicio: string con nombre del estado inicial
    finales: lista de strings con estados finales
    mostrar_pasos: bool, si True imprime paso a paso
    """
    my_dfa = DFA()

    # Set de estados
    my_dfa.setStates({e["nombre"] for e in estados})

    # Set del alfabeto
    alfabeto = set()
    for t in conexiones:
        simbolos = t[1].split(',')  # Permite múltiples símbolos separados por coma
        for s in simbolos:
            alfabeto.add(s.strip())
    my_dfa.setAlphabet(alfabeto)

    # Inicial y finales
    my_dfa.setInitial(inicio)
    my_dfa.setFinals(set(finales))

    # Transiciones
    for t in conexiones:
        inicio_t, simbolo_t, fin_t = t
        if ',' in simbolo_t:
            for s in simbolo_t.split(','):
                my_dfa.addTransition((inicio_t, s.strip(), fin_t))
        else:
            my_dfa.addTransition((inicio_t, simbolo_t, fin_t))

    # Mostrar info del DFA
    my_dfa.show()

    # Evaluar palabra
    return my_dfa.accepts(palabra, stepByStep=mostrar_pasos)


def calcular_afnd(estados, conexiones, palabra, inicios, finales, mostrar_pasos=False):
    """
    Procesa un AFND o AFN-ε usando Pyomatas.
    
    estados: lista de dicts {"nombre": "q0"}
    conexiones: lista de tuplas (inicio, simbolo, fin) 
                símbolo puede ser 'ε'
    palabra: string a evaluar
    inicios: lista de strings con estados iniciales
    finales: lista de strings con estados finales
    mostrar_pasos: bool, si True imprime paso a paso
    """
    my_nfa = NFA()

    # Set de estados
    my_nfa.setStates({e["nombre"] for e in estados})

    # Set del alfabeto (excluye ε)
    alfabeto = set()
    for t in conexiones:
        simbolos = t[1].split(',')
        for s in simbolos:
            s = s.strip()
            if s != 'ε':
                alfabeto.add(s)
    my_nfa.setAlphabet(alfabeto)

    # Inicial y finales
    # Pyomatas NFA acepta un solo estado inicial, si hay varios, tomamos el primero
    my_nfa.setInitial(inicios[0])
    my_nfa.setFinals(set(finales))

    # Transiciones
    for t in conexiones:
        inicio_t, simbolo_t, fin_t = t
        simbolos = simbolo_t.split(',')
        for s in simbolos:
            my_nfa.addTransition((inicio_t, s.strip(), fin_t))

    # Mostrar info del NFA
    my_nfa.show()

    # Evaluar palabra
    return my_nfa.accepts(palabra, stepByStep=mostrar_pasos)
def calcular_afn(estados, conexiones, palabra, inicios, finales, mostrar_pasos=False):
    """
    Procesa un AFN (con ε-transiciones) usando Pyomatas.

    estados: lista de dicts {"nombre": "q0"}
    conexiones: lista de tuplas (inicio, simbolo, fin) donde símbolo puede ser 'ε'
    palabra: string a evaluar
    inicios: lista de strings con estados iniciales
    finales: lista de strings con estados finales
    mostrar_pasos: bool, si True imprime paso a paso
    """
    my_nfa = NFA()

    # Definir estados
    my_nfa.setStates({e["nombre"] for e in estados})

    # Definir alfabeto (excluyendo ε)
    alfabeto = {s.strip() for _, simbolo, _ in conexiones for s in simbolo.split(',') if s.strip() != 'ε'}
    my_nfa.setAlphabet(alfabeto)

    # Estado inicial: Pyomatas NFA acepta solo uno, tomamos el primero si hay varios
    my_nfa.setInitial(inicios[0])
    my_nfa.setFinals(set(finales))

    # Agregar transiciones
    for inicio_t, simbolo_t, fin_t in conexiones:
        for s in simbolo_t.split(','):
            my_nfa.addTransition((inicio_t, s.strip(), fin_t))

    # Mostrar información del AFN
    my_nfa.show()

    # Evaluar la palabra
    return my_nfa.accepts(palabra, stepByStep=mostrar_pasos)