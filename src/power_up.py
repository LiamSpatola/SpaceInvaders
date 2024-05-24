from ship import Ship
import pygame as pg


class PowerUp(Ship):
    def __init__(self, x: int, y: int, img, time_alive: int, variant: str):
        super().__init__(x, y)
        self.ship_img = img
        self.time_alive = time_alive # in frames
        self.variant = variant
        self.mask = pg.mask.from_surface(self.ship_img)

    def countdown(self) -> bool:
        """ Counts down the timer for the time to keep the powerup

        Returns
        -------
        bool
            True if still alive, false otherwise
        """
        if self.time_alive <= 0:
            return False
        else:
            self.time_alive -= 1
            return True
        
    def check_collision(obj1, obj2) -> bool:
        """ Checks whether an object overlaps another

        Parameters
        ----------
        obj1
            The object to be checked for collision with obj2
        obj2
            The object to be checked for collision with obj1

        Returns
        -------
        bool
            True if the objects have collided, false if they haven't
        """

        x_offset = obj2.x - obj1.x
        y_offset = obj2.y - obj1.y

        return obj1.mask.overlap(obj2.mask, (x_offset, y_offset)) is not None # Returning true for a collision, false for no collision
    
    def collision(self, obj) -> bool:
        """ Checks if the power up has collided with another object

        Parameters
        ----------
        obj : laser
            The object to check if the power up has collided with
        
        Returns
        -------
        bool
            True if there is a collision, false otherwise
        """
        return self.check_collision(obj)
