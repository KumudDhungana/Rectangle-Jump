import pygame
import time
import random
import math

# Initialize pygame and font
pygame.init()
pygame.font.init()

# Setting window
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump the Rectangle Game")

# Player settings
P_WIDTH = 40
P_HEIGHT = 40
P_JUMP = 20
P_GRAVITY = 1


# Obstacle settings
OBSTACLE_MIN_WIDTH = 40
OBSTACLE_MAX_WIDTH = 80
OBSTACLE_MIN_HEIGHT = 30
OBSTACLE_MAX_HEIGHT = 80
OBSTACLE_SPEED = 7
OBSTACLE_COLOR = (255, 255, 0)

# Fonts
FONT = pygame.font.SysFont("comicsans", 30)

# Background image
bg = pygame.image.load("galaxbackground.png").convert()
tiles = math.ceil(WIDTH / bg.get_width()) + 1

# Double jump limit
MAX_DOUBLE_JUMPS = 5  
remaining_double_jumps = MAX_DOUBLE_JUMPS  

def generate_obstacle():
    x_pos = WIDTH
    y_pos = HEIGHT - 30
    obstacle_height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
    obstacle_width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
    obstacle = pygame.Rect(x_pos, y_pos - obstacle_height, obstacle_width, obstacle_height)
    return obstacle

def draw(player, score, obstacles, scroll):
    # Draw the scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg.get_width() + scroll, 0))
    
    # Draw the player
    pygame.draw.rect(screen, (255, 0, 0), player)

    
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
        
    
    score_text = FONT.render(f"Score: {round(score)}", 1, (255, 255, 255))
    screen.blit(score_text, (900, 10))
    
    
    double_jump_text = FONT.render(f"Double Jumps Left: {remaining_double_jumps}", 1, (255, 255, 255))
    screen.blit(double_jump_text, (20, 10))

    if remaining_double_jumps > 0 :
        instruction_text = FONT.render("Press UP to Double Jump", 1, (0, 255, 0))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width()//2, 80))
    else:
        instruction_text = FONT.render("No Double Jumps Left", 1, (255, 0, 0))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width()//2, 80))

    pygame.display.update()

def main():
    global remaining_double_jumps
    MAX_DOUBLE_JUMPS = 5  
    remaining_double_jumps = MAX_DOUBLE_JUMPS  
    MAX_DOUBLE_JUMPS1 = 5
    clock = pygame.time.Clock()
    start_time = time.time()
    player = pygame.Rect(100, HEIGHT - P_HEIGHT - 30, P_WIDTH, P_HEIGHT)
    JUMP_VEL = 0
    is_jumping = False
    obstacles = []
    score = 0
    hit = False
    scroll = 0
    up_pressed = False
    
    while True:
        clock.tick(60)  
        
        elapsed_time = time.time() - start_time
        score = elapsed_time * 10 
        scroll = scroll - 6
        
        if scroll < -bg.get_width():
            scroll = 0
        
        if random.randint(1, 120) == 1:
            obstacles.append(generate_obstacle())

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

       
        if keys[pygame.K_SPACE]:
            if not is_jumping:  
                JUMP_VEL = -P_JUMP
                is_jumping = True

        # Handle double jump (up key)
        if keys[pygame.K_UP] and not up_pressed and remaining_double_jumps > 0 and is_jumping:
            
            JUMP_VEL = -P_JUMP
            remaining_double_jumps -= 1  
            MAX_DOUBLE_JUMPS1 -= 1
            up_pressed = True  

        
        if not is_jumping:
            up_pressed = False

        
        if is_jumping:
            player.y += JUMP_VEL
            JUMP_VEL += P_GRAVITY  

            
            if player.y >= HEIGHT - P_HEIGHT - 30:
                player.y = HEIGHT - P_HEIGHT - 30
                is_jumping = False
                remaining_double_jumps = MAX_DOUBLE_JUMPS1  

        
        for obstacle in obstacles:
            obstacle.x -= OBSTACLE_SPEED
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)

        for obstacle in obstacles:
            if player.colliderect(obstacle):
                hit = True
                break
        
        if hit:
            lost_text = FONT.render("You Lost!", 1, "red")
            score_text = FONT.render(f"Your Score: {round(score)}", 1, "red")
            retry_text = FONT.render("Press X to Retry", 1, "red")
            screen.fill((0, 0, 0))  
            screen.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 30))
            screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 60))
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:
                            main()  
                        else:
                            pygame.quit()
                            quit()

        
        screen.fill((0, 0, 0)) 
        draw(player, score, obstacles, scroll)

if __name__ == "__main__":
    main()
