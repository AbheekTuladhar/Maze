'''
Student Name: Abheek Tuladhar 
Game title: Maze
Period: 4 - HCP
Features of Game: Guide the octpus throughout the maze and collect all of it's treasure to win, all within 20 seconds.
'''

import pygame, sys, random                
pygame.init()

WIDTH=840
HEIGHT=int(WIDTH * 0.8) #5:4 screen ratio

size=(WIDTH,HEIGHT)

surface = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("Maze")
pygame.time.set_timer(pygame.USEREVENT, 1000) #Set the timer

#Colors
BLACK    = (0, 0, 0) #Maze walls
GREEN    = (0, 128, 0) #Finish line
BLUE     = (0, 84, 119) #Background
RED      = (255, 0, 0) #Text
YELLOW   = (255, 255, 0) #Gem Hitbox

#Divide the screen into a 40 by 32 coordinate graph
xu = WIDTH//40
yu = HEIGHT//32

#Program variables
gemcount = 0
totalGems = 5

#Loading and Scaling Images
player = pygame.image.load("Player.png").convert_alpha()
player = pygame.transform.scale(player, (2.5*xu, 2*yu))
player = pygame.transform.flip(player, True, False)
player_original = player.copy() #A copy of the image for when the game resets, it goes to this instead of the flipped image

gem = pygame.image.load("Gem.png").convert_alpha()
gem = pygame.transform.scale(gem, (2*xu, 2*yu))

gemCollection = pygame.mixer.Sound("GemCollection.wav") #Plays when you collect a gem

#Maze Walls
border_walls = [pygame.Rect([0, 0, WIDTH, 2*xu]), 
                pygame.Rect([38*xu, 0, 2*xu, 25*yu]), 
                pygame.Rect([0, 30*yu, WIDTH, 2*yu]), 
                pygame.Rect([39.9*xu, 27*yu, 2*xu, 5*yu]), #This border is for the end wall
                pygame.Rect([0, 0, 2*xu, HEIGHT])]

finish_line = pygame.Rect([38*xu, 25*yu, 2*xu, 5*yu]) #This is the finish line

#All of the walls that are horizontal are in this list
horizontal_walls = [pygame.Rect([ 2*xu,  5*yu,  6*xu,  2*yu]),
                    pygame.Rect([ 5*xu, 13*yu, 18*xu,  2*yu]),
                    pygame.Rect([19*xu,  8*yu,  4*xu,  2*yu]),
                    pygame.Rect([31*xu,  7*yu,  4*xu,  2*yu]),
                    pygame.Rect([ 2*xu, 18*yu,  8*xu,  2*yu]),
                    pygame.Rect([ 2*xu, 25*yu,  7*xu,  2*yu]),
                    pygame.Rect([18*xu, 23*yu, 20*xu,  2*yu])
                    ]

#All of the walls that are vertical are in this list
vertical_walls = [pygame.Rect([ 6*xu,  5*yu, 2*xu,  5*yu]),
                  pygame.Rect([13*xu,  2*yu, 2*xu,  3*yu]),
                  pygame.Rect([19*xu,  2*yu, 2*xu,  8*yu]),
                  pygame.Rect([26*xu,  2*yu, 2*xu, 12*yu]),
                  pygame.Rect([33*xu,  2*yu, 2*xu,  5*yu]),
                  pygame.Rect([13*xu,  8*yu, 2*xu, 12*yu]),
                  pygame.Rect([ 7*xu, 23*yu, 2*xu,  2*yu]),
                  pygame.Rect([13*xu, 23*yu, 2*xu,  7*yu]),
                  pygame.Rect([18*xu, 18*yu, 2*xu,  9*yu]),
                  pygame.Rect([31*xu, 15*yu, 2*xu, 12*yu])
                  ]

#Program helper functions:
def getSpeed(gemCount):
    """
    Returns the speed of the player based on the number of gems collected

    Parameters:
    ----------
    gemCount: int
        The number of gems collected by the player

    Returns:
    -------
    int
        The speed of the player
    """

    if gemCount == 0:
        return 1
    elif gemCount == 1:
        return 2
    elif gemCount == 2:
        return 3
    elif gemCount == 3:
        return 4
    elif gemCount == 4:
        return 5
    else:
        return 6
    

