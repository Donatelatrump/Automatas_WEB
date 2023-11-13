from django.shortcuts import render
from .Funciones_py.DFAs import calcular_dfa
from .Funciones_py.DFAs import calcular_nfa
from .Funciones_py.DFAs import calcular_tm
from django.http import JsonResponse
import json



def menu(request):
    return render(request, 'menu.html')

def index(request):
    
    return render(request, 'Principal.html')

def NFA(request):
    return render(request, 'Principal_NFA.html')
def TM(request):
    return render(request, 'Principal_TM.html')




def Calcular_dfa(request):
    resultado = ""

    if request.method == 'POST':
        data = json.loads(request.body)
        estados = data.get('estados')
        conexiones = data.get('datos')
        palabra = data.get('textoEntrada')
        entrada = data.get('entrada')
        salida = data.get('salida')
        resultado = calcular_dfa(estados, conexiones, palabra, entrada, salida)
        
        if resultado:
            resultado = "La cadena es aceptada por el automata"
        else:
            resultado = "La cadena no es aceptada por el automata"

    return JsonResponse({'resultado': resultado})

def Calcular_nfa(request):
    resultado = ""

    if request.method == 'POST':
        data = json.loads(request.body)
        estados = data.get('estados')
        conexiones = data.get('datos')
        palabra = data.get('textoEntrada')
        entrada = data.get('entrada')
        salida = data.get('salida')
        resultado = calcular_nfa(estados, conexiones, palabra, entrada, salida)

        if resultado:
            resultado = "La cadena es aceptada por el automata"
        else:
            resultado = "La cadena no es aceptada por el automata"

    return JsonResponse({'resultado': resultado})

def Calcular_TM(request):
    resultado = ""

    if request.method == 'POST':
        data = json.loads(request.body)
        estados = data.get('estados')
        conexiones = data.get('datos')
        palabra = data.get('textoEntrada')
        entrada = data.get('entrada')
        salida = data.get('salida')
        resultado = calcular_tm(estados, conexiones, palabra, entrada, salida)

        if resultado:
            resultado = "La cadena es aceptada por el automata"
        else:
            resultado = "La cadena no es aceptada por el automata"

    return JsonResponse({'resultado': resultado})

