import pygame, random
from elfClasses import Cardslot
from evoClasses import Animal, Plant

pygame.init()
bg = pygame.image.load("field.png") # Credit http://pixelartmaker.com/art/41ac4fd04fde6fb
yellow = (12,150,78)

def main():
    pygame.display.set_caption('Evolution v0.1')
    screenwidth = 1000
    screenheight = 600
    win = pygame.display.set_mode((screenwidth, screenheight))
    win.blit(bg, (0, 0))
    pygame.display.flip()
    sheep = create_a_sheep()
    grass = grow_grass()
    animals_to_draw = [sheep]
    plants_to_draw = [grass]
    #sheep.draw(win)
    time = 0
    time_list = []
    count = 0
    while count < 100:
        num = count*random.randint(1,100)
        time_list.append(num)
        count += 1

    # game loop
    while True:
        time = time + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                sheep = create_a_sheep()
                animals_to_draw.append(sheep)
                #grass = grow_grass()
                #plants_to_draw.append(grass)

        if time in time_list:
            grass = grow_grass()
            plants_to_draw.append(grass)

        redraw_window(win, animals_to_draw, plants_to_draw)


def redraw_window(win, animals_to_draw, plants_to_draw):
    win.blit(bg, (0, 0))

    for animal in animals_to_draw:
        closest_grass = find_closest_grass(animal, plants_to_draw)
        animal, closest_grass = check_if_found_grass(closest_grass, animal)
        if closest_grass.foliage <= 0:
            plants_to_draw.remove(closest_grass)
        animal.move(closest_grass.x, closest_grass.y, animals_to_draw)
        animal.draw(win)
    for plant in plants_to_draw:
        plant.draw(win)

    pygame.display.flip()

def create_a_sheep():
    rand_x = random.randint(0, 1000-20)
    rand_y = random.randint(0, 600-20)
    sheep = Animal("Sheep", rand_x, rand_y, 40, 30, 100, 5, 10)
    return sheep

def grow_grass():
    rand_x = random.randint(0, 1000-20)
    rand_y = random.randint(0, 600-20)
    grass = Plant("Grass", rand_x, rand_y, 15, 25, 50)
    return grass

def find_closest_grass(animal, plants_to_draw):
    final_plant = 0
    for plant in plants_to_draw:
        if final_plant == 0:
            final_plant = plant
        else:
            cur_x_distance = abs(final_plant.x - animal.x)
            cur_y_distance = abs(final_plant.y - animal.y)
            cur_total_distance = cur_x_distance + cur_y_distance
            new_x_distance = abs(plant.x - animal.x)
            new_y_distance = abs(plant.y - animal.y)
            new_total_distance = new_x_distance + new_y_distance

            if cur_total_distance > new_total_distance:
                final_plant = plant

    return final_plant

def check_if_found_grass(grass, animal):
    if pygame.Rect.colliderect(animal.rect, grass.rect):
        grass = animal.eat(grass)
        return animal, grass
    else:
        return animal, grass


main()

