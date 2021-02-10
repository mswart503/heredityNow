import pygame

class Animal():
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



class Plant():
    def __init__(self, name, x, y, width, height, foliage):
        self.name = name
        self.x = x
        self.y = y
        self.foliage = foliage
        self.width = 2*self.foliage
        self.height = 3*self.foliage
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

class Button():
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height