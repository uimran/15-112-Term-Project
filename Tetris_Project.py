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


#import the necessary libraries
import pygame


#############################################FUNCTION DEFINITIONS#######################################################
#Taken references and help from the following links:
#https://www.youtube.com/watch?v=Ign-VmKmz9g
#https://pythonprogramming.net/
#https://github.com/DanielSlater/PyGamePlayer/blob/master/games/tetris.py
#https://github.com/yash-iiith/Tetris-Game-in-Python-without-Pygame-/blob/master/tetris.py
#https://inventwithpython.com/pygame/chapter7.html
#https://gist.github.com/silvasur/565419/d9de6a84e7da000797ac681976442073045c74a4
#https://www.pygame.org/docs/ref/event.html
#https://github.com/matachi/python-tetris/blob/master/main.py
#http://www.discoveryplayground.com/computer-programming-for-kids/rgb-colors/


#Code taken from: https://pythonprogramming.net/pygame-start-menu-tutorial/
#function(text_objects) is used to centre align the text of a button
def text_objects(text, font):
    textSurface = font.render(text, True, cyan)
    return textSurface, textSurface.get_rect()

#Code taken from: https://pythonprogramming.net/pygame-start-menu-tutorial/
#function(button) is used to create a button on the screen. It takes the text for the button, its x and y coordinates,
#its width and height, and calls the specified action(function) when the button is clicked
def button(msg, x, y, w, h, on, off, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, off, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, on, (x, y, w, h))

    if msg == "Pause" or msg == "Quit" or msg == "Sound":
        smallText = pygame.font.Font("freesansbold.ttf", 14)
    else:
        smallText = pygame.font.Font("freesansbold.ttf", 20)

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

#Code taken from:https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
#class Background is used to set an image as the background of a screen
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

#function(quitgame) exits the pygame window when clicked on 'X'
def quitgame():
    pygame.quit()
    quit()

#function(board) returns a 2D list 'board' in which each item in the list represents a row, and each element in the row
#represents a column. It takes the number of rows and columns as parameters. Each row is intialized as [0,0,0....,n],
#where n represents the number of columns. At the end, an extra row with [1,1,1,....,n] is intialized - this is to
#detect when a block touches the bottom of the board (by using the function collision_occured)
def board(rows,cols):
    board = []
    for i in range (rows):
        row=[]
        for j in range (cols):
            row.append(0)
        board.append(row)
    extra_row=[]
    for k in range (cols):
        extra_row.append(1)
    board.append(extra_row)

    return board

#function(collision_occured) takes the board, the shape definition, the sxth col and the syth row as inputs (sx and sy
#are the x and y positions of the shape). Using this, it determines when the shape has collided with either the edges,
# with the button of the board or with another shape
def collision_occured(board, shape, sx, sy):
    i,j=0,0 #i and j are the variables for number of count for iterations

    #The following code goes through each row of a shape and accesses each column of the shape and compares it to the
    #value in the board. If the value at the board is 0, collision has not occured otherwise if it is 1, and the block
    #touches it, then collision has occured and the block stops
    for row in shape:
        for col in row:
            try:
                if col and board[j + sy][i + sx]:
                    return True
            except IndexError:
                return True
            i += 1
        j += 1
        i = 0
    return False

#function(place_shape) adds the '1's to the board when the shape is place in it and returns the updated version of the
#board.
def place_shape(board, shape, shape_coords):
    sx, sy = shape_coords
    x,y=0,0
    for row in shape:
        for col in row:
            board[y+sy-1][sx+x] = col
            x += 1
        y += 1
        x = 0
    return board


#Definitions of all colors used
black = (0, 0, 0)
white = (255, 255, 255)
darkblue = (72, 61, 139)
cyan = (224, 255, 255)
blue = (25, 25, 112)
staleblue = (72, 61, 139)
med_blue=(25, 25, 112)

#The current shape that I'm using (for a square-two rows,two cols)
shape = [[1, 1],[1, 1]]

#initializing the values of the following variables:
rules = False
start = False
started = False
back = False
home = True
running = True
collide=False
shape_x = 4
shape_y = 0
rows = 20
cols = 10

