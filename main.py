import pygame
import city
import ant
import random
import time

starttime=time.time()
pygame.init()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill([255, 255, 255])
pygame.display.set_caption("SalesAnt Simulator")
pygame.display.update()
run = True
default_city_image = "city.png"
city_image = ["first_city.png", "city2.png", "city3.png", "city4.png", "city5.png", "city6.png", "city7.png", "city8.png"]
first_city_image = "first_city.png"

cost_matrix = [[0, 10, 40, 60, 55, 75, 80, 70],
               [10, 0, 45, 55, 60, 75, 80, 65],
               [40, 45, 0, 90, 15, 55, 50, 60],
               [60, 55, 90, 0, 85, 60, 80, 50],
               [15, 60, 15, 85, 0, 30, 20, 35],
               [75, 75, 55, 60, 30, 0, 15, 10],
               [80, 80, 50, 80, 20, 15, 0, 30],
               [70, 65, 60, 50, 35, 10, 30, 0]]

pheromone_value_matrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1]]

# For trails:
trail_value =  [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
# List with chances of each choice
chance_list = []
probability_list = []
city_list = []
not_visited_cities = [1, 2, 3, 4, 5, 6, 7]
testing_coordinates = [[100, 100], [50, 200], [400, 50], [150, 500], [500, 150], [500, 400], [600, 300], [400, 400]]
ant = ant.Ant(0, 0)
current_city = 0
shortest_path = 1000
which_iteration = 0
trail_checker = 0

# Creates cities according to testing_coordinates list


def show_pheromones():
    for element in pheromone_value_matrix:
        print(element)


def city_maker():
    city_list.clear()
    for x in range(0, 8):
        temp_city = city.City()
        temp_city.xPos = testing_coordinates[x][0]
        temp_city.yPos = testing_coordinates[x][1]
        city_list.append(temp_city)
    return city_list

# Updates the whole screen and its objects: cities, ants and pheromone trails


def update_screen(cities, pheromones, ant):
    counter = 0
    screen.fill([255, 255, 255])
    # Displaying cities
    for city in cities:
        current_image = pygame.image.load(city_image[counter])
        screen.blit(current_image, (city.xPos + 1, city.yPos + 1))
        counter += 1
    # Displaying current ant position
    current_image = pygame.image.load(ant.image)
    screen.blit(current_image, (ant.xPos + 10, ant.yPos + 20))
    external_counter = 0
    # Displaying trails of pheromone between cities
    for pheromone_list in pheromones:
        internal_counter = 0
        for pheromone_value in pheromone_list:
            stroke_width = pheromone_value
            pygame.draw.line(screen, (0, 0, 255), (cities[external_counter].xPos, cities[external_counter].yPos),(cities[internal_counter].xPos, cities[internal_counter].yPos), stroke_width)
            internal_counter += 1
        external_counter += 1
    pygame.display.flip()

# Chooses the city according to the ACO algorithm

# Chooses city basing on the cost of each journey


def choose_city():
    # print("Wybieranie najkrótszej opcji")
    #print("Obecna długość: " + str(len(not_visited_cities)))
    if len(not_visited_cities) > 0:
        lowest_cost = 100
        for element in cost_matrix[current_city]:
            if element < lowest_cost and element != 0 and cost_matrix[current_city].index(
                    element) in not_visited_cities:
                lowest_cost = element
                closest_city_index = cost_matrix[current_city].index(element)
        not_visited_cities.remove(closest_city_index)
        return closest_city_index
    else:
        return 0

# Chooses city randomly


def choose_city_randomly():
    # print("Wybieranie losowe")
    if len(not_visited_cities) > 0:
        randomCity = int(random.choice(not_visited_cities))
        #not_visited_cities.remove(randomCity)
        return randomCity
    else:
        return 0
# Do funkcji trzeba przekazać obecną listę odwiedzonych miast


def choose_city_with_probability():
    method_choice = random.uniform(0, 1)
    random_number = random.uniform(0, 1)
    current_best = 0
    if len(not_visited_cities) > 0:
        if method_choice > 0.5:
            for element in chance_list:
                if element > current_best:
                    current_best = element
            return not_visited_cities[chance_list.index(current_best)]
        else:
            for probability in probability_list:
                if random_number < probability:
                    return not_visited_cities[probability_list.index(probability)]
    else:
        return 0





# Moves the ant to the chosen city and updates the pheromone trail


def calculate_chance(current_index, cost_importance, pheromone_importance):
    if len(not_visited_cities) > 0:
        chance_list.clear()
        probability_list.clear()
        total_sum = 0
        counter1 = 0
        cost_sum = 0
        iterations = len(not_visited_cities)
        for x in range(0, iterations):
            city_index = not_visited_cities[x]
            if cost_matrix[current_index][city_index] > 0:
                cost_sum += cost_matrix[current_index][city_index]
                total_sum += (pheromone_value_matrix[current_index][city_index]) ** pheromone_importance * (
                            (1 / cost_matrix[current_index][city_index]) ** cost_importance)
        for element in not_visited_cities:
            chance_list.append(((pheromone_value_matrix[current_index][element]) ** pheromone_importance * (
                           1 / cost_matrix[current_index][element])) ** cost_importance / total_sum)
        temp_counter = len(chance_list)
        for element in chance_list:
            current_sum = 0
            for x in range(0, temp_counter):
                current_sum += chance_list[x]
            probability_list.append(current_sum)
            temp_counter -= 1
        probability_list.reverse()

    else:
        return 0


def move_ant(cities):
    global current_city

    global which_iteration
    calculate_chance(current_city, 3, 1)
    chosenCity = choose_city_with_probability()
    if chosenCity != 0:
        not_visited_cities.remove(chosenCity)
    ant.xPos = cities[chosenCity].xPos
    ant.yPos = cities[chosenCity].yPos
    trail_value[current_city][chosenCity] += 1
    ant.recent_path_cost += cost_matrix[current_city][chosenCity]
    ant.recent_path.append(chosenCity)
    ant.recent_pheromone_value += pheromone_value_matrix[current_city][chosenCity]
    if chosenCity == 0:
        not_visited_cities.extend([1, 2, 3, 4, 5, 6, 7])
        update_pheromone(ant)
    current_city = chosenCity
    update_screen(cities, trail_value, ant)


def update_pheromone(ant):
    global which_iteration
    which_iteration += 1
    global shortest_path
    if ant.recent_path_cost < shortest_path:
        shortest_path = ant.recent_path_cost
        print("Iteracja nr " + str(which_iteration) + ", obecnie najmniejszy koszt: " + str(shortest_path))
        print("Obecnie najkrótsza ścieżka: " + str(ant.recent_path))
    if ant.recent_path_cost != 0:
        pheromone_value = round(1 / ant.recent_path_cost, 4)
    else:
        pheromone_value = 0
    is_first_journey = True
    for element in ant.recent_path:
        if is_first_journey:
            pheromone_value_matrix[0][element] += pheromone_value
            is_first_journey = False
            previous_value = element
        else:
            pheromone_value_matrix[previous_value][element] += pheromone_value
            previous_value = element
    ant.recent_path = []
    ant.recent_path_cost = 0


while run:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                city_list = city_maker()
                ant.xPos = city_list[0].xPos
                ant.yPos = city_list[0].yPos
                update_screen(city_list, trail_value, ant)
            if event.key == pygame.K_RIGHT:
                x = 0
                while x < 1000:
                    move_ant(city_list)
                    x += 1
                print("Koniec!")
        if event.type == pygame.QUIT:
            run = False
