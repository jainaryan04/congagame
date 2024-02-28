import pygame
from pygame.locals import *
import time
import random
SIZE=40
BG_CLR=(50, 168, 107)

class Follower:
    
    def __init__(self,parent_screen):
        self.image=pygame.image.load("Media/follower.jpg").convert()
        self.parent_screen=parent_screen
        self.l=SIZE*3
        self.b=SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image,(self.l,self.b))
        pygame.display.update()
    
    def move(self):
        self.l=random.randint(0,14)*SIZE
        self.b=random.randint(0,19)*SIZE


class Chain:
    def __init__(self,surface,length):
        self.length=length
        self.parent_screen=surface
        self.block=pygame.image.load("Media/block.jpg").convert()

        self.l=[SIZE]*length
        self.b=[SIZE]*length
        self.direction='down'
        pygame.mixer.init()

    
    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'

    def walk(self):
        for i in range (self.length-1,0,-1):
            self.l[i]=self.l[i-1]
            self.b[i]=self.b[i-1]
        if self.direction=='left':
            self.l[0]-=SIZE
        if self.direction=='right':
            self.l[0]+=SIZE
        if self.direction=='up':
            self.b[0]-=SIZE
        if self.direction=='down':
            self.b[0]+=SIZE
        self.draw()
        if self.l[0]>600 or self.b[0]>800 or self.l[0]<0 or self.b[0]<0:
            Game.play_sound("gover.wav")
            Game.show_game_over()

    def draw(self):
        self.parent_screen.fill(BG_CLR)
        for i in range (self.length):

            self.parent_screen.blit(self.block,(self.l[i],self.b[i]))
        pygame.display.update()

    def increase_length(self):
        self.length+=1
        self.l.append(-1)
        self.b.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        self.play_bgmusic()
        self.surface=pygame.display.set_mode((600,800))
        self.chain=Chain(self.surface,1)
        self.chain.draw()
        self.follower=Follower(self.surface)
        self.follower.draw()
    
    def show_game_over(self):
        self.surface.fill(BG_CLR)
        
    
    def run(self):
        con=True
        pause=False
        while con:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        con=False
                    if not pause:
                        if event.key==K_UP:
                            self.chain.move_up()
                        if event.key==K_DOWN:
                            self.chain.move_down()
                        if event.key==K_LEFT:
                            self.chain.move_left()
                        if event.key==K_RIGHT:
                            self.chain.move_right()
                    if event.key==K_RETURN:
                        pause=False
                        pygame.mixer.music.unpause()
                    if event.key==K_ESCAPE:
                        con=False
           
                elif event.type==QUIT:
                    con=False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True 
                self.chain=Chain(self.surface,1)
                   
            time.sleep(.2)
    
    def play_bgmusic(self):
        pygame.mixer.music.load("Media/bgmusic.mp3")
        pygame.mixer.music.play()

    def play_sound(sound):
        sound=pygame.mixer.Sound(f"Media/{sound}")
        pygame.mixer.Sound.play(sound)

    

    def play(self):
        self.chain.walk()
        self.follower.draw()
        self.display_score()
        pygame.display.update()
        if self.is_collision(self.chain.l[0],self.chain.b[0],self.follower.l,self.follower.b):
            Game.play_sound("ding.mp3")
            self.chain.increase_length()
            self.follower.move()

        for i in range (1,self.chain.length):
            if self.is_collision(self.chain.l[0], self.chain.b[0], self.chain.l[i],self.chain.b[i]):
                Game.play_sound("gover.wav")
                raise"Collision"
            
    def show_game_over(self):
        self.surface.fill(BG_CLR)
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is Over. Your Followers Are: {self.chain.length-1}",True,(255,255,255))
        self.surface.blit(line1,(100,300))
        line2=font.render("Press ENTER to play again.",True,(255,255,255))
        line3=font.render("Press ESCAPE to exit.",True,(255,255,255))  
        self.surface.blit(line2,(100,350))
        self.surface.blit(line3,(100,400))
        pygame.display.update()
        pygame.mixer.music.pause()
        



    def is_collision(self,x1,y1,x2,y2): 
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
        return False
    

    
    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Followers: {self.chain.length-1}",True,(255,255,255))
        self.surface.blit(score,(450,10))
            
                 

if __name__=="__main__":
    game=Game()
    game.run()
    
