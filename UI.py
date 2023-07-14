from SETTING import WHITE, LEFT, BLACK
import pygame as pg
from pygame.locals import *
import time
from Game_Board import Board

def CreateButton(display_screen, x, y, width, height, content, font, content_color, bg_color):

    Button = pg.Rect(x, y, width, height)

    play_content = font.render(content, True, content_color)
    play_content_Rect = play_content.get_rect()
    play_content_Rect.center = Button.center

    pg.draw.rect(display_screen, bg_color, Button)
    display_screen.blit(play_content, play_content_Rect)

    return Button

def CreateTitle(display_screen, x, y, content, font, font_color=WHITE):

    Title = font.render(content, True, font_color)

    Title_Rect = Title.get_rect()
    Title_Rect.center = (x, y)
    display_screen.blit(Title, Title_Rect)

    return Title

class Game_Button:

    def __init__(self, x, y, width, height, display_screen, MyGame, font):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display_screen = display_screen
        self.MyGame = MyGame
        self.font = font

        # "content": ["Play Again", "Solution", "User Mode", "->", "Solve All", "<-", "Undo Move", "Submit"]

        self.button_list = {
            "Play Again": 0, "Solution": 1, "User Mode": 2,
            "->": 3, "Solve All": 4, "<-": 5, "Undo Move": 6, "Submit": 7
        }

        self.button_adjustment = {
            "width_scale": [1, 1, 1, 2, 1, 2, 1, 1],
            "height_scale": [1, 1, 1, 1, 1, 1, 1, 1],
            "x_offset": [0, 0, 0, self.width + 10, 0, -self.width//2 - 10, 0, 0],
            "y_offset": [180, 0, -60, 0, 0, 0, -60, 120]
        }

    def Init_Button(self, content):

        # Adjust position for button with content = content
        index = self.button_list[content]
        x = self.x + self.button_adjustment["x_offset"][index]
        y = self.y + self.button_adjustment["y_offset"][index]
        width = self.width // self.button_adjustment["width_scale"][index]
        height = self.height // self.button_adjustment["height_scale"][index]
        
        button = CreateButton(self.display_screen, x, y, width, height, content, self.font, content_color=BLACK, bg_color=WHITE)

        return button
    
    def onclick(self, content, button):

        # Check if button is clicked
        click, _, _ = pg.mouse.get_pressed()
        if click == 1:
            mouse = pg.mouse.get_pos()
            if button.collidepoint(mouse):
                time.sleep(0.2)

                if content == "Play Again":
                    self.MyGame = Board(self.MyGame.Font)
                    return self.MyGame
                elif content == "User Mode":
                    self.MyGame.ai_turn = False
                    return False
                elif content == "->":

                    index = len(self.MyGame.AI_move_logs)
                    if index < len(self.MyGame.Solutions):
                        self.MyGame.make_move(self.MyGame.Solutions[index], LEFT)

                elif content == "Solve All":

                    if len(self.MyGame.AI_move_logs) != len(self.MyGame.Solutions):

                        # Undo all past moves
                        while len(self.MyGame.AI_move_logs) > 0:
                            self.MyGame.undo_move()

                        # Making moves
                        for Move in self.MyGame.Solutions:
                            self.MyGame.make_move(Move, LEFT)

                    print('####################################################')
                    print(self.MyGame.Solutions)

                elif content == "<-" or content == "Undo Move":

                    self.MyGame.undo_move()
            
                elif content == "Submit":

                    over, message = self.MyGame.is_over()
                    self.Button_Title(message)

                    return over, message

                return True

        # None click
        if content == "Play Again":
            return self.MyGame
        elif content == "User Mode":
            return True
        elif content == "Submit":
            return False, ""
        
        return False
    
    def Button_Title(self, message):

        CreateTitle(self.display_screen, self.x + self.width//2, self.y - 180, message, self.font, WHITE)
        return

    def Button_creation(self, content):

        button = self.Init_Button(content)
        return self.onclick(content, button)
        

        

        



