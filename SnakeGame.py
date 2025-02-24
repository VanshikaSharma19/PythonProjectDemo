import pygame # type: ignore
import sys
import os
import random
import math

pygame.init()
pygame.display.set_caption("Snake game")
pygame.font.init()
random.seed()
#Declaring global Constant definitations
SPEED = 0.30
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE   #SAme Size for both food and snake
SEPARATION = 10 #Separation between two pixels
SCREEN_HEIGHT = 600
SCREEN_WEDTH = 800
FPS =25
KEY = {"UP":1 ,"DOWN":2 ,"RIGHT":3 ,"LEFT":4}

#Lets INitialize the Screen
Screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_HEIGHT),pygame.HWSURFACE)
#We have used hw surface which stands for hardware surface refers to using memory on the video card for storing
#draws as opposed to main memory

#Resources
score_font = pygame.font.Font(None,38)
score_numb_font = pygame.font.Font(None,28)
game_over_font = pygame.font.Font(None,48)
play_again_font = score_numb_font
score_msg = score_font.render("Score:",1,pygame.Color("Green"))
score_msg_size = score_font.size("Score")
background_color = pygame.Color(0,0,0) # We will fill background Color as black
black = pygame.Color(0,0,0)

#for clock at the left corner
gameClock = pygame.time.Clock()

def checkCollision(posA,As ,posB , Bs):  #as is the size of a and bs is the size of b
    if(posA.x < posB.x+Bs and posA.x+As > posB.x and posA.y < posB.y+Bs and posA.y+As > posB.y):
        return True
    return False
#To check the boundaries here we are not limiting boundaries like it can pass through screen and come from other side

def checkLimits(snake):
    if(snake.x > SCREEN_WEDTH):
        snake.x = SNAKE_SIZE
    if(snake.x < 0):             #this will be checked when some part of snake is on other side and some on opposite side
        snake.x = SCREEN_WEDTH - SNAKE_SIZE
    if(snake.y > SCREEN_HEIGHT):
        snake.y = SNAKE_SIZE
    if(snake.y < 0):            #This also same half half
        snake.y =SCREEN_HEIGHT - SNAKE_SIZE   

#We Will make Class for food of the Snake let's name its as Apple
class Apple:
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color =pygame.color.Color("orange")  #Color of Food

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,APPLE_SIZE,APPLE_SIZE),0)

class Segment:   #initially snake will move in up direction
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY['UP']
        self.color = "white"

class Snake:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = [] # initially it will be empty
        self.stack.append(self)
        blackBox = Segment(self.x, self.y + SEPARATION)
        blackBox.direction = KEY["UP"]
        blackBox.color ="NULL"
        self.stack.append(blackBox)

