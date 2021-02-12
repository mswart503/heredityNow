import pygame, random
from elfClasses import Cardslot
from evoClasses import Animal, Plant, Area

pygame.init()
bg = pygame.image.load("field.png") # Credit http://pixelartmaker.com/art/41ac4fd04fde6fb
yellow = (12,150,78)

def main():
    pygame.display.set_caption('Heredity Now v0.2')
    screenwidth = 1000
    screenheight = 600
    win = pygame.display.set_mode((screenwidth, screenheight))
    win.blit(bg, (0, 0))
    area = Area(0,0,screenwidth,screenheight)
    area.create_area(win, 20)
    pygame.display.flip()
    sheep = create_a_sheep()
    grass = grow_grass()
    animals_to_draw = [sheep]
    plants_to_draw = [grass]
    sheep.draw(win)
    time = 0
    time_list = []
    count = 0
    while count < 1000:
        #num = count*random.randint(1,100)
        time_list.append(count*10)
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

        # controls how grass is added to the field
        #    grass = grow_grass()
        #    plants_to_draw.append(grass)
        if time in time_list:
            plants_to_draw = area.check_for_growth()
        redraw_window(win, animals_to_draw, plants_to_draw, area)


def redraw_window(win, animals_to_draw, plants_to_draw, area):
    #win.blit(bg, (0, 0))
    area.draw_area(win)
    for plant in plants_to_draw:
        if plant:
            plant.draw(win)
    for animal in animals_to_draw:
        # the animal finds the closest grass
        if animal.target == None:
            animal.target = find_closest_grass(animal, plants_to_draw)
        animal, closest_grass, eating = check_if_found_grass(animal.target, animal)
        if eating:
            closest_grass.draw(win)
        if closest_grass.foliage <= 0:
            if closest_grass in plants_to_draw:
                plants_to_draw.remove(closest_grass)
        other_animals = animals_to_draw.copy()
        other_animals.remove(animal)
        animal.move(closest_grass.x, closest_grass.y, other_animals)
        animal.draw(win)


    pygame.display.flip()

def create_a_sheep():
    rand_x = random.randint(0, 1000-20)
    rand_y = random.randint(0, 600-20)
    sheep = Animal("Sheep", rand_x, rand_y, 40, 30, 100, 1, 10)
    return sheep

def grow_grass():
    rand_x = random.randint(0, 1000-20)
    rand_y = random.randint(0, 600-20)
    grass = Plant("Grass", rand_x, rand_y, 15, 25, random.randint(2,15))
    return grass

def find_closest_grass(animal, plants_to_draw):
    final_plant = Plant("None", 0, 0, 0, 0, 0)
    for plant in plants_to_draw:
        if plant == None:
            pass
        elif final_plant.name == "None":
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
        grass, still_full = animal.eat(grass)
        #if not still_full:
        grass.change(animal)
        animal.full_mouth = True
        return animal, grass, True
    else:
        return animal, grass, False


main()

