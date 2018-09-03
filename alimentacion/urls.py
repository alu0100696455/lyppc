from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stigler/', views.stigler, name='stigler'),
    path('stigler/muestreo_<int:muestreo>/', views.stigler, name='stigler'),
    path('stigler/muestreo_<int:muestreo>/repeticiones_<int:repeticiones>', views.stigler, name='stigler'),
    path('knapsack_multidimensional', views.knapsack_multidimensional, name='knapsack_multidimensional'),
    path('knapsack_multidimensional/muestreo_<int:muestreo>/', views.knapsack_multidimensional, name='knapsack_multidimensional'),
    path('knapsack_multidimensional/muestreo_<int:muestreo>/repeticiones_<int:repeticiones>', views.knapsack_multidimensional, name='knapsack_multidimensional'),
]
