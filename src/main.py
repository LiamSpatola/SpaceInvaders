from player import Player
from enemy import Enemy
from button import Button
import pygame as pg
import os
import random


# Initializing the screen dimensions, and setting up the main window
WIDTH, HEIGHT = 750, 750
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Invaders by Liam Spatola")
pg.font.init()

# Importing the game assets and resizing them
BG = pg.image.load(os.path.join("..", "assets", "images", "background.jpg"))
BG = pg.transform.scale(BG, (750, 750))

PLAYER_SHIP = pg.image.load(os.path.join("..", "assets", "images", "player_ship.png"))
PLAYER_SHIP = pg.transform.scale(PLAYER_SHIP, (75, 75))

PLAYER_LASERS = pg.image.load(os.path.join("..", "assets", "images", "player_lasers.png"))
PLAYER_LASERS = pg.transform.scale(PLAYER_LASERS, (8, 32))

ENEMY_ONE = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_one.png"))
ENEMY_ONE = pg.transform.scale(ENEMY_ONE, (75, 75))

ENEMY_ONE_LASERS = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_one_lasers.png"))
ENEMY_ONE_LASERS = pg.transform.scale(ENEMY_ONE_LASERS, (8, 32))

ENEMY_TWO = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_two.png"))
ENEMY_TWO = pg.transform.scale(ENEMY_TWO, (75, 75))

ENEMY_TWO_LASERS = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_two_lasers.png"))
ENEMY_TWO_LASERS = pg.transform.scale(ENEMY_TWO_LASERS, (8, 32))

ENEMY_THREE = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_three.png"))
ENEMY_THREE = pg.transform.scale(ENEMY_THREE, (75, 75))

ENEMY_THREE_LASERS = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_three_lasers.png"))
ENEMY_THREE_LASERS = pg.transform.scale(ENEMY_THREE_LASERS, (8, 32))

ENEMY_FOUR = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_four.png"))
ENEMY_FOUR = pg.transform.scale(ENEMY_FOUR, (75, 75))

ENEMY_FOUR_LASERS = pg.image.load(os.path.join("..", "assets", "images", "enemy_level_four_lasers.png"))
ENEMY_FOUR_LASERS = pg.transform.scale(ENEMY_FOUR_LASERS, (8, 32))

BUTTON = pg.image.load(os.path.join("..", "assets", "images", "button.png"))

# Setting up the sfx and background music
pg.mixer.init()
LEVEL_UP_SFX = pg.mixer.Sound("..\\assets\\sounds\\level_up.wav")
LIFE_LOST_SFX = pg.mixer.Sound("..\\assets\\sounds\\life_lost.wav")
KILLED_ENEMY_SFX = pg.mixer.Sound("..\\assets\\sounds\\enemy_shot.wav")
LASER_FIRED_SFX = pg.mixer.Sound("..\\assets\\sounds\\laser.wav")
HURT_SFX = pg.mixer.Sound("..\\assets\\sounds\\hurt.wav")
os.chdir("..\\assets\\sounds")
pg.mixer.music.load("background_music.mp3")
os.chdir("..\\..\\src")

# Setting up the fonts
MAIN_FONT = pg.font.Font("..\\assets\\fonts\\main_font.otf", 50)
PLAY_BUTTON_FONT = pg.font.Font("..\\assets\\fonts\\main_font.otf", 100)
TITLE_FONT = pg.font.Font("..\\assets\\fonts\\main_font.otf", 125)

def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        play_button = Button(WIN.get_width() / 2 - BUTTON.get_width() / 2, 500, BUTTON, "PLAY", PLAY_BUTTON_FONT)
        play_button.draw(WIN)
        title_line_1 = TITLE_FONT.render("SPACE", 1, (255, 255, 255))
        title_line_2 = TITLE_FONT.render("INVADERS", 1, (255, 255, 255))
        WIN.blit(title_line_1, (WIN.get_width() / 2 - title_line_1.get_width() / 2, 100))
        WIN.blit(title_line_2, (WIN.get_width() / 2 - title_line_2.get_width() / 2, 200))
        WIN.blit(PLAYER_SHIP, (WIN.get_width() / 2 - PLAYER_SHIP.get_width() / 2, 375))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
        
        pos = pg.mouse.get_pos()
        if play_button.clicked(pos):
            run = False
        
        pg.display.flip()
    main()
    pg.mixer.music.play(-1, 0.0)

def game_over():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        play_again_button = Button(WIN.get_width() / 2 - BUTTON.get_width() / 2, 500, BUTTON, "PLAY AGAIN", MAIN_FONT)
        play_again_button.draw(WIN)
        game_over_line_1 = TITLE_FONT.render("GAME", 1, (255, 255, 255))
        game_over_line_2 = TITLE_FONT.render("OVER", 1, (255, 255, 255))
        WIN.blit(game_over_line_1, (WIN.get_width() / 2 - game_over_line_1.get_width() / 2, 100))
        WIN.blit(game_over_line_2, (WIN.get_width() / 2 - game_over_line_2.get_width() / 2, 200))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
        
        pos = pg.mouse.get_pos()
        if play_again_button.clicked(pos):
            run = False
            break
        
        pg.display.flip()
    main()

