import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)   # Màu cho thức ăn đặc biệt

# Cài đặt kích thước màn hình
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Cài đặt đồng hồ
clock = pygame.time.Clock()

# Các thông số cho rắn
snake_block = 20
snake_speed = 8

level = 1
count = 0

font_style = pygame.font.SysFont(None, 50)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH/6, HEIGHT/3])

def gameLoop():
    global snake_speed, level, count

    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 2

    # Thức ăn thường
    foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

    # Các biến cho thức ăn đặc biệt
    special_food_exists = False
    special_food_x = None
    special_food_y = None
    special_food_spawn_time = 0  # thời điểm spawn (millisecond)

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press C to replay or Press Q to exit!", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Kiểm tra va chạm biên
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        # Vẽ thức ăn thường
        pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])
        
        # ---- Xử lý thức ăn đặc biệt ----
        # Nếu level đạt từ 2 trở lên thì spawn thức ăn đặc biệt nếu chưa có
        if level >= 2 and not special_food_exists:
            # Tính vị trí sao cho khít với lưới
            special_food_x = round(random.randrange(0, WIDTH - snake_block*4) / snake_block) * snake_block
            special_food_y = round(random.randrange(0, HEIGHT - snake_block*4) / snake_block) * snake_block
            special_food_spawn_time = pygame.time.get_ticks()
            special_food_exists = True

        # Tính thời gian tồn tại của thức ăn đặc biệt: 
        # 20 giây cho level 2, mỗi level tăng thêm giảm 2 giây, nhưng không dưới 4 giây
        special_food_lifetime = max(20 - (level - 2) * 2, 4)  # tính bằng giây

        # Nếu thức ăn đặc biệt đã xuất hiện, kiểm tra thời gian tồn tại
        if special_food_exists:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - special_food_spawn_time) / 1000  # chuyển sang giây

            if elapsed_time > special_food_lifetime:
                # Hết thời gian, loại bỏ thức ăn đặc biệt
                special_food_exists = False
            else:
                # Tạo hiệu ứng nhấp nháy: mỗi 500ms toggle hiển thị
                if (current_time // 2000) % 2 == 0:
                    pygame.draw.rect(screen, BLUE, [special_food_x, special_food_y, snake_block * 4, snake_block * 4])
        # ---------------------------------

        # Vẽ rắn
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Kiểm tra va chạm với thân
        for segment in snake_List[:0]:
            if segment == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        pygame.display.update()

        # Xử lý khi ăn thức ăn thường
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            snake_speed += 1
            # Giả sử khi ăn đủ số thức ăn nhất định, level sẽ tăng
            level += 1

        # Xử lý khi ăn thức ăn đặc biệt
        if special_food_exists:
            # Kiểm tra va chạm: nếu đầu rắn nằm trong vùng của thức ăn đặc biệt
            if (x1 >= special_food_x and x1 < special_food_x + snake_block*4) and \
               (y1 >= special_food_y and y1 < special_food_y + snake_block*4):
                special_food_exists = False
                # Tăng thêm điểm (ở đây tăng độ dài và tốc độ; bạn có thể thay đổi theo ý muốn)
                Length_of_snake += 2  # tăng thêm độ dài hơn so với thức ăn thường
                snake_speed += 2

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

gameLoop()
