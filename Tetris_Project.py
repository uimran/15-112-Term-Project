#    15-112: Principles of Programming and Computer Science
#    HW07 Programming: Term Project (Tetris)
#    Name      : Umaymah Imran
#    AndrewID  : uimran

#    File Created:
#    Modification History:
#    Start             End
#    2/11 11:46pm     3/11 3:14am
#    3/11 12:01pm     3/11 4:11pm
#    3/11 10:21pm     4/11 1:39am
#    4/11 9:44pm      4/11 11:32pm
#    7/11 5:13pm      7/11 8:21pm
#    8/11 10:45am     8/11 2:37pm
#    9/11 11:56pm     10/11 2:53am
#    10/11 4:07am     10/11 5:52am
#    10/11 2:43pm     10/11 6:17pm
#    11/11 3:12pm     11/11 6:21pm
#    13/11 02:41pm    13/11 04:22pm
#    14/11 06:19pm    14/11 07:56pm
#    17/11 09:48am    17/11 12:43pm
#    17/11 07:32pm    17/11 09:18pm
#    18/11 08:54pm    18/11 10:02pm
#    19/11 11:39pm    20/11 01:34am
#    20/11 05:19pm    20/11 08:16pm
#    21/11 12:04pm    21/11 01:23pm
#    21/11 04:04pm    21/11 08:57pm
#    21/11 09:26pm    22/11 02:56am
#    23/11 08:18pm    24/11 12:12am
#    24/11 03:44am    24/11 05:20am
#    25/11 08:00pm    26/11 05:50am
#    26/11 07:52pm    26/11 10:19pm
#    26/11 10:31pm    27/11 12:45am
#    27/11 10:28am    27/11 11:22am
#    27/11 03:12pm    27/11 07:35pm
#    27/11 09:11pm    27/11 11:08pm
#    28/11 12:00pm    28/11 12:45pm
# import the necessary libraries
import pygame
import random


#############################################FUNCTION DEFINITIONS#######################################################
# Taken references and help from the following links:
# https://www.youtube.com/watch?v=Ign-VmKmz9g
# https://pythonprogramming.net/
# https://github.com/DanielSlater/PyGamePlayer/blob/master/games/tetris.py
# https://github.com/yash-iiith/Tetris-Game-in-Python-without-Pygame-/blob/master/tetris.py
# https://inventwithpython.com/pygame/chapter7.html
# https://gist.github.com/silvasur/565419/d9de6a84e7da000797ac681976442073045c74a4
# https://www.pygame.org/docs/ref/event.html
# https://github.com/matachi/python-tetris/blob/master/main.py
# http://www.discoveryplayground.com/computer-programming-for-kids/rgb-colors/
# Image for main screen taken from: https://www.ubisoft.com/en-us/game/tetris-ultimate
# Sound for collision from: http://soundbible.com/1742-Anvil-Impact-1x.html
# Sound for removal of rows: http://soundbible.com/1891-Flyby.html
# Sound for main screen: https://downloads.khinsider.com/game-soundtracks/album/tetris-gameboy-rip-/tetris-gameboy-01.mp3

# Code taken from: https://pythonprogramming.net/pygame-start-menu-tutorial/
# function(text_objects) is used to centre align the text of a button
def text_objects(text, font):
    textSurface = font.render(text, True, cyan)
    return textSurface, textSurface.get_rect()


# Code modified but orginially taken from: https://pythonprogramming.net/pygame-start-menu-tutorial/
# function(button) is used to create a button on the screen. It takes the text for the button, its x and y coordinates,
# its width and height, and calls the specified action(function) when the button is clicked
def button(msg, x, y, w, h, on, off, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, off, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, on, (x, y, w, h))

    if msg == "Back" or (msg == "Quit" and gameover == False) or msg == "Sound":
        smallText = pygame.font.Font("freesansbold.ttf", 14)
    else:
        smallText = pygame.font.Font("freesansbold.ttf", 20)

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


