import pygame, random

class Animal:
    def __init__(self, name, x, y, width, height, belly, mouth_size, physical_sensitivity):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.belly = belly
        self.mouth_size = mouth_size
        self.belly_counter = []
        self.count = 0
        while self.count < 1000:
            self.belly_counter.append(self.count*10)
            self.count+=1
        self.count = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.physical_sensitivity = physical_sensitivity
        self.body_awareness = pygame.Rect(self.x - self.physical_sensitivity, self.y + self.physical_sensitivity, self.height + (self.physical_sensitivity * 2),
                                          self.width + (self.physical_sensitivity * 2))

        self.full_mouth = False
        self.mouth_counter = 0
        self.target = None
        #self.stats = False

    def draw(self, win):
        #self.change()
        body = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win,(235,235,235),body)
        #if self.stats == True:

    def change(self):
        cur_width = self.width
        cur_height = self.height
        self.width = 2*new_foliage
        self.height = 3*new_foliage
        self.x = self.x+((cur_width-self.width)/2)
        self.y = self.y+((cur_height-self.height)/2)
        self.foliage = new_foliage

    def move(self, target_x, target_y, obstacles):
        # checks for obstacles and moves at least 5 px away
        is_there_obstacle = False
        self.body_awareness = pygame.Rect(self.x - self.physical_sensitivity, self.y + self.physical_sensitivity,
                                          self.height + (self.physical_sensitivity * 2),
                                          self.width + (self.physical_sensitivity * 2))
        if obstacles:
            for obstacle in obstacles:
                if pygame.Rect.colliderect(self.body_awareness, obstacle.rect):
                    too_close = pygame.Rect(self.x-5, self.y+5, self.width+10, self.height+10)
                    if pygame.Rect.colliderect(too_close, obstacle):
                        is_there_obstacle = True
                        if self.x > obstacle.x:
                            self.x = self.x + 1
                        if self.x < obstacle.x:
                            self.x = self.x - 1
                        if self.y > obstacle.y:
                            self.y = self.y + 1
                        if self.y < obstacle.x:
                            self.y = self.y - 1
                        break

        if is_there_obstacle == False:
            # If no visible obstacles, go straight at the target
            if self.x > target_x:
                self.x = self.x - 1
            if self.x < target_x:
                self.x = self.x + 1
            if self.y > target_y:
                self.y = self.y - 1
            if self.y < target_y:
                self.y = self.y + 1
            self.count += 1
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.count in self.belly_counter:
                self.belly = self.belly-1

    def eat(self, plant_to_eat):
        if self.full_mouth:
            self.mouth_counter = self.mouth_counter +1
            if self.mouth_counter == 100:
                self.full_mouth = False
                self.mouth_counter = 0
            return plant_to_eat, True
        else:
            self.belly = self.belly+self.mouth_size
            return plant_to_eat, False



class Plant:
    def __init__(self, name, x, y, width, height, strength):
        self.name = name
        self.x = x
        self.y = y
        self.strength = strength
        self.foliage = self.strength*2
        self.foliage_limit = self.strength*5
        self.width = .1*self.foliage
        self.height = .2*self.foliage
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, win, new_size=""):
        #if new_size != "":
            #self.x

        #self.width = 2*self.foliage
        #self.height = 3*self.foliage
        body = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (15, 112, 4), body)

    def change(self, animal):
        new_foliage = self.foliage - animal.mouth_size
        cur_width = self.width
        cur_height = self.height
        self.width = 2*new_foliage
        self.height = 3*new_foliage
        self.x = self.x+((cur_width-self.width)/2)
        self.y = self.y+((cur_height-self.height)/2)
        self.foliage = new_foliage

    def grow(self):
        if self.foliage < self.foliage_limit:
            self.foliage = self.foliage+1
            cur_width = self.width
            cur_height = self.height
            self.width = 2*self.foliage
            self.height = 3*self.foliage
            self.x = self.x + ((cur_width - self.width) / 2)
            self.y = self.y + ((cur_height - self.height) / 2)

