from django.shortcuts import render
from django.db.models import Max

import random
import atexit
import copy
from time import time
from datetime import timedelta

# Modelos
from alimentacion.models import Alimento, Cantidad, Comida

# OR-TOOLS
from ortools.linear_solver import pywraplp
from ortools.algorithms import pywrapknapsack_solver

def index(request):
    return render(request, 'alimentacion/index.html')

class Datos:
    data_for_tests = []
    # [nutriente, mínimo recomendado, máximo recomendado]
    DEFAULTS_NUTRIENTS = [
        ['Calorías (1000s)', 2, 4],
        ['Proteínas (g)', 50, 200],
        ['Calcio (g)', 1, 2.5],
        ['Hierro (mg)', 18, 45],
        ['Vitamina A (1000 IU)', 3, 10],
        ['Vitamina B1 (mg)', 1.2, 4],
        ['Vitamina B2 (mg)', 1.3, 4],
        ['Vitamina B3 (mg)', 16, 35],
        ['Vitamina C (mg)', 90, 2000]]


# Stigler diet

def stigler_cbc(request, test_mode=False, muestreo=0, repeticiones=1):
    solver = pywraplp.Solver('SolveStigler', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    return stigler(request, solver, test_mode, muestreo, repeticiones)

def stigler_glop(request, test_mode=False, muestreo=0, repeticiones=1):
    solver = pywraplp.Solver('SolveStigler', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    return stigler(request, solver, test_mode, muestreo, repeticiones)

def stigler(request, solver=None, test_mode=False, muestreo=0, repeticiones=1):
    # Nombre, Unidad, Precio (euros), Calorias, Proteínas (g), Calcio (g), Hierro (mg),
    # Vitamina A (IU), Vitamina B1 (mg), Vitamina B2 (mg), Vitamina B3 (mg), Vitamina C (mg)
    if test_mode is False:
        if muestreo == 0:
            data = list(Alimento.objects.values_list('nombre', 'unidad', 'precio', 'calorias', 'proteinas', 'calcio', 'hierro', 'vitamina_a', 'vitamina_b1', 'vitamina_b2', 'vitamina_b3', 'vitamina_c'))
        else:
            data = []
            for i in range(muestreo):
                # nombre = aleatorio, unidad = 1~500,, precio = 0.01~1.00
                # calorias = 1~50, protenias = 0~2000, calcio = 0~20
                # hierro = 0~500, vitamina A = 0~200, vitamina B1 = 0~50
                # vitamina B2 = 0~100, vitamina B3 = 0~500 , vitamina C = 0~3000
                data += [[
                    'Alimento ' + str(i + 1),       random.uniform(1, 100),         random.uniform(1.00, 10.00),
                    random.uniform(0.00, 2.00),     random.uniform(0.00, 50.00),    random.uniform(0.00, 1.30),
                    random.uniform(0.00, 8.00),     random.uniform(0.00, 3.00),     random.uniform(0.00, 1.20),
                    random.uniform(0.00, 1.30),     random.uniform(0.00, 16.00),    random.uniform(0.00, 90.00)
                ]]
    else:
        data = Datos.data_for_tests

    # Nutrient minimums.
    nutrients = Datos.DEFAULTS_NUTRIENTS
    nutrient_minimus = nutrients

    columns_names = ['Nombre', 'Unidad (g)', 'Precio (€)'] + [nutrient[0] for nutrient in nutrients]

    times = []
    mean = 0

    for i in range(repeticiones):
        #Timer start
        timer_start = time()

        # Instanciar a Glop solver, SolveStigler.
        if solver is None:
            solver = pywraplp.Solver('SolveStigler', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        # Array para los datos nutricionales.
        food = [[]] * len(data)

        # Objetivo: minimizar el precio de la comida.
        objective = solver.Objective()

        for i in range(0, len(data)):
        	food[i] = solver.NumVar(0.0, solver.infinity(), data[i][0])
        	objective.SetCoefficient(food[i], 1)
        objective.SetMinimization()

    	# Crear la restricción de cada nutriente.
        constraints = [0] * len(nutrients)
        for i in range(0, len(nutrients)):
        	constraints[i] = solver.Constraint(nutrients[i][1], solver.infinity())
        	for j in range(0, len(data)):
        		constraints[i].SetCoefficient(food[j], float(data[j][i+3]))
        		# Solve!
        status = solver.Solve()

        #Timer end
        timer_end = time()

        mean += timer_end-timer_start
        times.append(str(timedelta(seconds=(timer_end-timer_start)).microseconds) + " µs")

    mean = str(timedelta(seconds=(mean/repeticiones)).microseconds) + " µs"

    if status == solver.OPTIMAL:
    	# Mostrar la cantidad (en euros) a comprar de cada comida.
    	price = 0
    	num_nutrients = len(data[0]) - 3
    	nutrients = [0] * (len(data[0]) - 3)
    	results_list = []
    	for i in range(0, len(data)):
    		price += food[i].solution_value()

    		for nutrient in range(0, num_nutrients):
    			nutrients[nutrient] += float(data[i][nutrient+3]) * food[i].solution_value()

    		if food[i].solution_value() > 0:
    			results_list.append("%s = %f" % (data[i][0], food[i].solution_value()))

    	context = {
            'foods': data,
            'columns_names': columns_names,
            'nutrient_minimus': nutrient_minimus,
            'times': times,
            'mean': mean,
    		'results_list': results_list,
    		'optimal_annual_price': '%.2f€' % (365 * price),
    	}
    	return render(request, 'alimentacion/stigler.html', context)

    else: # No optimal solution was found.
        if status == solver.FEASIBLE:
            context = {
                'foods': data,
                'columns_names': columns_names,
                'times': times,
                'mean': mean,
                'results_list': list(),
                'error': 'Una solución potencialmente subóptmia ha sido encontrada.',
            }
            return render(request, 'alimentacion/stigler.html', context)
        else:
            context = {
                'foods': data,
                'columns_names': columns_names,
                'times': times,
                'mean': mean,
                'results_list': list(),
                'error': 'El resolutor no pudo solucionar el problema.',
            }
            return render(request, 'alimentacion/stigler.html', context)


# Knapsack Multidimensional

def knapsack_multidimensional_cbc(request, test_mode=False, muestreo=0, repeticiones=1):
    solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER,
    "Multi-dimensional solver");
    return knapsack_multidimensional(request, solver, test_mode, muestreo, repeticiones)

def knapsack_multidimensional_bandb(request, test_mode=False, muestreo=0, repeticiones=1):
    solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
    "Multi-dimensional solver");
    return knapsack_multidimensional(request, solver, test_mode, muestreo, repeticiones)

def knapsack_multidimensional(request, solver=None, test_mode=False, muestreo=0, repeticiones=1):
    # Nombre, Unidad, Precio (euros), Calorias, Proteínas (g), Calcio (g), Hierro (mg),
    # Vitamina A (IU), Vitamina B1 (mg), Vitamina B2 (mg), Vitamina B3 (mg), Vitamina C (mg)
    if test_mode is False:
        if muestreo == 0:
            data = list(Alimento.objects.values_list('nombre', 'unidad', 'precio', 'calorias', 'proteinas', 'calcio', 'hierro', 'vitamina_a', 'vitamina_b1', 'vitamina_b2', 'vitamina_b3', 'vitamina_c'))
        else:
            data = []
            for i in range(muestreo):
                # nombre = aleatorio, unidad = 1~500, precio = 1~100
                # calorias = 0~2, protenias = 0~50, calcio = 0~1.3
                # hierro = 0~8, vitamina A = 0~3, vitamina B1 = 0~1.2
                # vitamina B2 = 0~1.3, vitamina B3 = 0-16 , vitamina C = 0~90
                data += [[
                    'Alimento ' + str(i + 1),       random.uniform(1, 100),         random.uniform(1.00, 10.00),
                    random.uniform(0.00, 2.00),     random.uniform(0.00, 50.00),    random.uniform(0.00, 1.30),
                    random.uniform(0.00, 8.00),     random.uniform(0.00, 3.00),     random.uniform(0.00, 1.20),
                    random.uniform(0.00, 1.30),     random.uniform(0.00, 16.00),    random.uniform(0.00, 90.00)
                ]]
    else:
        data = Datos.data_for_tests

    # Nutrient minimums.
    nutrients = Datos.DEFAULTS_NUTRIENTS

    nutrient_minimus = nutrients

    columns_names = ['Nombre', 'Unidad', 'Precio (€)'] + [nutrient[0] for nutrient in nutrients]

    times = []
    mean = 0
    computed_value = 0

    for i in range(repeticiones):
        #Timer start
        timer_start = time()

        profits = [item[2] for item in data]
        max_price = max(profits)
        profits = [max_price-item for item in profits]
        weights = [[float(item[3]) for item in data]
                , [float(item[4]) for item in data]
                , [float(item[5]) for item in data]
                , [float(item[6]) for item in data]
                , [float(item[7]) for item in data]
                , [float(item[8]) for item in data]
                , [float(item[9]) for item in data]
                , [float(item[10]) for item in data]
                , [float(item[11]) for item in data]]
        capacities = [float(item[1]) for item in nutrients]

        if solver is None:
            solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
            "Multi-dimensional solver")

        solver.Init(profits, weights, capacities)

        computed_value = solver.Solve()

        #Timer end
        timer_end = time()

        mean += timer_end-timer_start
        times.append(str(timedelta(seconds=(timer_end-timer_start)).microseconds) + " µs")

    mean = str(timedelta(seconds=(mean/repeticiones)).microseconds) + " µs"

    packed_items = [x for x in range(0, len(weights[0]))
                    if solver.BestSolutionContains(x)]

    context = {
        'foods': data,
        'columns_names': columns_names,
        'nutrient_minimus': nutrient_minimus,
        'times': times,
        'mean': mean,
        'packed_items': packed_items,
    }

    return render(request, 'alimentacion/knapsack_multidimensional.html', context)