def drawScreen(gems, gemcount, seconds, player, playerRect):
    """
    Draws the screen and all of the game elements
    
    Parameters:
    ----------
    gems: list
        A list of all the gem rectangles
    gemcount: int
        The number of gems collected by the player
    seconds: int
        The number of seconds left in the game
    player: pygame.Surface
        The player image
    playerRect: pygame.Rect
        The player rectangle
    
    Returns:
    -------
    gameover: bool
        True if the game is over, False otherwise
    """

    gameover = False
    drawMaze()
    for gemRect in gems:
        surface.blit(gem, gemRect)
    surface.blit(player, playerRect)

    if checkWon(gemcount, playerRect, gems, seconds) == True:
        showMessage("You Win!", 60, "Consolas", WIDTH//2, HEIGHT//2, RED)
        showMessage("Press Enter to Play Again", 30, "Consolas", WIDTH//2, HEIGHT//2 + 50, RED)

    if seconds == 0:
        showMessage("You Lose!", 60, "Consolas", WIDTH//2, HEIGHT//2, RED)
        showMessage("Press Enter to Play Again", 30, "Consolas", WIDTH//2, HEIGHT//2 + 50, RED)
        gameover = True
    
    showMessage("Timer: " + str(seconds), 30, "Consolas", WIDTH//2, 20, RED, BLACK)
    return gameover


def collidesWithGem(gems, gemcount, playerRect):
    """
    Checks if the player has collided with a gem and updates the gem count
    
    Parameters:
    ----------
    gems: list
        A list of all the gem rectangles
    gemcount: int
        The number of gems collected by the player
    playerRect: pygame.Rect
        The player rectangle
    
    Returns:
    -------
    gemcount: int
        The updated gem count
    gems: list
        The updated list of gem rectangles
    """

    for gem in gems:
        if playerRect.colliderect(gem):
            pygame.mixer.Sound.play(gemCollection) #Plays the sound when you collect a gem
            gemcount += 1
            gems.remove(gem) #Removes the gem from the list
    return gemcount, gems


def collidesWithWall(rect):
    """
    Checks if the player has collided with a wall
    
    Parameters:
    ----------
    rect: pygame.Rect
        The player rectangle
    
    Returns:
    -------
    bool
        True if the player has collided with a wall, False otherwise
    """

    for wall in border_walls: #Checks if the player has collided with a border wall
        if wall.colliderect(rect):
            return True
    for wall in horizontal_walls: #Checks if the player has collided with a horizontal wall
        if wall.colliderect(rect):
            return True
    for wall in vertical_walls: #Checks if the player has collided with a vertical wall
        if wall.colliderect(rect):
            return True
    if wall.colliderect(finish_line): #Checks if the player has collided with the finish line
        return True
    return False


def showMessage(words, size, font, x, y, color, bg = None):
    """
    Displays a message on the screen
    
    Parameters:
    ----------
    words: str
        The message to display
    size: int
        The size of the font
    font: str
        The font of the message
    x: int
        The x-coordinate of the message
    y: int
        The y-coordinate of the message
    color: tuple
        The color of the message
    bg: tuple
        The background color of the message. If no background color is provided, the message will have a transparent background
    """
    
    text_font = pygame.font.SysFont(font, size, True, False)
    text = text_font.render(words, True, color, bg)
    textBounds = text.get_rect()
    textBounds.center = (x, y)
    surface.blit(text, textBounds)


def placeGems(totalGems):
    """
    Places the gems in random locations on the screen. If the gem is placed on a wall, it will be placed in a new location
    
    Parameters:
    ----------
    totalGems: int
        The total number of gems to place
    
    Returns:
    -------
    gemList
        A list of all the gem rectangles
    """
    
    gemList = [] #A list of all the gem rectangles

    for _ in range(totalGems): #Runs the loop for the amount of times specified by totalGems
        x = random.randint(0, WIDTH-2*xu)
        y = random.randint(0, HEIGHT-2*yu)
        gemRect = pygame.Rect([x, y, 2*xu, 2*yu])
    
        while collidesWithWall(gemRect): #If it did collide with a wall, loop until it doesn't
            x = random.randint(0, WIDTH-2*xu)
            y = random.randint(0, HEIGHT-2*yu)
            gemRect = pygame.Rect([x, y, 2*xu, 2*yu])
    
        gemList.append(gemRect)
    
    return gemList


def movePlayer(keys, playerRect, speed, left, right, player):
    """
    Moves the player based on the keys pressed
    
    Parameters:
    ----------
    keys: list
        A list of all the keys pressed
    playerRect: pygame.Rect
        The player rectangle
    speed: int
        The speed of the player
    left: bool
        True if the player is facing left, False otherwise
    right: bool
        True if the player is facing right, False otherwise
    player: pygame.Surface
        The player image
    
    Returns:
    -------
    left: bool
        Updated left. True if the player is facing left, False otherwise
    right: bool
        Updated right. True if the player is facing right, False otherwise
    player: pygame.Surface
        The player image in the new location
    """
    
    #Make 4 new rectangles that are located as if the player was in that position
    new_rect_left = pygame.Rect(playerRect.left - speed, playerRect.top, playerRect.width, playerRect.height)
    new_rect_right = pygame.Rect(playerRect.left + speed, playerRect.top, playerRect.width, playerRect.height)
    new_rect_up = pygame.Rect(playerRect.left, playerRect.top - speed, playerRect.width, playerRect.height)
    new_rect_down = pygame.Rect(playerRect.left, playerRect.top + speed, playerRect.width, playerRect.height)

    if keys[pygame.K_LEFT] and not collidesWithWall(new_rect_left):
        playerRect.left -= speed
        
        if right: #If the player is facing right, flip the player image
            player = pygame.transform.flip(player, True, False)
        right = False
        left = True
    if keys[pygame.K_RIGHT] and not collidesWithWall(new_rect_right):
        playerRect.left += speed

        if left: #If the player is facing left, flip the player image
            player = pygame.transform.flip(player, True, False)
        left = False
        right = True
    if keys[pygame.K_UP] and not collidesWithWall(new_rect_up):
        playerRect.top -= speed
    if keys[pygame.K_DOWN] and not collidesWithWall(new_rect_down):
        playerRect.top += speed
    
    return left, right, player


def checkWon(gemCount, playerRect, gems, seconds):
    """
    Checks if the player has won the game
    
    Parameters:
    ----------
    gemCount: int
        The number of gems collected by the player
    playerRect: pygame.Rect
        The player rectangle
    gems: list
        A list of all the gem rectangles
    seconds: int
        The number of seconds left in the game
    
    Returns:
    -------
    bool
        True if the player has won the game, False 
    str
        A message to display if the player has not collected all the gems
    """
    
    if playerRect.colliderect(finish_line) and gemCount == 5: #Win Condition
        return True
    elif playerRect.colliderect(finish_line) or seconds == 0: #If the player has not collected all the gems or time runs out, display a message and highlight the gems hitbox
        if len(gems) != 0:
            showMessage("Collect ALL the Gems", 30, "Consolas", WIDTH//2, 50, RED)
        for rect in gems:
            pygame.draw.rect(surface, YELLOW, rect, 1)
    return False


def drawMaze():
    """
    Draws the maze on the screen
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    None
    """
    
    for wall in border_walls: #Draws the border walls
        pygame.draw.rect(surface, BLACK, wall, 0)
    for wall in horizontal_walls: #Draws the horizontal walls
        pygame.draw.rect(surface, BLACK, wall, 0)
    for wall in vertical_walls: #Draws the vertical walls
        pygame.draw.rect(surface, BLACK, wall, 0)
    pygame.draw.rect(surface, GREEN, finish_line, 0) #Draws the finish line


def main(player):
    """
    The main game loop
    
    Parameters:
    ----------
    player: pygame.Surface
        The player image
    
    Returns:
    -------
    None
    """
    
    left = False
    right = True
    playerRect = pygame.Rect([2*xu, 2*yu, 2.5*xu, 2.3*yu])
    gems = placeGems(totalGems)
    gemcount = 0
    run = True
    seconds = 20
    gameover = False

    while run:
        keys = pygame.key.get_pressed() 

        for event in pygame.event.get():
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()                          
                sys.exit()
        
            if event.type == pygame.USEREVENT and not checkWon(gemcount, playerRect, gems, seconds) and not gameover: #If a second has happendded and the game is not won or over, decrease the timer by 1 second
                seconds -= 1
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and (checkWon(gemcount, playerRect, gems, seconds) or gameover): #If the game is won or over and the user presses enter, reset the game
                left = False
                right = True
                gems = placeGems(totalGems)
                gemcount = 0
                run = True
                seconds = 20
                gameover = False
                playerRect = pygame.Rect([2*xu, 2*yu, 2.5*xu, 2.3*yu])
                player = player_original.copy() #Reset the image like the game is restarting
                            
        speed = getSpeed(gemcount) #Get the speed of the player based on the number of gems collected
        
        if not checkWon(gemcount, playerRect, gems, seconds) and not gameover: #If the game is not won or over, move the player
            left, right, player = movePlayer(keys, playerRect, speed, left, right, player)

        surface.fill(BLUE) #clears the screen with background color
        
        gemcount, gems = collidesWithGem(gems, gemcount, playerRect)
        gameover = drawScreen(gems, gemcount, seconds, player, playerRect)

        #Draws the Player Hitbox. Uncomment to see it
        #pygame.draw.rect(surface, RED, playerRect, 1)
        
        clock.tick(60) #60 FPS
        pygame.display.update()
        

main(player)