# Code taken from:https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
# class Background is used to set an image as the background of a screen
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# function(quitgame) exits the pygame window when clicked on 'X'
def quitgame():
    pygame.quit()
    quit()


# function(board) returns a 2D list 'board' in which each item in the list represents a row, and each element in the row
# represents a column. It takes the number of rows and columns as parameters. Each row is intialized as [0,0,0....,n],
# where n represents the number of columns. At the end, an extra row with [1,1,1,....,n] is intialized - this is to
# detect when a block touches the bottom of the board (by using the function collision_occured)
def new_board(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(0)
        board.append(row)
    extra_row = []
    for k in range(cols):
        extra_row.append(1)
    board.append(extra_row)
    return board


# function(collision_occured) takes the board, the shape definition, the sxth col and the syth row as inputs (sx and sy
# are the x and y positions of the shape). Using this, it determines when the shape has collided with either the edges,
# with the button of the board or with another shape
def collision_occured(board, shape, shape_x, shape_y):
    i = 0  # i and j are  variables for the while loop in order to go through the indexes of the item (shape in
    j = 0  # case of i and row in case of j) specified
    
    
    # The following code segment goes through each row of a shape and accesses each column of the shape and compares it to the
    # value in the board. If the value at the board is 0, collision has not occured. If it's any value between 1-7, and the shape
    # touches it, then collision has occured and the shape stops
    while i < len(shape):
        row = shape[i]
        while j < len(row):
            col = row[j]
            try:
                if col and board[i + shape_y][j + shape_x]:
                    return True

            except IndexError:
                return True
            j += 1 #increment j by 1
        i += 1 #increment i by 1
        j = 0 #initialize j to 0 as next row will start
    return False

def collision_occured_bottom(board, shape, shape_x, shape_y):
    i = 0  # i and j are  variables for the while loop in order to go through the indexes of the item (shape in
    j = 0  # case of i and row in case of j) specified
    
    
    # The following code segment goes through each row of a shape and accesses each column of the shape and compares it to the
    # value in the board. If the value at the board is 0, collision has not occured. If it's any value between 1-7, and the shape
    # touches it, then collision has occured and the shape stops
    while i < len(shape):
        row = shape[i]
        while j < len(row):
            col = row[j]
            try:
                if col and board[i + shape_y+1][j + shape_x]:
                    return True

            except IndexError:
                return True
            j += 1 #increment j by 1
        i += 1 #increment i by 1
        j = 0 #initialize j to 0 as next row will start
    return False

# function(place_shape) adds the the digits 1-7 to the board when the shape is placed in it and returns the updated version of the
# board. It takes the current board, the shape that is moving down, the x (column) and y (row) location of the shape and mute (so
# that the functionality for the 'Sound' button can be controlled)
def place_shape(board, shape, shape_x, shape_y , mute):
    i = 0  # i and j are  variables for the while loop in order to go through the indexes of the item (shape in
    j = 0  # case of i and row in case of j) specified

    # The following code segment goes through each row of a shape and accesses each column of the shape and adds it to the specific
    # location of the board where the shape settles. If mute is False, then the sound to identify the collision/settlement of the
    # shape will play
    while i < len(shape):
        row = shape[i]
        while j < len(row):
            if shape[i][j]:
                board[i+shape_y-1][shape_x+j] = shape[i][j]
                if not mute:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('collision.wav')) # sound plays in the same channel as main sound
            j += 1 #increment j by 1
        i += 1 #increment i by 1
        j = 0 #initialize j to 0 as next row will start
    return board

