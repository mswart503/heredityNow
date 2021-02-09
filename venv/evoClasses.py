import pygame

class Animal():
    def __init__(self, name, x, y, width, height, belly, mouth_size, sight_distance):
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
        self.sight_distance = sight_distance

    def draw(self, win):
        body = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win,(235,235,235),body)

    def move(self, target_x, target_y, obstacles):

        # checks for obstacles and moves at least 5 px away
        is_there_obstacle = False
        sight = pygame.Rect(self.x-self.sight_distance, self.y+self.sight_distance, self.height+(self.sight_distance*2), self.width+(self.sight_distance*2))
        if obstacles:
            for obstacle in obstacles:
                if pygame.Rect.colliderect(sight, obstacle.rect):
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
        final_foliage = plant_to_eat.foliage - self.mouth_size
        foliage_eaten = plant_to_eat.foliage - final_foliage
        self.belly = self.belly+foliage_eaten
        plant_to_eat.foliage = plant_to_eat.foliage-foliage_eaten
        return plant_to_eat



class Plant():
    def __init__(self, name, x, y, width, height, foliage):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.foliage = foliage
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, win):
        body = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (15, 112, 4), body)


class Button():
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height