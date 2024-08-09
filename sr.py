import pygame
import sys
import random
from tkinter import messagebox, Tk


import sys
sys.path.insert(0, 'C:/Users/Dell/Desktop/Raghav\'s game/pgs4a-master/pgs4a-master/buildlib')


# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hridhaan's Stickman Game")

# Colors
STICKMAN_HEAD_COLOR = (0, 0, 0)  # Black head
STICKMAN_BODY_COLOR = (255, 0, 0)  # Red body
STICKMAN_ARM_COLOR = (0, 255, 0)  # Green arms
STICKMAN_LEG_COLOR = (0, 0, 255)  # Blue legs

# Load images
background_img1 = pygame.image.load('back.jpg')
background_img2 = pygame.image.load('back2.jpg')
background_img3 = pygame.image.load('back3.jpg')

# Load ball images
bronze_ball_img = pygame.image.load('bronze_ball.png')
silver_ball_img = pygame.image.load('silver_ball.png')
gold_ball_img = pygame.image.load('gold_ball.png')
bronze_ball_img = pygame.transform.scale(bronze_ball_img, (50, 50))
silver_ball_img = pygame.transform.scale(silver_ball_img, (50, 50))
gold_ball_img = pygame.transform.scale(gold_ball_img, (50, 50))

# Load static images
dinosaur_img = pygame.image.load('dinosaur.png')
carnivore_img = pygame.image.load('carnivore.png')
vegetable_img = pygame.image.load('vegetable.png')

# Scale images
animal_size = 60  # Increase size to 60x60
dinosaur_img = pygame.transform.scale(dinosaur_img, (animal_size, animal_size))
carnivore_img = pygame.transform.scale(carnivore_img, (animal_size, animal_size))
vegetable_size = 50  # Increase size to 50x50
vegetable_img = pygame.transform.scale(vegetable_img, (vegetable_size, vegetable_size))

