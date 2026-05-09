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
font_button = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 38)
how_to_play = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 20)
volume_and_brightness = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 20)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK = (30, 30, 30)

button_width = 200
button_height = 60
center_x = WIDTH // 2 - button_width // 2

start_y = HEIGHT // 2 - 100   # nút đầu tiên
gap = 80                      # khoảng cách giữa các nút

play_rect    = pygame.Rect(center_x, start_y, button_width, button_height)
options_rect = pygame.Rect(center_x, start_y + gap, button_width, button_height)
quit_rect    = pygame.Rect(center_x, start_y + gap * 2, button_width, button_height)
back_rect = pygame.Rect(WIDTH//2 - 100, 550, 200, 60)

class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, 6)
        self.min = min_val
        self.max = max_val
        self.value = start_val
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200,200,200), self.rect)

        pos = (self.value - self.min) / (self.max - self.min)
        handle_x = self.rect.x + pos * self.rect.width
        pygame.draw.circle(screen, (255,255,255), (int(handle_x), self.rect.centery), 10)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 20)
            if handle_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            ratio = (x - self.rect.x) / self.rect.width
            self.value = self.min + ratio * (self.max - self.min)

def draw_menu():
    screen.blit(background, (0, 0))

    title = font_title.render("SNAKE GAME", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//3 - 50)))

    pygame.draw.rect(screen, GRAY, play_rect)
    pygame.draw.rect(screen, GRAY, quit_rect)
    pygame.draw.rect(screen, GRAY, options_rect)

    play_text = font_button.render("PLAY", True, WHITE)
    quit_text = font_button.render("QUIT", True, WHITE)
    options_text = font_button.render("OPTIONS", True, WHITE)

    how_to_play_text = how_to_play.render("TIP: You can play using the WASD keys or the arrow keys.", True, DARK)
    screen.blit(how_to_play_text, how_to_play_text.get_rect(center=(WIDTH//2, HEIGHT - 50)))

    screen.blit(play_text, play_text.get_rect(center=play_rect.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))
    screen.blit(options_text, options_text.get_rect(center=options_rect.center))

def draw_options():
    screen.fill((30,30,30))

    title = font_title.render("OPTIONS", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

    vol_text = volume_and_brightness.render("Volume", True, WHITE)
    bright_text = volume_and_brightness.render("Brightness", True, WHITE)

    screen.blit(vol_text, (250, 260))
    screen.blit(bright_text, (250, 360))

    volume_slider.draw(screen)
    brightness_slider.draw(screen)

    #Thoát ra menu
    pygame.draw.rect(screen, GRAY, back_rect)

    back_text = font_button.render("BACK", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_rect.center))

volume_slider = Slider(250, 300, 300, 0, 1, 0.5)
brightness_slider = Slider(250, 400, 300, 0.2, 1, 1)
current_screen = "MENU"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "MENU":

                if play_rect.collidepoint(event.pos):
                    main.main_game = main.MAIN(volume_slider.value)
                    main.run_game(volume_slider.value, brightness_slider.value)

                elif options_rect.collidepoint(event.pos):
                    current_screen = "OPTIONS"

                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if current_screen == "OPTIONS":
            volume_slider.handle_event(event)
            brightness_slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    current_screen = "MENU"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = "MENU"

    main.volume = volume_slider.value
    main.brightness = brightness_slider.value

    if current_screen == "MENU":
        draw_menu()
    elif current_screen == "OPTIONS":
        draw_options()

    brightness = brightness_slider.value
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0,0,0))
    overlay.set_alpha(int((1 - brightness) * 255))
    screen.blit(overlay, (0,0))

    pygame.display.update()