###################################################MAIN CODE############################################################
pygame.init() #initializes all imported pygame modules
clock = pygame.time.Clock() #clock is used to track and control the framerate of the game
board = board(rows,cols) #initialize the board for the gameplay

#BackGround_MainScreen sets the background image for the main screen
BackGround_MainScreen = Background('Tetris_resized.jpg', [0,0])

#window_size is the height and width for the screen
window_size=(445, 511)

#screen initializes screen ans its size
screen = pygame.display.set_mode(window_size)

#sets the title for the window
pygame.display.set_caption('Tetris')

#applies changes to screen
screen.blit(BackGround_MainScreen.image, BackGround_MainScreen.rect)

#The following is an event type to appear on the event queue after every 1000 milliseconds
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

#While the game is running, the following events can possibly occur. Based on what event is
#true, carry out the neccesary steps
while running:
    for event in pygame.event.get():

        #pygame.QUIT: allows to quit the window when clicked on 'X' in the top right corner
        if event.type == pygame.QUIT:
            running = False

        #pygame.MOUSEBUTTONDOWN: detects a click on the screen
        elif event.type == pygame.MOUSEBUTTONDOWN:

            #get the coordinates on the x and y axis when you click on the screen
            x, y = pygame.mouse.get_pos()


            #the following conditions specify the range of click for x and y coordinates in order to
            #activate a particular button

            if (x > 130 and x < 310 and y > 280 and y < 330) and (start==False and rules==False):
                #after clicking on the button "START", the conditional statement for 'start' is made
                #true and therefore, executed
                click = pygame.mouse.get_pressed()
                button("START", 130, 280, 180, 50, blue, staleblue)

                if click[0] == 1:
                    start = True
                    rules = False
                    home = False

            elif (x > 130 and x < 310 and y > 340 and y < 390) and (start==False and rules==False) :
                #after clicking on the button "RULES", 'rules' is made true and the conditional statement for
                #it are executed
                click = pygame.mouse.get_pressed()
                button("RULES", 130, 340, 180, 50, blue, staleblue)

                if click[0] == 1 :
                    rules = True
                    back = True
                    home = False

            elif (x > 130 and x < 310 and y > 400 and y < 450) and (start==False and rules==False):
                #after clicking on the button "QUIT", the function(quitgame) is called
                click = pygame.mouse.get_pressed()
                button("QUIT", 130, 400, 180, 50, blue, staleblue, quitgame)

            elif (x > 0 and x < 80 and y > 0 and y < 30) and back == True:
                #when you click on the button "RULES", a screen with an image of the rules for the game
                #appear with a "BACK" button in the top left corner. By clicking on this back button,
                #the user is lead to the home screen again
                rules = False
                back = False
                home = True

        #pygame.KEYDOWN: detects if a key is pressed
        elif event.type == pygame.KEYDOWN and start==True:

            #the following show the initialization of the variables 'down' (holding the value when the
            #down arrow key is pressed), 'right' (holding the value when the right arrow key is pressed),
            #'left' (holding the value when the left arrow key is pressed)
            down = pygame.key.get_pressed()[pygame.K_DOWN]
            left = pygame.key.get_pressed()[pygame.K_LEFT]
            right = pygame.key.get_pressed()[pygame.K_RIGHT]

            #restricts the movement towards the left if there is already a shape lying on that side. otherwise,
            #it decreases the value of the x-axis by 1 block
            if left  and not collision_occured(board,shape,shape_x-1,shape_y):
                if shape_x > 0:
                    shape_x -= 1

            #restricts the movement towards the right if there is already a shape lying on that side. otherwise,
            #it increases the value of the x-axis by 1 block
            elif right:
                if shape_x < 9 and not collision_occured(board,shape,shape_x+1,shape_y):
                    shape_x += 1

            #if the down key is pressed, the value of the y-axis increments by 1 block
            elif down:
                shape_y += 1

        #pygame.USEREVENT +1: allows the block to automatically move downwards after one click, since it keeps
        #decrementing the value of the y-axis
        elif event.type == pygame.USEREVENT +1:
            if start:
                shape_y += 1

    #if any of the HOME, RULES or START screens is activated (or True), the suitable if-condition will be executed

    #'home' is the bool variable for the main screen. If it is true, the following code is executed. The home screen
    #first appears when the game is started
    if home:
        #shows the display including the background and necessary buttons
        screen.blit(BackGround_MainScreen.image,[0,0])
        button("START", 130, 280, 180, 50, blue, staleblue)
        button("RULES", 130, 340, 180, 50, blue, staleblue)
        button("QUIT", 130, 400, 180, 50, blue, staleblue, quitgame)

    #'rules' is the bool variable for the rules screen. If it is true, the following code is executed. The rule screen
    # appears when the button "RULES" is clicked
    elif rules:
        rule=Background("rules.png",[0,0])
        screen.blit(rule.image,[0,0])
        button("BACK", 0, 0, 80, 30, blue, staleblue)

    #'start' is the bool variable for the game play screen. If it is true, the following code is executed. The start
    #(or game play) screen appears when the button "START" is clicked
    elif start:

        #window initializes the total size for the game play window. In this, we will be using the first 250 pixels
        #(from left to right) for the tetris game play and the remaining 150 pixels to draw the side panel (which includes
        #the score, next piece, lines)
        window = (400, 500)

        #updates the screen
        screen = pygame.display.set_mode(window)
        background = pygame.Surface(window)
        screen.blit(background, (0, 0))

        #font1 & font2 are font types and their sizes to use for headings on the side panel
        font1 = pygame.font.Font("freesansbold.ttf", 20)
        font2 = pygame.font.Font("freesansbold.ttf", 16)

        #draw a rectangular panel on the right side
        pygame.draw.rect(screen, darkblue, (250, 0, 150, 500))

        #add the heading 'Next:' to the rectangular panel
        text = font1.render("Next:", 1, white)
        screen.blit(text, (260, 100))

        #Draw the black box in which the next piece should appear
        pygame.draw.rect(screen, black, (280, 140, 100, 100))
        pygame.draw.rect(screen, med_blue, (305, 165, 50, 50))

        #add the heading 'Lines:' to the rectangular panel
        text = font2.render("Lines:", 1, white)
        screen.blit(text, (260, 280))

        #add the heading 'Score:' to the rectangular panel
        text = font2.render("Score:", 1,white)
        screen.blit(text, (260, 310))

        #draw a white line b/w the gameplay screen and the rectangular panel
        pygame.draw.line(screen, white, (250, 0), (250, 500))

        #initialize buttons on the right panel to activate sound, pause the game, or to quit the game
        button("Sound", 300, 390, 60, 25, blue, staleblue)
        button("Pause", 300, 420, 60, 25, blue, staleblue)
        button("Quit", 300, 450, 60, 25, blue, staleblue, quitgame)


        #the following segment draws the block as it moves downwards (from top to bottom)
        y,x=0,0
        for row in shape:
            for col in row:
                if col:
                    pygame.draw.rect(screen, med_blue,
                                     pygame.Rect((shape_x+x) * 25,(shape_y+y) * 25,25, 25), 0)
                x += 1
            y += 1
            x = 0

        #if collision occurs at the maximum top of the screen, it indicates the end of the game
        if collision_occured(board, shape, 4, 0) or collision_occured(board, shape, 5, 0):
            collide=True
            start=False
            pygame.event.set_blocked(pygame.KEYDOWN)

        #otherwise, the game continues
        elif collide==False:
            if collision_occured(board, shape, shape_x, shape_y):
                place_shape(board, shape, (shape_x, shape_y))
                shape_x = 4
                shape_y = 0

        #the following segment draws the block at the bottom of the board when it is settled
        y, x = 0, 0
        for row in board:
            for col in row:
                if col:
                    pygame.draw.rect(screen,med_blue,pygame.Rect((x) * 25,(y) * 25,25, 25), 0)
                x += 1
            y += 1
            x = 0

    #update the screen
    clock.tick(30)
    pygame.display.update()

pygame.quit()



