import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, start_position, images, menu) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]
        self.state = 0
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        self.speed = 0
        self.flap = False

        self.menu = menu
        self.isAlive = True
        
    
    def update(self):
        if not self.menu:        
            if self.isAlive:
                self.state += 1
                if self.state >= 30: self.state = 0
                self.image = self.images[self.state // 10]
                self.image = pygame.transform.rotate(self.image, self.speed * -6)
            self.speed += 0.4
            if self.speed > 5:
                self.speed = 5
            if self.rect.y < 512:
                self.rect.y += self.speed
            if self.speed >= 0 or self.speed <= 0.8:
                self.flap = False
            if self.rect.y >=374:
                self.rect.y = 374
                self.isAlive = False
        else:
            self.state += 1
            if self.state >= 30: self.state = 0
            self.image = self.images[self.state // 10]
            self.image = pygame.transform.rotate(self.image, self.speed * -6)
        

    def jump(self):
        if not self.flap and self.rect.y > 0 and self.isAlive:
            self.flap = True
            self.speed = -5.6
