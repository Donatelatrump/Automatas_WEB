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
   
]