# function (remove_row) removes complete, non-zero horizontal rows from the board. This function returns the number of lines removed,
# the updated version of the board (the rows above the removed row(s) move down and row(s) with 0s are initialized at the top in their
# place) and the updated myscore (as score increases with removal of lines). 
def remove_row(board, myscore, lines, mute):
    rows_removed = 0 # keeps track of the zero rows removed, this is required for updating myscore
    zero_rows = [] #zero_rows are the newly initialized rows that will be appended to the board when row(s) is/are removed
    update = [] #update holds the final return value of the function
    score_inc = 40 # score_inc is the variable that stores the value with which rows_removed is to be multipled (for updating myscore)
    # By starting from the top most row, the following loop iterates through each row and loops for non-zero rows. Since the bottom
    # most row of the board is [1,1,1,....1], the loop will disregard that row.
    for i in range(len(board) - 2, -1, -1): 
        if 0 not in board[i]:
            if not mute:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('remove_row.wav')) #when the row is removed, a 'swish' sound is played
            del board[i]
            rows_removed += 1
            
    myscore += rows_removed * score_inc #myscore updates
    lines += rows_removed #updates number of lines that have been removed so far

    #This loop adds as many zero rows as non-zero rows were removed
    for j in range(0, rows_removed):
        zero_rows += [[0 for i in range(0, cols)]]
        
    board = zero_rows + board #adds the zero rows to top most of current board

    #stores the updated values for the board, myscore and line in the 'updated' list
    update.append(board)
    update.append(myscore)
    update.append(lines)
    return update

# function (shape_rotation) will change the orientation of the shape every time the 'up' arrow key is pressed. It takes the board, the
# description of the current shape and its x (column) and y (row) locations as input. If, by pressing the 'up' key a collision is occuring,
# the shape will not rotate and will remain as it is. Otherwise, the function returns the new shape description, causing the shape to
# rotate at 90 degrees with each key press of 'up'. 
def shape_rotation(board,current_shape_desc,shape_x,shape_y):
    new_shape = []

    # The following code segment changes the row and column wise description of the shape. In other words, it tranposes the 2D matrix (which
    # is the shape of the object)
    for y in range(len(current_shape_desc[0]) - 1, -1, -1):
        l = []
        for x in range(len(current_shape_desc)):
            l.append(current_shape_desc[x][y])
        new_shape.append(l)

    # The new shape will return if there is no collision on all four sides of the shape
    if not collision_occured(board, new_shape, shape_x, shape_y):
        return new_shape

    # Otherwise, the current shape description will be returned as it is
    return current_shape_desc

# function(new_shape) initializes the properties of a shape. It generates a random shape from the list All_shapes.
# It then returns the details of the shape, which are stored in a dictionary, that is, the shape's color and description
def new_shape(All_shapes):
    properties_current_shape = [random.choice(All_shapes)] #shapes are randomly generated
    item = properties_current_shape[0]
    return item

# function (initialize_game) is used to restart the game if the Back button on the Game Play screen is pressed and then if the player
# returns to the game OR to restart the game at the time of game over
def initialize_game():
    # The following variables are globalized to change and store the change in their state, by setting all variables to their initial values
    global board
    global current_shape_desc
    global current_shape_col
    global next_predicted_shape
    global shape_x
    global shape_y
    global mute
    global pause
    global fileopen
    global rules
    global start
    global started
    global back
    global home
    global collide
    global gameover
    global hscore
    global myscore
    global lines
    global p_count

    p_count = 25
    mute = False
    pause = False
    fileopen = True
    rules = False
    start = True
    started = False
    back = False
    home = False
    running = True
    collide = False
    gameover = False
    hscore = False
    myscore = 0
    lines = 0
    initial_shape = new_shape(All_shapes)
    current_shape_desc = initial_shape["shape"]
    current_shape_col = initial_shape["color"]
    next_predicted_shape = new_shape(All_shapes)
    shape_x = 4
    shape_y = 0
    board = new_board(rows, cols)

    file = 'maintheme.mp3'  # the main sound being played in the background 
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

#function(check_top) checks if there is any non-zero number in the first row of the
#board. If there is, it will return False, otherwise it'll return True
def check_top (board):
    if not 0 in board[0]:
        return False
    return True

# Definitions of all colors used
black = (0, 0, 0)
white = (255, 255, 255)
darkblue = (72, 61, 139)
cyan = (224, 255, 255)
blue = (25, 25, 112)
staleblue = (72, 61, 139)
med_blue = (25, 25, 112)
red = (178, 34, 34)
yellow = (230, 200, 48)
green = (34, 139, 34)
purple = (130, 50, 204)
orange = (210, 105, 30)
pink = (176, 48, 96)

