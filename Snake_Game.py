import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size) 
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)    #create a rect
            pygame.draw.rect(screen,(250,122,100),block_rect)       #draw the rectangele

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
           body_copy = self.body[:-1]
           body_copy.insert(0,body_copy[0] + self.direction)
           self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
class FOOD:
    def __init__(self):
        self.randomize()

    def draw_food(self): #creat a rectangle
        food_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y*cell_size),cell_size,cell_size)   
        screen.blit(drumstick, food_rect)


    def randomize(self):
        self.x = random.randint(0,cell_number -1)  
        self.y = random.randint(0,cell_number -1)    
        self.pos = Vector2(self.x, self.y)  
    
           
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.food.draw_food()    
        self.snake.draw_snake()

    def check_collision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize() # repostion the food
            self.snake.add_block() #add another block to the snake

    def check_fail(self):#check if snake is ourside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:   
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()    
        #check if snake hits itself
   
    def game_over(self):
        pygame.quit()
        sys.exit()    

pygame.init()
cell_size =29
cell_number= 21
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()#clock object limits how fast our while loop is going to run


drumstick = pygame.image.load("pictures/drumstick.png").convert_alpha()  



SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,220)

main_game =MAIN()
while True:
    #here we draw all our elements(drawing snake, drawing background,)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            #snake.move_sanke()
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y !=1: #restricting snake from reversing direction while it's going in one direction
                    main_game.snake.direction = Vector2(0, -1) 
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y !=-1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175,215,70))  
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)