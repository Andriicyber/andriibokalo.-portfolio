import pygame
import os
import random
import time

pygame.init()

WIDTH, HEIGHT = 900, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Game")

background_image_path = "C:\\Project1\\Images\\back.jpg"
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

goose_image_path = "C:\\Project1\\Images\\Goose.jpg"
goose_image = pygame.image.load(goose_image_path)
goose_width, goose_height = 50, 50
goose_image = pygame.transform.scale(goose_image, (goose_width, goose_height))
goose_x, goose_y = 10, 10
goose_speed = 4

bg_x = 0
bg_speed = 3

airplane_image_path = "C:\\Project1\\airplane\\airplane.png"

def create_airplane():
    airplane_size = (20, 20)
    airplane = pygame.image.load(airplane_image_path).convert_alpha()
    airplane_rect = pygame.Rect(WIDTH, random.randint(50, HEIGHT-50), *airplane_size)
    airplane_move = [random.randint(-8, -4), 0]
    return [airplane, airplane_rect, airplane_move]

def create_bonus():
    bonus_size = (30, 30)
    bonus = pygame.Surface(bonus_size)
    Color_Green = (0, 255, 0)  
    bonus.fill(Color_Green)  
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 5)]
    return [bonus, bonus_rect, bonus_move]

airplanes = []
bonuses = []

last_airplane_time = time.time()
airplane_interval = 2

Create_Bonus = pygame.USEREVENT + 2
pygame.time.set_timer(Create_Bonus, 3000)

goose_hit = False

goose_sound = pygame.mixer.Sound('C:\\Project1\\Sounds\\Goose.mp3')
goose_sound.play()

font = pygame.font.SysFont('Verdana', 20)
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == Create_Bonus:
            bonuses.append(create_bonus())

    window.fill((255, 255, 255))
    window.blit(background_image, (bg_x, 0))
    window.blit(background_image, (bg_x + WIDTH, 0))

    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0

    window.blit(goose_image, (goose_x, goose_y))

    player_rect = pygame.Rect(goose_x, goose_y, goose_width, goose_height)

    for airplane in airplanes:
        if player_rect.colliderect(airplane[1]):  
            print("Boom")
            goose_hit = True

    for bonus in bonuses:
        if player_rect.colliderect(bonus[1]):  
            print("Hell Yeah")
            bonuses.pop(bonuses.index(bonus))  
            score += 1  

    for airplane in airplanes:
        airplane[1].move_ip(airplane[2])
        window.blit(airplane[0], airplane[1])

    airplanes = [airplane for airplane in airplanes if airplane[1].right > 0]

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        window.blit(bonus[0], bonus[1])

    bonuses = [bonus for bonus in bonuses if bonus[1].top <= HEIGHT]

    current_time = time.time()
    if current_time - last_airplane_time > airplane_interval:
        airplanes.append(create_airplane())
        last_airplane_time = current_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        goose_x -= goose_speed
    if keys[pygame.K_RIGHT]:
        goose_x += goose_speed
    if keys[pygame.K_UP]:
        goose_y -= goose_speed
    if keys[pygame.K_DOWN]:
        goose_y += goose_speed

    goose_x = max(0, min(goose_x, WIDTH - goose_width))
    goose_y = max(0, min(goose_y, HEIGHT - goose_height))

    if goose_hit:
        running = False

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (WIDTH - 100, 20))

    pygame.time.delay(3)
    pygame.display.flip()

pygame.quit()