# The shapes and their colors that I'm using. The arrangement of each shape can be imagined as this one for the simple
# square (where * represents a number):
# [[*,*]
#  [*,*]]
All_shapes = [{"shape": [[1, 1], [1, 1]], "color": yellow}, {"shape": [[0, 5, 0], [5, 5, 5]], "color": med_blue},
              {"shape": [[0, 2, 2], [2, 2, 0]], "color": green}, {"shape": [[7, 7, 0], [0, 7, 7]], "color": red},
              {"shape": [[3, 0, 0], [3, 3, 3]], "color": purple}, {"shape": [[0, 0, 6], [6, 6, 6]], "color": pink},
              {"shape": [[4, 4, 4, 4]], "color": orange}]

# The dictionary color_shape_mapping assigns colors to each digit value (which signifies a specific shape)
color_shape_mapping = {"1": yellow, "5": med_blue, "2": green, "7": red, "3": purple, "6": pink, "4": orange}

# INITIALIZING THE FOLLOWING VARIABLES

mute = False # if 'Sound' is pressed then mute is True and the sounds discontinue, otherwise it is set to False by default and sound plays

pause = False # pause determines whether or not the game is in pause state

fileopen = True # fileopen is the file for storing the high score. It is open by default so that it can be updated when required (run-time)

rules = False # rules is for determining the state of the RULES screen. If it's false, then the screen for Rules is not open (vice-versa)

start = False # start is for determining the state of the START screen. If it's false, then the screen for Start is not open (vice-versa)

started = False # started is for indicating that the game has started.

back = False # back is for determining the states of the back button and for determining the required screens

home = True # home is for determining the state of the HOME/MAIN screen. If it's false, then the screen for Home is not open (vice-versa)

running = True # running is for the game loop

collide = False # collide is False by default, it becomes True if the shapes reach the top-most part of the board

gameover = False # if the shapes reach the top-most part of the board, the game is over

hscore = False # hscore determines the state of the high score. If it's True, the High Score of the game will update

play_music = True # play_music controls the background music

myscore = 0 # intially, the score is set to 0. It only increases if you press the down key or if complete non-zero rows are removed

lines = 0 # lines stores the number of non-zero rows removed

p_count = 25 # p_count is the pixel size of the box for drawing the shapes

tempo = 0 # tempo is used allow the shape to shift a bit after it hits a surface

# The first shape and the shape after that are determined
initial_shape = new_shape(All_shapes)
current_shape_desc = initial_shape["shape"]
current_shape_col = initial_shape["color"]
next_predicted_shape = new_shape(All_shapes)

# shape_x: xth column from where the shape drops
# shape_y: yth row from where the shape drops
shape_x = 4
shape_y = 0

# the board has a total of 20 rows and 10 columns
rows = 20
cols = 10

board = new_board(rows, cols)  # initialize the board for the gameplay


    
###################################################MAIN CODE############################################################
pygame.init()  # initializes all imported pygame modules
clock = pygame.time.Clock()  # clock is used to track and control the framerate of the game

# BackGround_MainScreen sets the background image for the main screen
BackGround_MainScreen = Background('TetrisMain.jpg', [0, 0])

# window_size is the height and width for the screen
window_size = (400, 500)

# screen initializes screen ans its size
screen = pygame.display.set_mode(window_size)

# sets the title for the window
pygame.display.set_caption('Tetris')

# applies changes to screen
screen.blit(BackGround_MainScreen.image, BackGround_MainScreen.rect)

# The following is an event type to appear on the event queue after every 1000 milliseconds
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)


if play_music:
    file = 'maintheme.mp3' # the main sound being played in the background
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