def main():
    pg.display.flip()
    run = True
    level = 0
    lives = 3
    player_vel = 5
    
    # Setting enemy variables to manipulate difficulty
    enemies = []
    wave_length = 3
    enemy_vel = 0.9
    laser_vel = 7
    player_laser_vel = -7 # Setting as a negative to make the lasers fly upward, rather than downwards off the screen

    # Setting enemy movement variables for moving enemies
    move_direction = 0
    move_downward = False

    # Creating the player ship instance of the ship class
    player_ship = Player((WIDTH / 2) - (75 / 2), 650)

    # Initializing the clock object
    FPS = 60
    clock = pg.time.Clock()

    def redraw_window():
        """ 
        Redraws the window, refreshes the display, and renders all relevant elements.
        """
        # Rendering the background
        WIN.blit(BG, (0, 0))
        
        # Rendering the lives and level labels
        lives_label = MAIN_FONT.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = MAIN_FONT.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # Rendering the enemies
        for enemy in enemies:
            enemy.draw(WIN)           

        # Rendering the player ship
        player_ship.draw(WIN)
        
        pg.display.update()
    
    while run:
        clock.tick(FPS)

        # Checking if there are any more enemies, and if there are none, beginning a new level
        if len(enemies) == 0:
            level += 1
            enemy_vel += 0.1
            new_enemy_x = 112
            new_enemy_y = 75
            number_in_current_line = 0
            LEVEL_UP_SFX.play()

            # Capping the wave length at level 7
            if level <= 7:
                wave_length += 4

            for i in range(wave_length):
                # Determining which variant of enemy to spawn depending on level (to change difficulty)
                if level <= 3:
                    enemy = Enemy(new_enemy_x, new_enemy_y, random.choice(["level_one", "level_one", "level_one", "level_two"]))
                elif level > 3 and level <= 5:
                    enemy = Enemy(new_enemy_x, new_enemy_y, random.choice(["level_one", "level_two", "level_two", "level_three"]))
                elif level > 5 and level <= 7:
                    enemy = Enemy(new_enemy_x, new_enemy_y, random.choice(["level_two", "level_three", "level_three", "level_four"]))
                elif level > 7:
                    enemy = Enemy(new_enemy_x, new_enemy_y, random.choice(["level_three", "level_four", "level_four", "level_four"]))
                # enemy = Enemy(new_enemy_x, new_enemy_y, random.choice(["level_one", "level_two", "level_three", "level_four"]))

                # Checking whether there is yet 7 enemies in the line, and if so, making a new line
                if number_in_current_line >= 6:
                    new_enemy_y += 75
                    new_enemy_x = 112 - 75
                    number_in_current_line = -1
                
                # Setting up the variables for the next enemy
                new_enemy_x += 75
                number_in_current_line += 1

                enemies.append(enemy)    

        # Enabling the movement of the player ship using the arrow keys or A and D keys and shooting using the space bar
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and player_ship.x - player_vel > 0 or keys[pg.K_LEFT] and player_ship.x - player_vel > 0: # Move left
            player_ship.x -= player_vel
        if keys[pg.K_d] and player_ship.x + player_vel + 75 < WIDTH or keys[pg.K_RIGHT] and player_ship.x + player_vel + 75 < WIDTH: # Move right
            player_ship.x += player_vel
        if keys[pg.K_SPACE]:
            player_ship.shoot()
            LASER_FIRED_SFX.play()

        # Seeing if any enemies are touching the wall, and if so, reversing the direction, and moving downward
        for enemy in enemies:
            if enemy.touchingWall(move_direction):
                move_downward = True

                if move_direction == 0:
                    move_direction = 1
                else:
                    move_direction = 0
                break
            else:
                continue

        for enemy in enemies[:]:
            # Moving the enemy
            enemy.move(enemy_vel, move_direction, move_downward)
            enemy.move_lasers(laser_vel, player_ship)

            # Randomnly picking when to shoot based on the enemy level
            match enemy.variant:
                case "level_one":
                    if random.randrange(0, (8 * 60)) == 1:
                        enemy.shoot()
                case "level_two":
                    if random.randrange(0, (6 * 60)) == 1:
                        enemy.shoot()
                case "level_three":
                    if random.randrange(0, (4 * 60)) == 1:
                        enemy.shoot()
                case "level_four":
                    if random.randrange(0, (2 * 60)) == 1:
                        enemy.shoot()

            # Seeing if any enemies are off the bottom of the screen, and killing them
            if (enemy.y + 75) > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player_ship.move_lasers(player_laser_vel, enemies)

        move_downward = False

        redraw_window()

        # Checking if the player has zero health and subtracting a life
        if player_ship.health <= 0:
            lives -= 1
            player_ship.health = 100
            LIFE_LOST_SFX.play()

        # Checking if the window is closed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                exit(0)

        # Checking if the player lost
        if lives <= 0:
            run = False
    game_over()
    pg.mixer.stop()
    exit(0)

main_menu()
main()
