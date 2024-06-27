# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 19:22:55 2021

@author: Francis Allanah
"""

import random
import math
import copy

nodes = ["Berlin", "Dortmund", "München", "Hamburg", "Leipzig"]

costs = {
    "Berlin" : {
        "Berlin": 0,
        "Leipzig": 149,
        "München": 505,
        "Dortmund": 423,
        "Hamburg": 256,
    },
    "Leipzig": {
        "Berlin": 149,
        "Leipzig": 0,
        "München": 359,
        "Dortmund": 340,
        "Hamburg": 295,
    },
    "München": {
        "Berlin": 505,
        "Leipzig": 359,
        "München": 0,
        "Dortmund": 478,
        "Hamburg": 613,
    },
    "Dortmund": {
        "Berlin": 423,
        "Leipzig": 340,
        "München": 478,
        "Dortmund": 0,
        "Hamburg": 285,
    },
    "Hamburg": {
        "Berlin": 256,
        "Leipzig": 295,
        "München": 613,
        "Dortmund": 285,
        "Hamburg": 0,
    },
}

def annealing(initial_state, max_iterations, min_temp, initial_temp, alpha, print_iterations=False):
    # Simulated annealing function for TSP
    accept_count = 0
    reject_count = 0

    iteration_count = 0
    if print_iterations:
        print("INITIAL")
        print(initial_state, get_cost(initial_state))

    current_temp = initial_temp

    # Start by initializing the current state with the initial state
    solution = initial_state
    
    while iteration_count < max_iterations and current_temp > min_temp:
        if print_iterations:
            print("\n")
            print("Iteration:", iteration_count+1)
        neighbor = get_neighbors(solution)
        
        # Check if neighbor is best so far
        cost_diff = get_cost(neighbor) - get_cost(solution)
        # if the new solution is better, accept it
        if cost_diff <= 0:
            accept_count += 1
            solution = neighbor
            if print_iterations:
                print("Better solution accepted:")
                print(solution, get_cost(solution))
        else:
            if random.uniform(0, 1) <= math.exp((-float(cost_diff)) / float(current_temp)):
                accept_count += 1
                solution = neighbor
                if print_iterations:
                    print("Worse solution accepted:")
                    print(solution, get_cost(solution))
            else:
                if print_iterations:
                    print("Worse solution rejected")
                    print(neighbor, get_cost(neighbor))
                reject_count += 1
        current_temp = current_temp * alpha
        iteration_count += 1

    return solution, get_cost(solution), current_temp, accept_count, reject_count

def get_cost(state):
    # Calculates cost of a solution
    distance = 0
    
    for i in range(len(state)):
        from_city = state[i]
        to_city = None
        if i+1 < len(state):
            to_city = state[i+1]
        else:
            to_city = state[0]
        distance += costs[from_city][to_city]
    return distance
    
def get_neighbors(state):
    # Returns neighbor solution
    neighbor = copy.deepcopy(state)
    newState = swap(neighbor)
    return newState

def swap(state):
    # Perturbation function
    index_one = -1
    index_two = -1

    while index_one == index_two:
        index_one = random.randint(1, len(state) - 1)
        index_two = random.randint(1, len(state) - 1)

    city_one = state[index_one]
    state[index_one] = state[index_two]
    state[index_two] = city_one

    return state

temp = 3
is_warm_enough = False
max_iterations = 50

while not is_warm_enough:
    route, route_distance, current_temp, accept, reject = annealing(nodes, max_iterations, 0, temp, 0.95)
    if accept / max_iterations >= 0.8:
        is_warm_enough = True
        print("\n")
        print("Final Temperature:")
        print(temp)
        print("Final Acceptance ratio:")
        print(accept / max_iterations)
        continue
    temp = temp * 2
    print("Temperature:")
    print(temp)
    print("Acceptance ratio:")
    print(accept / max_iterations)


print("\n")
print("Using intital temperature: ", temp)
route, route_distance, current_temp, accept, reject = annealing(nodes, 1000000, 0.0001, temp, 0.95, True)

print("RESULT")
print(route)
print(route_distance)
print("Remaining Temperature")
print(current_temp)
print("Solutions accepted:")
print(accept)
print("Solutions rejected:")
print(reject)