class Button():
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Area:
    def __init__(self,x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tile_dict = dict()
        self.number_of_x_tiles = 0
        self.number_of_y_tiles = 0

    def create_area(self, win, tile_width_height):
        self.number_of_x_tiles = int(self.width/tile_width_height)
        self.number_of_y_tiles = int(self.height/tile_width_height)
        for tile_y in range(self.number_of_y_tiles):
            for tile_x in range(self.number_of_x_tiles):
                self.tile_dict[(tile_x, tile_y)] = Tile(tile_x*tile_width_height, tile_y*tile_width_height, tile_width_height, tile_width_height, "field")
                self.tile_dict[(tile_x, tile_y)].draw(win)

    def draw_area(self, win):
        for tile_y in range(self.number_of_y_tiles):
            for tile_x in range(self.number_of_x_tiles):
                self.tile_dict[(tile_x, tile_y)].draw(win)

    def check_for_growth(self):
        plants_to_return = []
        for tile_y in range(self.number_of_y_tiles):
            for tile_x in range(self.number_of_x_tiles):
                plants_to_return.append(self.tile_dict[tile_x, tile_y].check_growth())
        return plants_to_return

zone_dict = {"field": {"sand": (.1, .3),
                       "silt": (.3, .5),
                       "clay": (.3, .5),
                       "seeds": ["Grass"]}}

class Tile:
    def __init__(self, x, y, width, height, zone_type):
        # basic perameters
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
        self.zone_type = zone_type
        #soil content
        # ideal growing ratio: sand = 20% silt = 40% clay = 40%
        # perfect color: sand = 100 silt = 80 clay = 15
        perfect_soil_color = (100, 80, 15)
        sand = random.uniform(zone_dict[self.zone_type]["sand"][0],zone_dict[self.zone_type]["sand"][1])
        silt = random.uniform(zone_dict[self.zone_type]["silt"][0],zone_dict[self.zone_type]["silt"][1])
        clay = random.uniform(zone_dict[self.zone_type]["clay"][0],zone_dict[self.zone_type]["clay"][1])
        self.sand_silt_clay_ratio = {"sand":sand, "silt":silt, "clay":clay}
        # perfect growing rate is .4, reduces by the total of distance from perfect soil
        self.growing_rate = .4 -(abs(self.sand_silt_clay_ratio["sand"]-.2)+abs(self.sand_silt_clay_ratio["silt"]-.2)+abs(self.sand_silt_clay_ratio["clay"]-.2))
        self.color = (perfect_soil_color[0]+((100*(self.sand_silt_clay_ratio["sand"]-.2))/2), perfect_soil_color[1]+((100*(self.sand_silt_clay_ratio["silt"]-.40)/2)), perfect_soil_color[2]+((100*(self.sand_silt_clay_ratio["clay"]-.40))/2))
        self.plants = None

    def draw(self, win, new_rect=""):

        if new_rect != "":
            pass
            # Where the location of the tile can be changed

        else:
            pygame.draw.rect(win, self.color, self.rect)

    def check_growth(self):
        # perfect soil conditions = sand = 20% silt = 40% clay = 40%
        # the above mix yields a 40% chance to grow grass from seed
        # Once the grass seeds it starts growing

        if self.plants == None:

            # test whether seeds grow:
            growth_check = random.randint(0, 100)
            if growth_check <= (self.growing_rate*100):
                seed = Plant(zone_dict[self.zone_type]["seeds"], self.x+(self.width/2)-2, self.y+self.height, 4, 8, random.randint(0,5))
                self.plants = [seed]
                return seed
            else:
                return None
        else:
            return self.grow()

    def grow(self):
        plant_to_grow = self.plants[0]
        growth_check = random.randint(0, 100)
        if growth_check <= (self.growing_rate * 100):
            plant_to_grow.grow()
        return plant_to_grow

