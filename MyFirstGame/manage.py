import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("My Game")

icon = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\mushroom.png").convert_alpha()
pygame.display.set_icon(icon)
bg = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\Game_background.png").convert_alpha()
bg_sound = pygame.mixer.Sound(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\sounds\396175_3307719.mp3")
bg_sound.play()
jump_sound = pygame.mixer.Sound(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\sounds\pryjok-mario.mp3")
game_over_sound = pygame.mixer.Sound(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\sounds\mario-smert.mp3")

player_right1 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_right1.png").convert_alpha()
player_right2 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_right2.png").convert_alpha()
player_right3 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_right3.png").convert_alpha()
player_right4 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_right4.png").convert_alpha()
player_left1 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_left1.png").convert_alpha()
player_left2 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_left2.png").convert_alpha()
player_left3 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_left3.png").convert_alpha()
player_left4 = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_left4.png").convert_alpha()
player_straight = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\player_straight.png").convert_alpha()
enemy_right = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\ghost_right.png").convert_alpha()
enemy_left = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\ghost_left.png").convert_alpha()
bullet_img = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\bullet.png").convert_alpha()
bullet_left = pygame.image.load(r"C:\Users\VICTUS\PycharmProjects\MyFirstGame\assets\bullet_left.png").convert_alpha()

walk_right = [player_right1, player_right2, player_right3, player_right4]
walk_left = [player_left1, player_left2, player_left3, player_left4]
straight = [player_straight]

player_animation_count = 0
bg_x = 0
player_x = 10
player_y = 570
player_speed = 5
is_jump = False
jump_count = 9
last_shot_time = 0
shoot_delay = 900

enemy_speed = 5
enemies = []
score = 0
direction = "right"


bullets = []
bullet_speed = 10

enemy_spawn_timer = 0


def reset_game():
    global player_x, player_y, bg_x, enemies, is_jump, jump_count, score, game_over
    player_x, player_y = 10, 570
    bg_x = 0
    enemies = []
    is_jump = False
    jump_count = 9
    score = 0
    bullets.clear()
    game_over = False


def spawn_enemy():
    side = random.choice(["left", "right"])
    x = 1280 if side == "right" else -50
    enemies.append({"x": x, "y": 570, "side": side})


def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


running = True
game_over = False

while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1280, 0))

    if not game_over:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 30:
            spawn_enemy()
            enemy_spawn_timer = 0

        for enemy in enemies[:]:
            if enemy["side"] == "left":
                enemy["x"] += enemy_speed
                enemy_img = enemy_left
            else:
                enemy["x"] -= enemy_speed
                enemy_img = enemy_right

            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_img.get_width(), enemy_img.get_height())
            screen.blit(enemy_img, (enemy["x"], enemy["y"]))

            player_rect = pygame.Rect(player_x, player_y, player_straight.get_width(), player_straight.get_height())
            if check_collision(player_rect, enemy_rect):
                game_over_sound.play()
                game_over = True

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 10)
                if check_collision(bullet_rect, enemy_rect):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    score += 1
                    break

            if enemy["x"] < -50 or enemy["x"] > 1280:
                enemies.remove(enemy)

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 200:
            player_x -= player_speed
            direction = "left"
            screen.blit(walk_left[player_animation_count], (player_x, player_y))
            player_animation_count += 1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < 1080:
            player_x += player_speed
            direction = "right"
            screen.blit(walk_right[player_animation_count], (player_x, player_y))
            player_animation_count += 1
        else:
            screen.blit(straight[0], (player_x, player_y))
            player_animation_count = 0

        if player_animation_count >= len(walk_right):
            player_animation_count = 0

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
                jump_sound.play()
        else:
            if jump_count >= -9:
                player_y -= (jump_count ** 2) / 2 if jump_count > 0 else -(jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_f] and current_time - last_shot_time > shoot_delay:
            bullet_x = player_x + (player_straight.get_width() if direction == "right" else 0)
            bullet_y = player_y + player_straight.get_height() // 2 - bullet_img.get_height() // 2
            bullets.append({"x": bullet_x, "y": bullet_y, "direction": direction})
            last_shot_time = current_time

        for bullet in bullets[:]:
            if bullet["direction"] == "right":
                bullet["x"] += bullet_speed
                screen.blit(bullet_img, (bullet["x"], bullet["y"]))
            else:
                bullet["x"] -= bullet_speed
                screen.blit(bullet_left, (bullet["x"], bullet["y"]))

            if bullet["x"] < 0 or bullet["x"] > 1280:
                bullets.remove(bullet)

        if bg_x <= -1280:
            bg_x = 0
        elif bg_x > 0:
            bg_x = -1280

    else:
        screen.fill((0, 0, 0))
        draw_text(f"Вы проиграли, ваш счет: {score}", 100, (255, 0, 0), 250, 200)
        draw_text("Нажмите R для перезапуска", 50, (255, 255, 255), 420, 300)
        draw_text("Нажмите Q для выхода", 50, (255, 255, 255), 420, 400)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    draw_text(f"Счет: {score}", 36, (255, 255, 255), 10, 10)

    pygame.display.update()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
