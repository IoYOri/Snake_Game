import pygame, sys, random
from pygame.math import Vector2

class FRUIT:
    def __init__(self): # Ham def __ init__ (self) la ham se duoc goi tu dong khi tao doi tuong tu class FRUIT
        # Tao diem X va Y
        self.x = random.randint(0, cell_number - 1) #Su dung thu vien random de ngau nhien chon ra mot so tu 1 - 19, viec khong lay 20 la de tranh doi tuong hien thi ra khoi man hinh
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y) #Su dung Vecto 2 chieu giup khai trien cac logic di chuyen doi tuong de dang hon so voi viec dung List
        self.randomize()

    def draw_fruit(self): #Ve trai cay
        # Ve hinh chu nhat
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size) #Tao hinh chu nhat o vi tri self_x, self_y va voi kich thuoc ca chieu dai lan chieu rong la cell_size (40px)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (255, 0, 0), fruit_rect) \\\Ve doi tuong fruit_rect len screen

    def randomize(self):
        self.x = random.randint(0, cell_number - 1) #Su dung thu vien random de ngau nhien chon ra mot so tu 1 - 19, viec khong lay 20 la de tranh doi tuong hien thi ra khoi man hinh
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y) #Su dung Vecto 2 chieu giup khai trien cac logic di chuyen doi tuong de dang hon so voi viec dung List
        
class SNAKE:
    def __init__ (self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0) #Vecto di chuyen phai
        self.new_block = False

        #Load hinh anh ran
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.mp3')
        self.right_sound = pygame.mixer.Sound('Sound/right.mp3')
        self.left_sound = pygame.mixer.Sound('Sound/left.mp3')
        self.up_sound = pygame.mixer.Sound('Sound/up.mp3')
        self.down_sound = pygame.mixer.Sound('Sound/down.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        # for block in self.body:
            # x_pos = block.x * cell_size
            # y_pos = block.y * cell_size
            #Tao mot hinh chu nhat
            # block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            #Ve hinh chu nhat
            # pygame.draw.rect(screen, (126, 166, 114), block_rect)

        #Thiet lap do hoa cho con ran
        for index, block in enumerate(self.body): # Code nay guip vua lay gia tri vua lay chi so
            # Thiet lap rect cho viec thiet lap vi tri
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # Xac dinh cac truong hop di chuyen cua con ran
            if index == 0: # Neu hinh chu nhat la phan tu dau => Dat hinh do thanh dau ran huong sang phai
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1: # Tìm phần tử cuối
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block #Tim khoi truoc do va tim quan he
                next_block = self.body[index - 1] - block #Tim khoi tiep theo va tim quan he
                if previous_block.x == next_block.x: # Neu trung x thi ran di chuyen doc
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y: # Neu trung y thi ran di chuyen ngang
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    #Cac truong hop goc cua cua con ran
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.y == 1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == 1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
           # else:
                #pygame.draw.rect(screen,(150,100,100), block_rect)

    def update_head_graphics(self):
        # Thuật toán ở dây dùng tọa độ đầu rắn trừ đi cho tọa độ phần thân nối tiếp đầu rắn
        # Sau đó kiểm tra tọa độ sau khi trừ trùng với các trường hợp nào để thay thế ảnh đầu con rắn
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1, 0): # Khi x = 1 thì rắn chắc chắn di chuyển sang phải => Ảnh đầu rắn sang phải
            self.head = self.head_right
        elif head_relation == Vector2(-1, 0):# Tương tự
            self.head = self.head_left
        elif head_relation == Vector2(0, 1):# Tương tự
            self.head = self.head_down
        elif head_relation == Vector2(0, -1): #Tương tự
            self.head = self.head_up

    def update_tail_graphics(self):
        tail_relation = self.body[len(self.body) - 1] - self.body[len(self.body) - 2]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_right
        if tail_relation == Vector2(-1, 0):
            self.tail = self.tail_left
        if tail_relation == Vector2(0, 1):
            self.tail = self.tail_down
        if tail_relation == Vector2(0, -1):
            self.tail = self.tail_up

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] 
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
            #Them than ran 
        else:
            body_copy = self.body[:-1] # Sao chep tat ca phan tu tru phan tu cuoi cung
            body_copy.insert(0, body_copy[0] + self.direction) #Then phan tu ngay phia truoc con ran
            #Logic cua 2 dong lenh tren thuc chat la loai bo phan tu cuoi cung va them phan tu lam dau con ran. 
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0) #Vecto di chuyen phai

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        #Khi tao doi tuong tu Class MAIN thi luon co hai doi tuong tu hai Class SNAKE va FRUIT
    
    def update(self): #Ham duy tri tro choi
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self): #Ham chua cac ham ve doi tuong
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):#Ham kiem tra cac hoat dong ran
        if self.fruit.pos == self.snake.body[0]: # Kiem tra neu dau ran trung voi thuc an
            #Doi lai vi tri thuc an
            self.fruit.randomize()
            #Them than cua con ran
            self.snake.add_block()
            #Them nhac
            self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()
        
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: #Kiem tra ran co o ngoai cua so hay khong (Thuat toan la kiem tra diem x,y cua dau ran co nam trong khoang tu 0 - 19 hay khong)
            self.game_over()

        #Kiem tra ran can chinh minh hay khong
        for block in self.snake.body[1:]: # Duyet cac phan tu tru dau ran
            if block == self.snake.body[0]: # Kiem tra neu than trung voi dau ran
                self.game_over()
    
    def game_over(self):
        self.snake.reset()
    
    def draw_grass(self): # Ve co
        grass_color = (167,209,61) 
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_int = len(self.snake.body) - 3
        score_text = str(len(self.snake.body) - 3 )
        try:
            with open("highscore.txt", "r") as f:
                content = f.read().strip()   # bỏ khoảng trắng, xuống dòng
                if content:                  # nếu không rỗng
                    saved_score = int(content)
                else:
                    saved_score = 0
        except FileNotFoundError:
            saved_score = 0

        if score_int > saved_score:
            with open("highscore.txt", "w") as f:
                f.write(str(score_text))

        highscore_surface = game_font.render(f"Highscore: {saved_score}", True, (56, 74, 12))
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)

        score_rect = score_surface.get_rect(center = (score_x, score_y))
        highscore_rect = highscore_surface.get_rect(center = (score_x - 40, score_y - 40))

        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery)) #Hien thi anh trai tao ngay ben canh diem
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 8,apple_rect.height)

        
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        screen.blit(highscore_surface, highscore_rect)

    def input(self):
        if event.type == pygame.KEYDOWN: # Su kien khi nhap input ban phim
            if event.key == pygame.K_UP: # Neu la phim mui ten len
                if self.snake.direction.y != 1: # Kiem tra neu y la 1 thi khong input di len
                    self.snake.direction = Vector2(0, -1) # X khong doi, Y giam thi ran di len
                    self.snake.up_sound.play()
            if event.key == pygame.K_DOWN: # Neu la phim mui ten xuong
                if self.snake.direction.y != -1: # Kiem tra neu y la -1 thi khong input di xuong
                    self.snake.direction = Vector2(0, 1) # X khong doi, Y tang thi ran di xuong
                    self.snake.down_sound.play()
            if event.key == pygame.K_LEFT: # Neu la phim mui ten trai
                if self.snake.direction.x != 1: # Kiem tra neu x la 1 thi khong input sang trai
                    self.snake.direction = Vector2(-1, 0) # Y khong doi, X giam thi ran di sang trai
                    self.snake.left_sound.play()
            if event.key == pygame.K_RIGHT: # Neu la phim mui ten phai
                if self.snake.direction.x != -1: # Kiem tra neu x la -1 thi khong input di phai
                    self.snake.direction = Vector2(1, 0) # Y khong doi, X tang thi ran di sang phai
                    self.snake.right_sound.play()

