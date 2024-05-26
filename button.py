import pygame as pg


class Button:
    def __init__(self, x: int, y: int, button_img, button_text: str, font):
        self.x = x
        self.y = y
        self.button_img = button_img
        self.button_text = button_text
        self.font = font
        self.text = font.render(self.button_text, 1, (255, 255, 255))
        # Calculating the x and y positions to center the text in the button
        self.text_x = self.x + (self.button_img.get_width() / 2) - (self.text.get_width() / 2)
        self.text_y = self.y + (self.button_img.get_height() / 2) - (self.text.get_height() / 2)
        self.rect = self.button_img.get_rect(topleft=(self.x, self.y))
    
    def draw(self, window):
        """ Draws the button on the screen

        Paramaters
        ----------
        window : pygame.display
            The window to render the button on
        """
        window.blit(self.button_img, (self.x, self.y))
        window.blit(self.text, (self.text_x, self.text_y))

    def clicked(self, mouse_pos):
        """ Checks if the button was clicked

        Parameters
        ----------
        mouse_pos : tuple
            The x and y position of the mouse
        
        Returns
        -------
        bool
            True if clicked, false otherwise
        """
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                return True
        return False
