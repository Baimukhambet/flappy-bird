import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.entered = False
        self.passed = False


    def update(self, speed, bird_x):
        self.rect.x -= speed
        if self.rect.x <= -288:
            self.kill() 

        if bird_x > self.rect.topleft[0]:
            self.entered = True
        if bird_x > self.rect.topright[0] and not self.passed:
            self.passed = True
            return True

    def check(self, bird_x):
        if bird_x > self.rect.topleft[0] and not self.passed:
            self.entered = True
        if bird_x > self.rect.topright[0] and self.entered:
            self.passed = True
