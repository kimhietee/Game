import pygame

pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

box = pygame.rect.Rect(300, 200, 50, 50)
red = (255, 0, 0)
blue = (0 ,0, 255)
running = True

while running:
    mouse_position = pygame.mouse.get_pos()
    print(mouse_position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        # if moouse_position =s

    screen.fill((255, 180, 100))

    # screen.blit(screen, )
    pygame.draw.rect(screen, red, box)
    pygame.display.flip()
    clock.tick(FPS)