import pygame

class Button: 
    def __init__(self, x, y, width, height, key=None, text='', color=(200, 200, 200), text_color=(0, 0, 0), hover_color=(150,150,255), font_size=30):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.key = key
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont('arial', font_size)

    def draw(self, win, outline=None):
        pos = pygame.mouse.get_pos()

        current_color = self.hover_color if self.is_over(pos) else self.color

        if outline:
            pygame.draw.rect(win, current_color, (self.x, self.y, self.width, self.height), border_radius=10)

        if self.text != '':
            text_surface = self.font.render(self.text, True, self.text_color)
            text_x = self.x + (self.width - text_surface.get_width()) // 2
            text_y = self.y + (self.height - text_surface.get_height()) // 2
            win.blit(text_surface, (text_x, text_y))

    def is_over(self, pos):
        return (self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height)       
        
