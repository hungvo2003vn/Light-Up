import pygame as pg
import sys
from pygame.locals import *
from SETTING import *
from UI import *
from Game_Board import *
import asyncio

# Init pygame
pg.init()
pg.display.set_caption("Light Up")

display_screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Font size
MEDIUM_FONT = pg.font.Font("OpenSans-Regular.ttf", 28)
LARGE_FONT = pg.font.Font("OpenSans-Regular.ttf", 40)
MOVE_FONT = pg.font.Font("OpenSans-Regular.ttf", 60)
Font = [MEDIUM_FONT, LARGE_FONT]

def main():

    #Init game
    MyGame = Board(Font)
    message = ""

    # For title
    width = SCREEN_WIDTH/6
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2 + 120

    while True:

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        display_screen.fill(BLACK)

        MyGame.make_board_all(display_screen)

        _, message = Submit_Button(display_screen, MyGame, MEDIUM_FONT)

        # Create SUBMIT title
        CreateTitle(display_screen, x + width//2, y - 300, message, MEDIUM_FONT, WHITE)
        

        MyGame = GameOver_Button(display_screen, MyGame, MEDIUM_FONT)
        if not MyGame.ai_turn:
            MyGame.ai_turn = Solve_Button(display_screen, MEDIUM_FONT)
            if MyGame.ai_turn:
                if not MyGame.solved:
                    # Update UI immediately
                    CreateTitle(display_screen, x + width//2, y - 300, "AI solving...", MEDIUM_FONT, WHITE)
                    pg.display.update()
                    time.sleep(2)
                    # Solving
                    MyGame.AI_solver()
                continue

        # AI mode
        if MyGame.ai_turn:

            next_clicked = Next_Button(display_screen, MyGame, MEDIUM_FONT)
            all_clicked = All_Button(display_screen, MyGame, MEDIUM_FONT)
            undo_clicked = Undo_Button(display_screen, MyGame, MEDIUM_FONT)
            switch_clicked = User_Mode_Button(display_screen, MEDIUM_FONT)

            if all_clicked:
                
                if len(MyGame.AI_move_logs) != len(MyGame.Solutions):

                    # Undo all past moves
                    while len(MyGame.AI_move_logs) > 0:
                        MyGame.undo_move()

                    # Making moves
                    for Move in MyGame.Solutions:
                        MyGame.make_move(Move, LEFT)

                print('####################################################')
                print(MyGame.Solutions)

            MyGame.ai_turn = switch_clicked
        
        # Handle User click event
        # Check if pieces is clicked
        else:

            Undo_User_Button(display_screen, MyGame, MEDIUM_FONT)

            pos = None
            type = None
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    
                    if event.button == LEFT or event.button == RIGHT:
                        pos = pg.mouse.get_pos()
                        type = event.button
            
            if pos is not None:
                MyGame.checking_clicked(pos, type)
            

        # Update after each event
        pg.display.update()
        
        if message != "":
            time.sleep(2)

if __name__ == '__main__':
    main()