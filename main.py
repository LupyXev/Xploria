import pygame
import player

pygame.init()

WIDTH, HEIGHT = 1280, 720
GAME_NAME = "Xploria Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()
fps = 60

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill("white")
        pygame.display.update()
        clock.tick(fps)