def data_for_tests(request, muestreo=0):
    if muestreo > 0:
        Datos.data_for_tests = []
        for i in range(muestreo):
            # nombre = aleatorio, unidad = 1~500, precio = 1~100
            # calorias = 0~2, protenias = 0~50, calcio = 0~1.3
            # hierro = 0~8, vitamina A = 0~3, vitamina B1 = 0~1.2
            # vitamina B2 = 0~1.3, vitamina B3 = 0-16 , vitamina C = 0~90
            Datos.data_for_tests += [[
                'Alimento ' + str(i + 1),       random.uniform(1, 500),         random.uniform(1.00, 10.00),
                random.uniform(0.00, 2.00),     random.uniform(0.00, 50.00),    random.uniform(0.00, 1.30),
                random.uniform(0.00, 8.00),     random.uniform(0.00, 3.00),     random.uniform(0.00, 1.20),
                random.uniform(0.00, 1.30),     random.uniform(0.00, 16.00),    random.uniform(0.00, 90.00)
            ]]

    nutrients = Datos.DEFAULTS_NUTRIENTS

    nutrient_minimus = nutrients
    columns_names = ['Nombre', 'Unidad', 'Precio (€)'] + [nutrient[0] for nutrient in nutrients]

    context = {
        'foods': Datos.data_for_tests,
        'columns_names': columns_names,
        'nutrient_minimus': nutrient_minimus,
    }
    return render(request, 'alimentacion/data_for_tests.html', context)
