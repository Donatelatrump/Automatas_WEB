from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name = 'Menu'),
    path('DFA/', views.index, name='index'),
    path('NFA/', views.NFA, name= "NFA"),
    path('MT/', views.TM, name= "TM"),
    path('calcular/', views.Calcular_dfa, name='calcular_dfa'),
    path('nfa/', views.Calcular_nfa, name='calcular_nfa'),
    path('tm/', views.Calcular_TM, name='calcular_tm'),
   path('AFND/', views.AFND, name='AFND'),           # GET → renderiza página
    path('AFN/', views.AFN, name='AFN'),              # GET → renderiza página
    path('procesar_afnd/', views.procesar_afnd, name='procesar_afnd'),  # POST
    path('procesar_afn/', views.procesar_afn, name='procesar_afn'),     # POST
   
]