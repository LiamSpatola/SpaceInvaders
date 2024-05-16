import pygame as pg


class Laser:
    def __init__(self, x: int, y: int, img: str):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pg.mask.from_surface(self.img)
    
    def draw(self, window: pg.display):
        """ Draws the laser on the screen

        Parameters
        ----------
        window : pygame.display
            The window to draw the laser on
        """
        window.blit(self.img, (self.x, self.y))

    def move(self, vel: int):
        """ Moves the laser upward

        Parameters
        ----------
        vel : int
            The velocity at which the laser should move
        """
        self.y += vel

    def off_screen(self, height: int) -> bool:
        """ Checks if the laser is off screen

        Parameters
        ----------
        height : int
            The height of the screen
        
        Returns
        -------
        bool
            True if the player is on the screen, false if it is off the screen
        """
        return not(self.y <= height and self.y >= 0)
    
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
        """ Checks if the laser has collided with another object

        Parameters
        ----------
        obj : player OR enemy
            The object to check if the laser has collided with
        
        Returns
        -------
        bool
            True if there is a collision, false otherwise
        """
        return self.check_collision(obj)