# Stickman settings
stickman_pos = [WIDTH // 2, HEIGHT // 2]
stickman_speed = 5
stickman_speed_boost = 8
jump = False
jump_height = 10
jump_count = 10

# Obstacle and vegetable settings
animal_speed = 3
animal_list = []
vegetable_list = []
bronze_ball_list = []
silver_ball_list = []
gold_ball_list = []

# Add initial animals and vegetables
for i in range(5):
    x_pos = random.randint(0, WIDTH - animal_size)
    y_pos = random.randint(0, HEIGHT - animal_size)
    animal_list.append([x_pos, y_pos, random.choice([dinosaur_img, carnivore_img])])

for i in range(3):
    x_pos = random.randint(0, WIDTH - vegetable_size)
    y_pos = random.randint(0, HEIGHT - vegetable_size)
    vegetable_list.append([x_pos, y_pos, vegetable_img])

# Add initial bronze, silver, and gold balls
for i in range(3):
    x_pos = random.randint(0, WIDTH - 50)
    y_pos = random.randint(0, HEIGHT - 50)
    bronze_ball_list.append([x_pos, y_pos, bronze_ball_img])

for i in range(2):
    x_pos = random.randint(0, WIDTH - 50)
    y_pos = random.randint(0, HEIGHT - 50)
    silver_ball_list.append([x_pos, y_pos, silver_ball_img])

x_pos = random.randint(0, WIDTH - 50)
y_pos = random.randint(0, HEIGHT - 50)
gold_ball_list.append([x_pos, y_pos, gold_ball_img])

# Scoring and lives
score = 0
lives = 3
font = pygame.font.SysFont(None, 55)

# Watermark
watermark_font = pygame.font.SysFont(None, 30)

def draw_watermark(text):
    watermark = watermark_font.render(text, True, (255, 255, 255, 100))  # White watermark
    window.blit(watermark, (WIDTH - watermark.get_width() - 10, 10))

# Function to show game over message
def show_game_over(score):
    root = Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Game Over", f"Your score is: {score}")
    root.destroy()

# Zoom settings
zoom_level = 1.0
zoom_in = True
zoom_speed = 0.01

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys
    keys = pygame.key.get_pressed()
    current_speed = stickman_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        current_speed = stickman_speed_boost

    if keys[pygame.K_LEFT]:
        stickman_pos[0] -= current_speed
    if keys[pygame.K_RIGHT]:
        stickman_pos[0] += current_speed
    if not jump:
        if keys[pygame.K_UP]:
            stickman_pos[1] -= current_speed
        if keys[pygame.K_DOWN]:
            stickman_pos[1] += current_speed
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        if jump_count >= -jump_height:
            stickman_pos[1] -= (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        else:
            jump_count = jump_height
            jump = False

    # Move animals and vegetables
    for animal in animal_list:
        animal[1] += animal_speed
        if animal[1] > HEIGHT:
            animal[0] = random.randint(0, WIDTH - animal_size)
            animal[1] = -animal_size

    for vegetable in vegetable_list:
        vegetable[1] += animal_speed
        if vegetable[1] > HEIGHT:
            vegetable[0] = random.randint(0, WIDTH - vegetable_size)
            vegetable[1] = -vegetable_size
            score -= 1  # Decrease score if vegetable is missed

    for bronze_ball in bronze_ball_list:
        bronze_ball[1] += animal_speed
        if bronze_ball[1] > HEIGHT:
            bronze_ball[0] = random.randint(0, WIDTH - 50)
            bronze_ball[1] = -50
            score -= 1

    for silver_ball in silver_ball_list:
        silver_ball[1] += animal_speed
        if silver_ball[1] > HEIGHT:
            silver_ball[0] = random.randint(0, WIDTH - 50)
            silver_ball[1] = -50
            score -= 2

    for gold_ball in gold_ball_list:
        gold_ball[1] += animal_speed
        if gold_ball[1] > HEIGHT:
            gold_ball[0] = random.randint(0, WIDTH - 50)
            gold_ball[1] = -50
            score -= 3

    # Check for collisions
    stickman_rect = pygame.Rect(stickman_pos[0] - 20, stickman_pos[1] - 20, 40, 80)
    for animal in animal_list:
        animal_rect = pygame.Rect(animal[0], animal[1], animal_size, animal_size)
        if stickman_rect.colliderect(animal_rect):
            lives -= 1
            animal_list.remove(animal)
            x_pos = random.randint(0, WIDTH - animal_size)
            y_pos = random.randint(0, HEIGHT - animal_size)
            animal_list.append([x_pos, y_pos, random.choice([dinosaur_img, carnivore_img])])
            if lives == 0:
                show_game_over(score)
                running = False

    for vegetable in vegetable_list:
        vegetable_rect = pygame.Rect(vegetable[0], vegetable[1], vegetable_size, vegetable_size)
        if stickman_rect.colliderect(vegetable_rect):
            vegetable_list.remove(vegetable)
            x_pos = random.randint(0, WIDTH - vegetable_size)
            y_pos = random.randint(0, HEIGHT - vegetable_size)
            vegetable_list.append([x_pos, y_pos, vegetable_img])
            score += 2

    for bronze_ball in bronze_ball_list:
        bronze_ball_rect = pygame.Rect(bronze_ball[0], bronze_ball[1], 50, 50)
        if stickman_rect.colliderect(bronze_ball_rect):
            bronze_ball_list.remove(bronze_ball)
            x_pos = random.randint(0, WIDTH - 50)
            y_pos = random.randint(0, HEIGHT - 50)
            bronze_ball_list.append([x_pos, y_pos, bronze_ball_img])
            score += 1

    for silver_ball in silver_ball_list:
        silver_ball_rect = pygame.Rect(silver_ball[0], silver_ball[1], 50, 50)
        if stickman_rect.colliderect(silver_ball_rect):
            silver_ball_list.remove(silver_ball)
            x_pos = random.randint(0, WIDTH - 50)
            y_pos = random.randint(0, HEIGHT - 50)
            silver_ball_list.append([x_pos, y_pos, silver_ball_img])
            score += 2

    for gold_ball in gold_ball_list:
        gold_ball_rect = pygame.Rect(gold_ball[0], gold_ball[1], 50, 50)
        if stickman_rect.colliderect(gold_ball_rect):
            gold_ball_list.remove(gold_ball)
            x_pos = random.randint(0, WIDTH - 50)
            y_pos = random.randint(0, HEIGHT - 50)
            gold_ball_list.append([x_pos, y_pos, gold_ball_img])
            score += 3

    # Change background based on score
    if score >= 30:
        current_background_img = background_img3
    elif score >= 10:
        current_background_img = background_img2
    else:
        current_background_img = background_img1

    # Zoom effect
    if zoom_in:
        zoom_level += zoom_speed
        if zoom_level >= 1.5:
            zoom_in = False
    else:
        zoom_level -= zoom_speed
        if zoom_level <= 1.0:
            zoom_in = True

    zoomed_background = pygame.transform.scale(current_background_img, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))
    window.blit(zoomed_background, (0, 0))

    # Draw stickman with colors
    pygame.draw.circle(window, STICKMAN_HEAD_COLOR, (stickman_pos[0], stickman_pos[1]), 20)  # Head
    pygame.draw.line(window, STICKMAN_BODY_COLOR, (stickman_pos[0], stickman_pos[1] + 20), (stickman_pos[0], stickman_pos[1] + 60), 2)  # Body
    pygame.draw.line(window, STICKMAN_LEG_COLOR, (stickman_pos[0], stickman_pos[1] + 60), (stickman_pos[0] - 20, stickman_pos[1] + 80), 2)  # Left leg
    pygame.draw.line(window, STICKMAN_LEG_COLOR, (stickman_pos[0], stickman_pos[1] + 60), (stickman_pos[0] + 20, stickman_pos[1] + 80), 2)  # Right leg
    pygame.draw.line(window, STICKMAN_ARM_COLOR, (stickman_pos[0], stickman_pos[1] + 30), (stickman_pos[0] - 20, stickman_pos[1] + 40), 2)  # Left arm
    pygame.draw.line(window, STICKMAN_ARM_COLOR, (stickman_pos[0], stickman_pos[1] + 30), (stickman_pos[0] + 20, stickman_pos[1] + 40), 2)  # Right arm

    # Draw animals
    for animal in animal_list:
        window.blit(animal[2], (animal[0], animal[1]))

    # Draw vegetables
    for vegetable in vegetable_list:
        window.blit(vegetable[2], (vegetable[0], vegetable[1]))

    # Draw bronze, silver, and gold balls
    for bronze_ball in bronze_ball_list:
        window.blit(bronze_ball[2], (bronze_ball[0], bronze_ball[1]))

    for silver_ball in silver_ball_list:
        window.blit(silver_ball[2], (silver_ball[0], silver_ball[1]))

    for gold_ball in gold_ball_list:
        window.blit(gold_ball[2], (gold_ball[0], gold_ball[1]))

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, 50))

    # Draw watermark
    draw_watermark("This is Hridhaan's personal game")

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
