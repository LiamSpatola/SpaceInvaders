from laser import Laser


class Ship:
    COOLDOWN = 20 # Setting the cooldown for laser shooting to 20 frames (1/3 of a second)

    def __init__(self, x: int, y: int, health:int = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lasers_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        """ Draws the ship on the window

        Parameters
        ----------
        window : pg.display
            The window to draw the ship on
        """
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel: int, obj):
        """ Moving the lasers
        
        Parameters
        ----------
        vel : int
            The velocity of the lasers
        obj : object
            The object which the laser can collide with (i.e. the object which it can hurt)
        """
        from main import HEIGHT, HURT_SFX # Importing in the move_lasers function to avoid a circular import with main


        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                HURT_SFX.play()
                obj.health -= 10
                self.lasers.remove(laser)
    
    def get_width(self) -> int:
        """ Returns the width of the ship

        Returns
        -------
        int
            The width of the ship
        """
        return int(self.ship_img.get_width())

    def get_height(self) -> int:
        """ Returns the height of the ship

        Returns
        -------
        int
            The height of the ship
        """
        return int(self.ship_img.get_height())
    
    def cooldown(self):
        """
        Resetting the cooldown counter if it is above the threshold, incrementing it otherwise (if it is not equal to zero), or if it is zero, doing nothing.
        """
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        """ 
        Shoots a laser if the cooldown is at 0, otherwise does nothing.
        """
        if self.cool_down_counter == 0:
            laser = Laser(self.x + (75 / 2) - 4, self.y, self.lasers_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
