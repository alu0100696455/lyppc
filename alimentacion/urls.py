from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('stigler/', views.stigler, name='stigler'),
    path('stigler/muestreo-<int:muestreo>/', views.stigler, name='stigler'),
    path('stigler/repeticiones-<int:repeticiones>', views.stigler, name='stigler'),
    path('stigler/muestreo-<int:muestreo>/repeticiones-<int:repeticiones>', views.stigler, name='stigler'),
    path('stigler/test-mode/', views.stigler, {'test_mode': True}),

    path('stigler-cbc/', views.stigler_cbc, name='stigler_cbc'),
    path('stigler-cbc/muestreo-<int:muestreo>/', views.stigler_cbc, name='stigler_cbc'),
    path('stigler-cbc/repeticiones-<int:repeticiones>', views.stigler_cbc, name='stigler_cbc'),
    path('stigler-cbc/muestreo-<int:muestreo>/repeticiones-<int:repeticiones>', views.stigler_cbc, name='stigler_cbc'),
    path('stigler-cbc/test-mode/', views.stigler_cbc, {'test_mode': True}),

    path('stigler-glop/', views.stigler_glop, name='stigler_glop'),
    path('stigler-glop/muestreo-<int:muestreo>/', views.stigler_glop, name='stigler_glop'),
    path('stigler-glop/repeticiones-<int:repeticiones>', views.stigler_glop, name='stigler_glop'),
    path('stigler-glop/muestreo-<int:muestreo>/repeticiones-<int:repeticiones>', views.stigler_glop, name='stigler_glop'),
    path('stigler-glop/test-mode/', views.stigler_glop, {'test_mode': True}),

    path('knapsack-multidimensional/', views.knapsack_multidimensional, name='knapsack_multidimensional'),
    path('knapsack-multidimensional/muestreo-<int:muestreo>/', views.knapsack_multidimensional, name='knapsack_multidimensional'),
    path('knapsack-multidimensional/repeticiones-<int:repeticiones>', views.knapsack_multidimensional, name='knapsack_multidimensional'),
    path('knapsack-multidimensional/muestreo-<int:muestreo>/repeticiones-<int:repeticiones>', views.knapsack_multidimensional, name='knapsack_multidimensional'),
    path('knapsack-multidimensional/test-mode/', views.knapsack_multidimensional, {'test_mode': True}),

    path('knapsack-multidimensional-cbc/', views.knapsack_multidimensional_cbc, name='knapsack_multidimensional_cbc'),
    path('knapsack-multidimensional-cbc/muestreo-<int:muestreo>/', views.knapsack_multidimensional_cbc, name='knapsack_multidimensional_cbc'),
    path('knapsack-multidimensional-cbc/repeticiones-<int:repeticiones>', views.knapsack_multidimensional_cbc, name='knapsack_multidimensional_cbc'),
    path('knapsack-multidimensional-cbc/muestreo-<int:muestreo>/repeticiones-<int:repeticiones>', views.knapsack_multidimensional_cbc, name='knapsack_multidimensional_cbc'),
    path('knapsack-multidimensional-cbc/test-mode/', views.knapsack_multidimensional_cbc, {'test_mode': True}),

    path('knapsack-multidimensional-bandb/', views.knapsack_multidimensional_bandb, name='knapsack_multidimensional_bandb'),
    path('knapsack-multidimensional-bandb/muestreo-<int:muestreo>/', views.knapsack_multidimensional_bandb, name='knapsack_multidimensional_bandb'),
    path('knapsack-multidimensional-bandb/repeticiones-<int:repeticiones>', views.knapsack_multidimensional_bandb, name='knapsack_multidimensional_bandb'),
    path('knapsack-multidimensional-bandb/muestreo-<int:muestreo>/repeticiones-<int:repeticiones>', views.knapsack_multidimensional_bandb, name='knapsack_multidimensional_bandb'),
    path('knapsack-multidimensional-bandb/test-mode/', views.knapsack_multidimensional_bandb, {'test_mode': True}),

    path('data-for-tests/', views.data_for_tests, name='data_for_tests'),
    path('data-for-tests/muestreo-<int:muestreo>/', views.data_for_tests, name='data_for_tests'),
]
