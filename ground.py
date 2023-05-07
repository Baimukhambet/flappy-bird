import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets\sprites\base.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x <= -288:
            self.kill()


    

    