from SETTING import *
import pygame as pg
from pygame.locals import *
import time
from Game_Board import *

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

def GameOver_Button(display_screen, MyGame, MEDIUM_FONT):

    content = "Play Again"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2 + 120
    game_over_button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT, content_color=BLACK, bg_color=WHITE)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if game_over_button.collidepoint(mouse):
            time.sleep(0.2)
            Font = MyGame.Font
            MyGame = Board(Font)

    return MyGame

def Solve_Button(display_screen, MEDIUM_FONT):

    content = "Solution"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2
    button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT, content_color=BLACK, bg_color=WHITE)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if button.collidepoint(mouse):
            time.sleep(0.2)
            return True

    return False

def Next_Button(display_screen, MyGame, MEDIUM_FONT):

    content = "Next move"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2 - 60
    button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT, content_color=BLACK, bg_color=WHITE)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if button.collidepoint(mouse):
            time.sleep(0.2)

            # Start code
            # TODO Mygame next move
            # End code

            return True

    return False

def All_Button(display_screen, MyGame, MEDIUM_FONT):

    content = "Solve All"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2
    button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT, content_color=BLACK, bg_color=WHITE)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if button.collidepoint(mouse):
            time.sleep(0.2)

            # Start code
            # TODO Mygame all move
            # End code

            return True

    return False

def Undo_Button(display_screen, MyGame, MEDIUM_FONT):

    content = "Undo"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2 + 60
    button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT, content_color=BLACK, bg_color=WHITE)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if button.collidepoint(mouse):
            time.sleep(0.2)

            # Start code
            # TODO Mygame undo move
            # End code

            return True

    return False