# While the game is running, the following events can possibly occur. Based on what event is
# true, carry out the neccesary steps
while running:
    for event in pygame.event.get():

        # pygame.QUIT: allows to quit the window when clicked on 'X' in the top right corner
        if event.type == pygame.QUIT:
            running = False

        # pygame.MOUSEBUTTONDOWN: detects a click on the screen
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # get the coordinates on the x and y axis when you click on the screen
            x, y = pygame.mouse.get_pos()

            # the following conditions specify the range of click for x and y coordinates in order to
            # activate a particular button

            if (x > 130 and x < 310 and y > 280 and y < 330) and (start == False and rules == False):
                # after clicking on the button "START", the conditional statement for 'start' is made
                # true and therefore, executed
                click = pygame.mouse.get_pressed()
                initialize_game()
                if click[0] == 1:
                    start = True
                    rules = False
                    back = True
                    home = False

            elif (x > 130 and x < 310 and y > 340 and y < 390) and (start == False and rules == False):
                # after clicking on the button "RULES", 'rules' is made true and the conditional statement for
                # it are executed
                click = pygame.mouse.get_pressed()

                if click[0] == 1:
                    rules = True
                    back = True
                    home = False

            elif (x > 130 and x < 310 and y > 400 and y < 450) and (start == False and rules == False):
                # after clicking on the button "QUIT", the function(quitgame) is called
                click = pygame.mouse.get_pressed()

            elif (x > 0 and x < 80 and y > 0 and y < 30) and back == True:
                # when you click on the button "RULES", a screen with an image of the rules for the game
                # appear with a "BACK" button in the top left corner. By clicking on this back button,
                # the user is lead to the home screen again
                rules = False
                back = False
                home = True

            elif (x > 170 and x < 270 and y > 315 and y < 350) and gameover == True:
                # after clicking on the button "RESTART", in gameover, the states of the following variables change:
                start = True
                gameover = False
                rules = False
                home = False

            elif (x > 170 and x < 270 and y > 360 and y < 395) and gameover == True:
                # after clicking on the button "RULES", in gameover, the states of the following variables change:
                gameover = False
                rules = True
                start = False
                home = False
                
            elif (x > 300 and x < 360 and y > 390 and y < 415) and start == True:
                # after clicking on the button "Sound", in game play, the sound is stopped (or played) - depending on
                # its previous state:
                mute = not mute
                if mute:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            elif (x > 300 and x < 360 and y > 420 and y < 445) and (start == True and back == True):
                # after clicking on the button "Back", in game play, the states of the following variables change and
                # the player is directed to the main screen:
                click = pygame.mouse.get_pressed()
                if click[0] == 1:
                    start = False
                    rules = False
                    back = False
                    home = True

            elif (x > 300 and x < 360 and y > 450 and y < 475) and start == True:
                # after clicking on the button "Quit", in game play, the program exits:
                click = pygame.mouse.get_pressed()
                quitgame()

        # pygame.KEYDOWN: detects if a key is pressed
        elif event.type == pygame.KEYDOWN and start == True:

            # the following show the initialization of the variables 'down' (holding the value when the
            # down arrow key is pressed), 'right' (holding the value when the right arrow key is pressed),
            # 'left' (holding the value when the left arrow key is pressed)
            down = pygame.key.get_pressed()[pygame.K_DOWN]
            left = pygame.key.get_pressed()[pygame.K_LEFT]
            right = pygame.key.get_pressed()[pygame.K_RIGHT]
            up = pygame.key.get_pressed()[pygame.K_UP]
            paused = pygame.key.get_pressed()[pygame.K_p]
            # restricts the movement towards the left if there is already a shape lying on that side. otherwise,
            # it decreases the value of the x-axis by 1 block
            if left and not collision_occured(board, current_shape_desc, shape_x - 1, shape_y):
                if shape_x > 0:
                    shape_x -= 1

            # restricts the movement towards the right if there is already a shape lying on that side. otherwise,
            # it increases the value of the x-axis by 1 block
            elif right and not collision_occured(board, current_shape_desc, shape_x + 1, shape_y):
                if shape_x < 9:
                    shape_x += 1
                    
            # restricts the rotation of the shape if there is already a shape/boundary on a side. otherwise,
            # returns the rotated shape      
            elif up and not collision_occured(board, current_shape_desc, shape_x, shape_y):
                current_shape_desc = shape_rotation(board, current_shape_desc, shape_x, shape_y)
                
            # if the down key is pressed, the value of the y-axis increments by 1 block
            elif down and not collision_occured(board, current_shape_desc, shape_x, shape_y + 1):
                    shape_y += 1
                    myscore += 1
                    if collision_occured_bottom(board, current_shape_desc, shape_x, shape_y):
                        tempo = 100
                    
            # if the 'P' key is pressed, the opposite of the present state of the game pause is returned       
            elif paused:
                pause = not pause
                
        # pygame.USEREVENT +1: allows the block to automatically move downwards after one click, since it keeps
        # decrementing the value of the y-axis. It also updates the board by returning the new board if the rows
        # are removed and the corresponding change in myscore and lines removed.
        elif event.type == pygame.USEREVENT+1:
            
            if start:
                shape_y += 1
                update = remove_row(board, myscore, lines, mute)
                board = update[0]
                myscore = update[1]
                lines = update[2]
                
    # checking if the game is paused, if yes, then game stays within this loop until unpaused           
    while pause:

        # displays the message that the game is paused
        largeText = pygame.font.Font("freesansbold.ttf", 60)
        msg = "Paused"
        textSurf, textRect = text_objects(msg, largeText)
        textRect.center = (190, 235)
        screen.blit(textSurf, textRect)

        for event in pygame.event.get():
            
            # pygame.QUIT: allows to quit the window when clicked on 'X' in the top right corner
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # pygame.KEYDOWN: detects if a key is pressed
            elif event.type == pygame.KEYDOWN and start == True:
                paused = pygame.key.get_pressed()[pygame.K_p]
                # unpause the game if its paused, and so exits this loop
                if paused:
                    pause = not pause

            # pygame.MOUSEBUTTONDOWN: detects a click on the screen    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # get the coordinates on the x and y axis when you click on the screen
                x, y = pygame.mouse.get_pos()
                if (x > 300 and x < 360 and y > 420 and y < 445) and (start == True):
                    # after clicking on the button "Back", in game play, the states of the following variables change and
                    # the player is directed to the main screen:
                    click = pygame.mouse.get_pressed()
                    if click[0] == 1:
                        start = False
                        rules = False
                        back = False
                        home = True
                        pause = False
                        
                if (x > 300 and x < 360 and y > 390 and y < 415) and (start == True):
                    # after clicking on the button "Sound", in game play, the sound is stopped (or played) - depending on
                    # its previous state:
                    click = pygame.mouse.get_pressed()
                    if click[0] == 1:
                        mute = not mute
                        if mute:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        button("Sound", 300, 390, 60, 25, blue, staleblue)
        button("Back", 300, 420, 60, 25, blue, staleblue)
        button("Quit", 300, 450, 60, 25, blue, staleblue, quitgame)

        # update screen
        pygame.display.update()
        clock.tick(20)
        
    # if any of the HOME, RULES or START screens is activated (or True), the subsequent if-condition will be executed

    # 'home' is the bool variable for the main screen. If it is true, the following code is executed. The home screen
    # first appears when the game is started
    if home:

        # shows the display including the background and necessary buttons
        screen.blit(BackGround_MainScreen.image, [0, 0])
        button("START", 110, 280, 180, 50, blue, staleblue)
        button("RULES", 110, 340, 180, 50, blue, staleblue)
        button("QUIT", 110, 400, 180, 50, blue, staleblue, quitgame)

    # 'rules' is the bool variable for the rules screen. If it is true, the following code is executed. The rule screen
    # appears when the button "RULES" is clicked
    elif rules:
        rule = Background("rules.png", [0, 0])
        screen.blit(rule.image, [0, 0])
        button("BACK", 0, 0, 80, 30, blue, staleblue)

    # 'start' is the bool variable for the game play screen. If it is true, the following code is executed. The start
    # (or game play) screen appears when the button "START" is clicked
    elif start:
        # window initializes the total size for the game play window. In this, we will be using the first 250 pixels
        # (from left to right) for the tetris game play and the remaining 150 pixels to draw the side panel (which includes
        # the score, next piece, lines)

        window = (400, 500)

        # updates the screen
        screen = pygame.display.set_mode(window)
        background = pygame.Surface(window)
        screen.blit(background, (0, 0))

        # font1 & font2 are font types and their sizes to use for headings on the side panel
        font1 = pygame.font.Font("freesansbold.ttf", 20)
        font2 = pygame.font.Font("freesansbold.ttf", 16)

        # draw a rectangular panel on the right side
        pygame.draw.rect(screen, darkblue, (250, 0, 150, 500))

        # add the heading 'Next:' to the rectangular panel with the upcoming shape
        text = font1.render("Next:", 1, white)
        screen.blit(text, (260, 100))

        # Draw the black box in which the next piece should appear
        pygame.draw.rect(screen, black, (265, 140, 120, 95))

        # add the heading 'Lines:' to the rectangular panel with the updated removed lines
        text = font2.render("Lines: " + str(lines), 1, white)
        screen.blit(text, (260, 280))

        # add the heading 'Score:' to the rectangular panel with the updated current score
        text = font2.render("Score: " + str(myscore), 1, white)
        screen.blit(text, (260, 310))

        
        f = open("high_score.txt", 'r') # opens the file to read the current high score value
        line = f.read()
        highscore = line.strip()
        highscore = int(highscore)
        
        if myscore > highscore: # if the highscore value is less than the current myscore, then the current
            highscore = myscore # score becomes the high score

        # add the heading 'High Score:' to the rectangular panel with the updated high score
        text = font2.render("High Score: " + str(highscore), 1, white)
        screen.blit(text, (260, 340))
        
        # draw a white line b/w the gameplay screen and the rectangular panel
        pygame.draw.line(screen, white, (250, 0), (250, 500))

        # initialize buttons on the right panel to activate sound, pause the game, or to quit the game
        button("Sound", 300, 390, 60, 25, blue, staleblue)
        button("Back", 300, 420, 60, 25, blue, staleblue)
        button("Quit", 300, 450, 60, 25, blue, staleblue)


        # the following segment draws the block as it moves downwards (from top to bottom)
        y, x = 0, 0
        for row in current_shape_desc:
            for col in row:
                if col:
                    # to draw the shape
                    pygame.draw.rect(screen, current_shape_col, pygame.Rect((shape_x + x) * p_count, (shape_y + y) * p_count, 25, 25), 0)

                    # to draw the outline of the shape
                    pygame.draw.rect(screen, black, pygame.Rect((shape_x + x) * p_count, (shape_y + y) * p_count, 25, 25), 1)
                x += 1
            y += 1
            x = 0

        # draw the next predicted shape and align the next shape in the black rectangular box (below Next) according
        # to the shape dimensions
        # In this code segment, the digits being added to x and y represent the column and row from where the shape
        # should be started for drawing
        y, x = 0, 0
        for row in next_predicted_shape["shape"]:
            for col in row:
                if col:
                    if 1 in row: # if the shape is a square
                        
                        # to draw the shape
                        pygame.draw.rect(screen, next_predicted_shape["color"],
                                         pygame.Rect((12 + x) * p_count, (6.5 + y) * p_count, 25, 25), 0)
                        
                        # to draw the outline of the shape
                        pygame.draw.rect(screen, black,
                                         pygame.Rect((12 + x) * p_count, (6.5 + y) * p_count, 25, 25), 1)
                        
                    elif 4 in row: #if the shape is a straight line
                        
                        # to draw the shape
                        pygame.draw.rect(screen, next_predicted_shape["color"],
                                         pygame.Rect((11 + x) * p_count, (7 + y) * p_count, 25, 25), 0)
                        # to draw the outline of the shape
                        pygame.draw.rect(screen, black,
                                         pygame.Rect((11 + x) * p_count, (7 + y) * p_count, 25, 25), 1)
                        
                    else: #any other shape

                        # to draw the shape
                        pygame.draw.rect(screen, next_predicted_shape["color"],
                                         pygame.Rect((11.5 + x) * p_count, (6.5 + y) * p_count, 25, 25), 0)

                        # to draw the outline of the shape
                        pygame.draw.rect(screen, black,
                                         pygame.Rect((11.5 + x) * p_count, (6.5 + y) * p_count, 25, 25), 1)
                x += 1
            y += 1
            x = 0

        # if collision occurs at the maximum top of the screen, it indicates the end of the game
        if collision_occured(board, current_shape_desc, 4, 0) :
            if check_top (board):
                collide = True
                pygame.time.delay(2000)
                start = False
                gameover = True
                file = 'gameover.wav'  # the sound in the background being played
                pygame.mixer.music.stop()
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.5)

        # otherwise, the game continues
        if collide == False:
            if collision_occured_bottom(board, current_shape_desc, shape_x, shape_y):
                if tempo<10:
                    tempo = tempo+1
                else:
                    tempo=0
                    place_shape(board, current_shape_desc, shape_x, shape_y+1, mute)
                    shape_x = 4
                    shape_y = 0
                    next_shape = next_predicted_shape
                    next_predicted_shape = new_shape(All_shapes)
                    current_shape_col = next_shape["color"]
                    current_shape_desc = next_shape["shape"]


            # the following segment draws the block at the bottom of the board when it is settled
            y, x = 0, 0
            for row in board:
                for col in row:
                    if col:
                        
                        color = color_shape_mapping[str(col)]
                        
                        # to draw the shape
                        pygame.draw.rect(screen, color, pygame.Rect(x * p_count, y * p_count, 25, 25), 0)
                        
                        # to draw the outline of the shape
                        pygame.draw.rect(screen, black, pygame.Rect(x * p_count, y * p_count, 25, 25), 1)
                    x += 1
                y += 1
                x = 0

    # 'gameover' is the bool variable for the gameover screen. If it is true, the following code is executed. The gameover screen
    # first appears when the collision occurs at the top most portion of the board              
    elif gameover:
        # sets screen to black
        screen.fill(black)

        # initialize fonts
        font3 = pygame.font.Font("freesansbold.ttf", 40)
        font4 = pygame.font.Font("freesansbold.ttf", 20)

        # open the file that scores the high score for read and write
        hisc = open("high_score.txt", 'r+')

        #first read the high score
        line = hisc.read()
        highscore = line.strip()
        highscore = int(highscore)

        #if the highscore is less than the current score, update the highscore value in the file
        #by overwriting the current highscore value
        if fileopen:
            if myscore > highscore:
                hisc.seek(0)
                hisc.truncate()
                fileopen = False
                myscore = str(myscore)
                hisc.write(myscore)
                highscore = int(myscore)
                hscore = True
            hisc.close()

        # if there was a new high score, then show the message of New High Score to user with the current score
        if hscore:
            text = font4.render("New High Score!", 1, white)
            screen.blit(text, (120, 230))
            text = font4.render("Score: " + str(myscore), 1, white)
            screen.blit(text, (150, 260))

        #otherwise, just show the user their ending score
        else:
            text = font4.render("Score: " + str(myscore), 1, white)
            screen.blit(text, (150, 260))
            
        # add the heading to the Gameover screen
        text = font3.render("Game Over", 1, white)
        screen.blit(text, (80, 160))

        # add buttons to the gameover screen:

        # restart the game:
        button("RESTART", 110, 300, 180, 50, blue, staleblue)

        # go to rules:
        button("RULES", 110, 360, 180, 50, blue, staleblue)

        # quit the game:
        button("QUIT", 110, 420, 180, 50, blue, staleblue, quitgame)

    # update the screen
    clock.tick(30)
    pygame.display.update()

pygame.quit()
