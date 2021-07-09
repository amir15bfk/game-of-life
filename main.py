import pygame ,sys,random
from pygame.locals import *
pygame.init()
SCREEN_WIDTH =1200
FULL_SCREEN_WIDTH=SCREEN_WIDTH+300
SCREEN_HEIGHT =1000
PIXEL_SIZE = 20
BG_COLOR=pygame.Color(255,255,255)
OBJ_COLOR=pygame.Color(0,0,0)
FONT = pygame.font.Font("OpenSans-Bold.ttf",24)
#FONT = pygame.font.Font("OpenSans-Regular.ttf",16)
class Game_env:
    def __init__(self):
        self.screen = pygame.display.set_mode((FULL_SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('game of life')
        self.grid = self.newGrid()
        self.backup = self.grid
        self.game_state = 0
        self.framrate=30
        #load images
        self.start_button_img = pygame.image.load('img/start.png').convert_alpha()
        self.pause_button_img = pygame.image.load('img/pause.png').convert_alpha()
        self.resume_button_img = pygame.image.load('img/resume.png').convert_alpha()
        self.reset_button_img = pygame.image.load('img/reset.png').convert_alpha()
        self.clear_button_img = pygame.image.load('img/clear.png').convert_alpha()
        self.random_button_img = pygame.image.load('img/random.png').convert_alpha()
        self.step_button_img = pygame.image.load('img/step.png').convert_alpha()
        self.slow_button_img = pygame.image.load('img/slow.png').convert_alpha()
        self.fast_button_img = pygame.image.load('img/fast.png').convert_alpha()
        self.amir_button_img = pygame.image.load('img/amir.png').convert_alpha()
        self.logo_button_img = pygame.image.load('img/logo.png').convert_alpha()
        self.logo_button=Button(self.logo_button_img,SCREEN_WIDTH+25,10)
        self.play_button=Button(self.start_button_img,SCREEN_WIDTH+25,300)
        self.speed_button=Button(self.step_button_img,SCREEN_WIDTH+25,425)
        self.reset_button=Button(self.reset_button_img,SCREEN_WIDTH+25,550)
        self.clear_button=Button(self.clear_button_img,SCREEN_WIDTH+25,675)
        self.random_button=Button(self.random_button_img,SCREEN_WIDTH+25,800)
        self.amir_button=Button(self.amir_button_img,SCREEN_WIDTH+25,SCREEN_HEIGHT-70)
        self.number_of_cells=0
        self.round_number=0
        self.bord_reflash()
        

    def bord_reflash(self):
        num_text = FONT.render(f"number of cells : {self.number_of_cells}",False,OBJ_COLOR)
        round_text = FONT.render(f"round number : {self.round_number}",False,OBJ_COLOR)
        self.screen.blit(num_text,(SCREEN_WIDTH+25,200))
        self.screen.blit(round_text,(SCREEN_WIDTH+25,230))
    
    def newGrid(self):
        grid = list(range(int(SCREEN_WIDTH/PIXEL_SIZE)))
        for row in grid:
            grid[row]=[0] * int(SCREEN_HEIGHT/PIXEL_SIZE)
        for i in range(int(SCREEN_WIDTH/PIXEL_SIZE)):
            for j in range(int(SCREEN_HEIGHT/PIXEL_SIZE)):
                grid[i][j]=Obj(PIXEL_SIZE*i+1,PIXEL_SIZE*j+1)
        return grid
    
    def clear(self):
        self.grid = self.newGrid()
        self.number_of_cells=0
        self.round_number=0

    
    def random_grid(self):
        self.number_of_cells=0
        for i in range(int(SCREEN_WIDTH/PIXEL_SIZE)):
            for j in range(int(SCREEN_HEIGHT/PIXEL_SIZE)):
                self.grid[i][j].state=random.randint(0,1)
                self.number_of_cells+=self.grid[i][j].state
        
        self.round_number=0

    def draw(self):
        self.screen.fill(BG_COLOR)
        pygame.draw.line(self.screen,OBJ_COLOR,(SCREEN_WIDTH+1,0),(SCREEN_WIDTH+1,SCREEN_HEIGHT),4)
        self.logo_button.draw(self.screen)
        self.play_button.draw(self.screen)
        self.speed_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.clear_button.draw(self.screen)
        self.random_button.draw(self.screen)
        self.amir_button.draw(self.screen)
        self.bord_reflash()
        for row in self.grid:
            for item in row:
                if item.state:
                    pygame.draw.rect(self.screen,OBJ_COLOR,item)
    
    def round(self):
        temp_grid = self.newGrid()
        self.number_of_cells=0
        flag = False
        for i in range(int(SCREEN_WIDTH/PIXEL_SIZE)):
            for j in range(int(SCREEN_HEIGHT/PIXEL_SIZE)):
                num_of_nei = self.count_nei(i,j)
                if (num_of_nei < 2 or num_of_nei > 3 )and self.grid[i][j].state==1:
                    temp_grid[i][j].state=0
                    flag = True
                elif num_of_nei == 3 and self.grid[i][j].state==0 :
                    temp_grid[i][j].state=1
                    flag = True
                else:
                    temp_grid[i][j].state=self.grid[i][j].state
                self.number_of_cells+=temp_grid[i][j].state
        self.grid=temp_grid
        self.round_number+=1
        if not flag:
            self.play_button.set_img(self.start_button_img)
            self.speed_button.set_img(self.step_button_img)
            self.framrate=30
            self.game_state=0

    def correct_pos_x(self,x):
        return(x+(SCREEN_WIDTH//PIXEL_SIZE))%(SCREEN_WIDTH//PIXEL_SIZE)
    def correct_pos_y(self,y):
        return(y+(SCREEN_HEIGHT//PIXEL_SIZE))%(SCREEN_HEIGHT//PIXEL_SIZE)
    def count_nei(self,x,y):
        sum=-self.grid[x][y].state
        for i in range(-1,2):
            tempx=self.correct_pos_x(x+i)
            for j in range(-1,2):
                tempy=self.correct_pos_y(y+j)
                sum+=self.grid[tempx][tempy].state
        return sum
    
    
    def loop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.round()
                    if event.key == pygame.K_r:
                        self.random_grid()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button==1:
                        mx,my=pygame.mouse.get_pos()
                        if mx<SCREEN_WIDTH:
                            self.grid[mx//PIXEL_SIZE][my//PIXEL_SIZE].change_state()
                            self.backup = self.grid
                            self.number_of_cells+=1
                            self.round_number=0
                        elif self.play_button.rect.collidepoint((mx,my)):
                            self.game_state=self.game_state*(1-self.game_state)+(1-self.game_state)
                            if self.game_state == 1:
                                self.play_button.set_img(self.pause_button_img)
                                self.speed_button.set_img(self.slow_button_img)
                                self.framrate=10
                            else:
                                self.play_button.set_img(self.start_button_img)
                                self.speed_button.set_img(self.step_button_img)
                                self.framrate=30
                        elif self.speed_button.rect.collidepoint((mx,my)):
                            if self.framrate==30:
                                self.round()
                            elif self.framrate==10:
                                self.speed_button.set_img(self.fast_button_img)
                                self.framrate=60
                            else:
                                self.speed_button.set_img(self.slow_button_img)
                                self.framrate=10
                        elif self.reset_button.rect.collidepoint((mx,my)):
                            self.grid = self.backup
                            self.play_button.set_img(self.start_button_img)
                            self.speed_button.set_img(self.step_button_img)
                            self.framrate=30
                            self.game_state = 0
                        elif self.clear_button.rect.collidepoint((mx,my)):
                            self.clear()
                            self.play_button.set_img(self.start_button_img)
                            self.speed_button.set_img(self.step_button_img)
                            self.framrate=30
                            self.game_state = 0
                        elif self.random_button.rect.collidepoint((mx,my)):
                            self.random_grid()
                            self.play_button.set_img(self.start_button_img)
                            self.speed_button.set_img(self.step_button_img)
                            self.framrate=30
                            self.game_state = 0
            self.draw()
            if self.game_state:
                self.round()
            # Updating the window
            pygame.display.flip()
            self.clock.tick(self.framrate)
class Button():
    def __init__(self,img,x,y,scale=1):
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width*scale),int(height*scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft=(x,y)
    
    def draw(self,screen):
        screen.blit(self.img,(self.rect.x,self.rect.y))
    
    def set_img(self,img):
        self.img = img
        
class Obj():

    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,PIXEL_SIZE-2,PIXEL_SIZE-2)
        self.state=0
        
    
    def change_state(self):
        self.state=self.state*(1-self.state)+(1-self.state)
game =Game_env()
game.loop()