pygame.mixer.pre_init(44100, -16, 2 ,512) #pygame.mixer.pre_init chiu trach nhiem trong viec khong lam am thanh bi delay
pygame.init() # Khoi dong module pygame 

cell_size = 40 #Kich thuoc o (40 px)
cell_number = 20 #So luong o tren 1 hang (Hoac cot)
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number)) #Cua so tro choi
clock = pygame.time.Clock() #Gioi han so vong chay cua lenh While(FPS)
apple = pygame.image.load('Graphics/apple.png').convert_alpha() #Lay hinh anh va chuyen dinh dang
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

pygame.display.set_caption('SnakeGame')
pygame.display.set_icon(apple)
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT #Su kien cho ran di chuyen
pygame.time.set_timer(SCREEN_UPDATE, 200) #Su kien se kich hoat sau 150 mili giay

def run_game():
    global event

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == SCREEN_UPDATE:
                main_game.update()

            main_game.input()

        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

#Update cua so
#while True:
    # Vong lap su kien
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT: # Neu su kien la thoat khoi tro choi bang dau X tren cua so
            #pygame.quit()
            #sys.exit() # sys.exit dung de ket thuc bat cu doan ma dang duoc chay
        #if event.type == SCREEN_UPDATE:
            #main_game.update() #Ran di chuyen
        #main_game.input()
    #screen.fill((175,215,70)) # Thay doi mau screen voi gia tri RGB
    #main_game.draw_elements()
    # Ve cac phan tu cua tro choi
    #pygame.display.update()
    #clock.tick(60) #Gioi han 60FPS