#we will define moves of the snake
    def move(self):
        last_element = len(self.stack) - 1
        while(last_element != 0):
            self.stack[last_element].direction = self.stack[last_element].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element - 1].y
            last_element -= 1
        if(len(self.stack)< 2):
            last_element = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if(self.stack[0].direction == KEY["UP"]):
            last_segment.y = self.stack[0].y - (SPEED * FPS)
        elif(self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y + (SPEED * FPS)
        elif(self.stack[0].direction == KEY["LEFT"]):
            last_segment.x = self.stack[0].x - (SPEED * FPS)
        elif(self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x + (SPEED * FPS)  
        self.stack.insert(0, last_segment)   

    def getHead(self): #head of the snake
        return(self.stack[0])  #It will be always 0 index
    
    #now when snake eats food it will grow so for that we will add that food to stack

    def grow(self):
        last_element = len(self.stack) -1
        self.stack[last_element].direction = self.stack[last_element].direction
        if(self.stack[last_element].direction == KEY["UP"]):
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y -SNAKE_SIZE)
            blackBox = Segment(newSegment.x , newSegment.y-SEPARATION)

        elif(self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y -SNAKE_SIZE)
            blackBox = Segment(newSegment.x , newSegment.y+SEPARATION)

        elif(self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = Segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = Segment(newSegment.x - SEPARATION, newSegment.y)

        elif(self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = Segment(self.stack[last_element].x + SNAKE_SIZE, self.stack[last_element].y)
            blackBox = Segment(newSegment.x + SEPARATION, newSegment.y) 

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)

    def iterateSegment(self,delta):
        pass

    def setDirection(self,direction):
        if(self.direction == KEY['RIGHT'] and direction == KEY["LEFT"] or self.direction == KEY['LEFT'] and direction == KEY["RIGHT"]):
            pass
        elif(self.direction == KEY['UP'] and direction == KEY['DOWN'] or self.direction == KEY['UP'] and direction == KEY['DOWN']):
            pass
        else:
            self.direction = direction

    def get_rect(self):   #get the rectangle  shape
        rect = (self.x, self.y)
        return rect

    def getX(self):
        return self.x

    def getY(self):
        return self.y    

    #We will make the function of crashing when snake eats itself

    def checkCrashing(self):
        counter = 1
        while(counter < len(self.stack)-1):
            if(checkCollision(self.stack[0], SNAKE_SIZE, self.stack[counter], SNAKE_SIZE) and
               self.stack[counter].color != "NULL"):
                return True
            counter +=1
        return False
    #We will draw the snake
    def draw(self,screen):
        pygame.draw.rect(screen,pygame.color.Color("Green"),(self.stack[0].x , self.stack[0].y, SNAKE_SIZE, SNAKE_SIZE),0)
        counter = 1
        while(counter < len(self.stack)):
            if(self.stack[counter].color == "NULL"):
                counter +=1
                continue
            pygame.draw.rect(screen, pygame.color.Color("yellow"), (self.stack[counter].x, self.stack[counter].y, SNAKE_SIZE, SNAKE_SIZE),0)
            counter+=1



#We will define Keys
def getkey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            #for exit 
            if event.key == pygame.K_ESCAPE:
                return "exit"
            #if we want to contnue playing again
            elif event.key == pygame.K_y:
                return "YES"
            #if we dont want to play game
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            sys.exit(0)

def endGame():
    message = game_over_font.render("Game Over",1,pygame.Color("White"))
    message_play_again = play_again_font.render("play Again? (Y/N)", 1,pygame.Color("Green"))
    Screen.blit(message_play_again,(320+12+40))

    pygame.display.flip()
    pygame.display.update()

    mkey = getkey()
    while(mkey != "exit"):
        if(mkey == "YES"):
            main()
        elif(mkey=="no"):
            break
        mkey = getkey()
        gameClock.tick(FPS)
    sys.exit(0)

def drawScore(score):
    score_numb = score_numb_font.render(str(score),1,pygame.Color("Yellow"))
    Screen.blit(score_msg, (SCREEN_WEDTH - score_msg_size[0]-60,10))
    Screen.blit(score_numb,(SCREEN_WEDTH - 45,14))

def drawGameTime(gameTime):
    game_time = score_font.render("Time:" ,1,pygame.Color("White"))
    game_time_numb = score_numb_font.render(str(gameTime/1000),1,pygame.Color("White"))
    Screen.blit(game_time,(30,10))
    Screen.blit(game_time_numb,(105,14))
    
def exitScreen():
    pass

def respawnApple(apples , index, sx, sy):
    radius = math.sqrt(SCREEN_WEDTH/2*SCREEN_WEDTH/2 + SCREEN_HEIGHT/2*SCREEN_HEIGHT/2)/2
    angle = 999
    while(angle > radius):
        angle = random.uniform(0,800)*math.pi*2
        x = SCREEN_WEDTH/2 + radius * math.cos(angle)
        y = SCREEN_WEDTH/2 + radius * math.sin(angle)
        if(x==sx and y==sy):
            continue
    newApple = Apple(x, y, 1)
    apples[index]= newApple
def respawnApples(apples, quantity, sx,sy):
    counter = 0
    del apples[:]
    radius = math.sqrt((SCREEN_WEDTH/2 * SCREEN_WEDTH/2 + SCREEN_HEIGHT/2*SCREEN_HEIGHT/2))/2
    angle = 999
    while(counter < quantity):
        while(angle > radius):
            angle = random.uniform(0,800)*math.pi*2
            x = SCREEN_WEDTH/2 + radius * math.cos(angle)
            y = SCREEN_HEIGHT/2 + radius *math.sin(angle)
            if((x-APPLE_SIZE == sx or x+APPLE_SIZE==sx) and (y-APPLE_SIZE == sy or y+APPLE_SIZE == sy or radius - angle <=10)):
                continue
        apples.append(Apple(x,y,1))
        angle = 999
        counter +=1


def main():
    score = 0

#initalisation of snake
    mySnake = Snake(SCREEN_WEDTH/2,SCREEN_HEIGHT/2)
    mySnake.setDirection==KEY["UP"]
    mySnake.move()
    start_segment = 3  #initially we will be having 3 segment long snake
    while(start_segment > 0):
        mySnake.grow()
        mySnake.move()
        start_segment -=1

    #FOOD
    max_apples = 1 #1 apple when snake eats
    eaten_apple = False #as snake will eat food apple will be disappear
    apples = [Apple(random.randint(60,SCREEN_WEDTH), random.randint(60,SCREEN_HEIGHT), 1)]
    respawnApples(apples,max_apples,mySnake.x, mySnake.y)

    startTime = pygame.time.get_ticks()
    endgame= 0

    while(endgame != 1):
        gameClock.tick(FPS)

        #input
        keyPress = getkey()
        if keyPress == "exit":
            endgame = 1

            #to check collision
        checkLimits(mySnake)
        if(mySnake.checkCrashing()):
           endGame()
        for myApple in apples:
            if(myApple.state == 1):
                if(checkCollision(mySnake.getHead(), SNAKE_SIZE,myApple,APPLE_SIZE)== True):
                    mySnake.grow()
                    myApple.state=0
                    score += 10
                    eaten_apple = True
      #update postion
        if(keyPress):
            mySnake.setDirection(keyPress)
        mySnake.move()
         #if Respawning food
        if(eaten_apple == True):
                eaten_apple = False
                respawnApple(apples, 0, mySnake.getHead().x, mySnake.getHead().y)
        
        Screen.fill(background_color)
        for myApple in apples:
            if(myApple.state == 1):
                myApple.draw(Screen)
        
        mySnake.draw(Screen)
        drawScore(score)
        gameTime = pygame.time.get_ticks()- startTime
        drawGameTime(gameTime)
        
        pygame.display.flip()
        pygame.display.update()

main()      
pygame.quit()     
sys.exit()
