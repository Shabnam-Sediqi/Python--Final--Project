import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.headUp = pygame.image.load("pictures/headUp.png").convert_alpha()
        self.headDown = pygame.image.load("pictures/headDown.png").convert_alpha()
        self.headRight = pygame.image.load("pictures/headRight.png").convert_alpha()
        self.headLeft = pygame.image.load("pictures/headLeft.png").convert_alpha()

        self.tailUp = pygame.image.load("pictures/tailUp.png").convert_alpha()
        self.tailDown = pygame.image.load("pictures/tailDown.png").convert_alpha()
        self.tailRight = pygame.image.load("pictures/tailRight.png").convert_alpha()
        self.tailLeft = pygame.image.load("pictures/tailLeft.png").convert_alpha()

        self.body_X = pygame.image.load("pictures/body_X.png").convert_alpha()
        self.body_Y = pygame.image.load("pictures/body_Y.png").convert_alpha()

        self.body_tr = pygame.image.load("pictures/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("pictures/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("pictures/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("pictures/body_bl.png").convert_alpha()
        

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
              # 1 need rect for positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
              
            # 2 what direction is the face
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
                
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_Y,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_X,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)   
                

    def update_head_graphics(self): # 3 snake head direction should update
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headLeft
        elif head_relation == Vector2(-1,0): self.head = self.headRight
        elif head_relation == Vector2(0,1): self.head = self.headUp
        elif head_relation == Vector2(0,-1): self.head = self.headDown

        ##for block in self.body:
          ##  x_pos = int(block.x*cell_size)
           ## y_pos = int(block.y*cell_size) 
           ## block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)    #create a rect
            ##pygame.draw.rect(screen,(183,111,122),block_rect)       #draw the rectangele

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tailRight
        elif tail_relation == Vector2(-1,0): self.tail = self.tailLeft
        elif tail_relation == Vector2(0,1): self.tail = self.tailDown
        elif tail_relation == Vector2(0,-1): self.tail = self.tailUp

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

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)


class FOOD:
    def __init__(self):
        self.randomize() #creates x and y position randomly  #draw a square

    def draw_food(self):
        food_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y*cell_size),cell_size,cell_size)   #creat a rectangle
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
        self.draw_score()

    def check_collision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize() # repostion the food
            self.snake.add_block() #add another block to the snake

        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:   #check if snake is ourside of the screen
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()    
        #check if snake hits itself
   
    def game_over(self):
        self.snake.reset()
        ##pygame.quit()
        ##sys.exit()    

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        drumstic_rect = drumstick.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(drumstic_rect.left,drumstic_rect.top,drumstic_rect.width + score_rect.width + 6,drumstic_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(drumstick,drumstic_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.init() #start all the different modules of Pygame( sound module, graphics module)
pygame.display.set_caption("Snake Game") #changing the pygame window name
cell_size =30 
cell_number= 20 
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()#clock object limits how fast our while loop is going ot run

drumstick = pygame.image.load("pictures/drumstick.png").convert_alpha()  
game_font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game =MAIN()
while True: # this will keep the mian surface/window of game displaying on the screen unless we mainually close it or the game ends
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
