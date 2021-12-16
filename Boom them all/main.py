from os import path
from random import randint

import pygame


class Bomb(pygame.sprite.Sprite):
    bomb = pygame.image.load(path.join("data", "bomb.png"))
    boom = pygame.image.load(path.join("data", "boom.png"))

    def __init__(self, screen_size, *args):
        super(Bomb, self).__init__(*args)
        self.image = self.bomb
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.image.get_width() // 2,
                              screen_size[0] - self.image.get_width())
        self.rect.y = randint(self.image.get_height() // 2,
                              screen_size[1] - self.image.get_height())
        self.flag = True

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN \
                and self.rect.collidepoint(args[0].pos) and self.flag:
            self.image = self.boom
            self.rect.move_ip(-self.bomb.get_width() // 2, -self.bomb.get_height() // 2)
            self.flag = False


class Game:
    def __init__(self, **kwargs):
        self.size = kwargs.get("size", (600, 400))
        self.bg_color = kwargs.get("bg_color", (0, 0, 0))
        self.title = kwargs.get("title", "New Game")
        self.FPS = kwargs.get("FPS", 30)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

        self.objects_groups = dict()

    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.objects_groups["bombs"].update(event)
        return True

    def game_update(self):
        for group in self.objects_groups.values():
            group.update()

    def game_render(self):
        self.screen.fill(self.bg_color)
        for group in self.objects_groups.values():
            group.draw(self.screen)

    def add_group(self, name):
        self.objects_groups[name] = pygame.sprite.Group()

    def play(self):
        while self.game_events():
            self.game_update()
            self.game_render()

            pygame.display.flip()
            self.clock.tick(self.FPS)
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game = Game(size=(500, 500), bg_color=(0, 0, 0), title="Boom them all", FPS=30)
    game.add_group("bombs")
    for _ in range(20):
        game.objects_groups["bombs"].add(Bomb(game.size))
    game.play()
