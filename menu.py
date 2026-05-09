import pygame
import sys
import main

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
pygame.display.set_icon(apple)

background = pygame.image.load("Graphics/background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font_title = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 80)
font_button = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK = (30, 30, 30)

play_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 60)
quit_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 60)


def draw_menu():
    screen.blit(background, (0, 0))

    title = font_title.render("SNAKE GAME", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//3)))

    pygame.draw.rect(screen, GRAY, play_rect)
    pygame.draw.rect(screen, GRAY, quit_rect)

    play_text = font_button.render("PLAY", True, WHITE)
    quit_text = font_button.render("QUIT", True, WHITE)

    screen.blit(play_text, play_text.get_rect(center=play_rect.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                main.run_game()

            if quit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    draw_menu()
    pygame.display.update()