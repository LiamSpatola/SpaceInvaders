from ship import Ship
import pygame as pg


class Player(Ship):
    def __init__(self, x: int, y: int, health:int = 100):
        from main import PLAYER_SHIP, PLAYER_LASERS # Importing in the __init__ function to avoid a circular import with main.py


        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.lasers_img = PLAYER_LASERS
        self.mask = pg.mask.from_surface(self.ship_img)
        self.health = health

    def move_lasers(self, vel: int, objs: list): # Overriding the parent class move_lasers function to modify the collision behaviours with enemies
        """ Moving the lasers
        
        Parameters
        ----------
        vel : int
            The velocity of the lasers
        objs : list
            The objects which the laser can collide with (i.e. the objects which it can hurt)
        """
        from main import HEIGHT, KILLED_ENEMY_SFX # Importing in the move_lasers function to avoid a circular import with main


        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        KILLED_ENEMY_SFX.play()
                        obj.health -= 10
                        if obj.health <= 0:
                            objs.remove(obj)

                        # To fix errors where the laser is removed twice, and so isn't in the list anymore and throws a ValueError
                        try:
                            self.lasers.remove(laser)
                        except ValueError:
                            pass

    def draw(self, window): # Overriding the parent class' draw function to also render the healthbar
        """ Drawing the player and healthbar on the screen

        Parameters
        ----------
        window : pygame.window
            The window to draw the elements on
        """
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        """ Draws a healthbar on the screen below the player.

        Parameters
        ----------
        window : pygame.window
            The window to draw the healthbar on
        """
        pg.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10)) # Drawing the red rectangle
        pg.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / 100), 10)) # Drawing the green rectangle
