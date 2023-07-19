import pygame as pg
import sys
from pygame.locals import *
from SETTING import *
from UI import *
from Game_Board import *
import threading

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
    found_solution = False

    # For title
    content = ["Play Again", "Solution", "User Mode", "->", "Solve All", "<-", "Undo Move", "Submit", "Clear"]
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2

    # Game Button
    MyGame_Button = Game_Button(x, y, width, height, display_screen, MyGame, MEDIUM_FONT)

    while True:

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        display_screen.fill(BLACK)
        MyGame.make_board_all(display_screen)

        _, message = MyGame_Button.Button_creation(content[7]) # Create Submit button
        MyGame = MyGame_Button.Button_creation(content[0]) # Create Play Again button
        MyGame_Button.Button_creation(content[8]) # Create Clear button

        if not MyGame.ai_turn:

            # Create Solution Button
            MyGame.ai_turn = MyGame_Button.Button_creation(content[1])

            if MyGame.ai_turn:
                if not MyGame.solved:

                    # Update UI immediately
                    MyGame_Button.Button_Title("AI solving...")
                    pg.display.update()

                    #Solving
                    #MyGame.found_solution = MyGame.DFS_solver()
                    MyGame.found_solution, set_lights = MyGame.Heuristic_Solver()
                    MyGame.Solutions = deepcopy(set_lights)
                    MyGame.solved = True
                    time.sleep(0.5)

                    solution_content = "Solution found!"
                    if not MyGame.found_solution:
                        solution_content = "No solution!"

                    # Update UI immediately
                    MyGame_Button.y += 60
                    MyGame_Button.Button_Title(solution_content)
                    MyGame_Button.y -= 60
                    pg.display.update()
                    time.sleep(2)

                elif not MyGame.found_solution:
                    
                    # Update UI immediately
                    MyGame_Button.Button_Title("No solution")
                    pg.display.update()
                    time.sleep(2)

                MyGame.ai_turn = MyGame.found_solution
                continue

        # AI mode
        if MyGame.ai_turn:

            MyGame_Button.Button_creation(content[5]) # Undo Button
            MyGame_Button.Button_creation(content[3]) # Next Button
            MyGame_Button.Button_creation(content[4]) # Solve All Button
            MyGame_Button.Button_creation(content[2]) # User Mode Button
        
        # Handle User click event
        # Check if pieces is clicked
        else:
            MyGame_Button.Button_creation(content[6]) # Undo Move Button

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