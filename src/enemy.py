from ship import Ship
from laser import Laser
import pygame as pg


class Enemy(Ship):
    def __init__(self, x: int, y: int, enemy_variant: str, health: int = 100):
        from main import ENEMY_ONE, ENEMY_ONE_LASERS, ENEMY_TWO, ENEMY_TWO_LASERS, ENEMY_THREE, ENEMY_THREE_LASERS, ENEMY_FOUR, ENEMY_FOUR_LASERS # Importing in the __init__ function to avoid a circular import with main.py


        super().__init__(x, y, health)

        # Determining which enemy variant should be used (to manipulate difficulty)
        ENEMY_VARIANTS = {
            "level_one": (ENEMY_ONE, ENEMY_ONE_LASERS),
            "level_two": (ENEMY_TWO, ENEMY_TWO_LASERS),
            "level_three": (ENEMY_THREE, ENEMY_THREE_LASERS),
            "level_four": (ENEMY_FOUR, ENEMY_FOUR_LASERS)
        }

        self.variant = enemy_variant
        self.ship_img, self.lasers_img = ENEMY_VARIANTS[self.variant]
        self.mask = pg.mask.from_surface(self.ship_img)

    def move(self, vel: int, direction: int, downward: bool):
        """ Moves the enemy
        
        Parameters
        ----------
        vel : int
            The number of pixels to move the enemy (its velocity)
        direction : int
            The direction which the enemy should move. 0 for moving left, 1 for moving right.
        downward : bool
            Whether the enemies should move downward. True if they should, false otherwise.
        """

        # Checking if the enemy should move down

        if downward:
            self.y += vel * 8
        
        if direction == 0:
            self.x -= vel
        else:
            self.x += vel

    def touchingWall(self, direction: int) -> bool:
        """ Checks if the enemy is touching the wall

        Parameters
        ----------
        direction : int
            The direction which to test for collisions with the wall. 0 for the left wall, 1 for the right wall.
        
        Returns
        -------
        bool
            True if in contact with the wall,false if not in contact.
        """
        from main import WIDTH # Importing in the touchingWall function to avoid a circular import with main.py

            
        if direction == 0: # Moving left
            if self.x < 0: # Checking for contact with the left wall
                return True
            else:
                return False
        else: # Moving right
            if (self.x + 75) > WIDTH: # Checking for contact with the right wall
                return True
            else:
                return False
            
    def shoot(self): # Overriding the parent class shoot function to make sure the lasers spawn at the base of the enemy
        """ 
        Shoots a laser if the cooldown is at 0, otherwise does nothing.
        """
        if self.cool_down_counter == 0:
            laser = Laser(self.x + (75 / 2) - 4, self.y + 75, self.lasers_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
