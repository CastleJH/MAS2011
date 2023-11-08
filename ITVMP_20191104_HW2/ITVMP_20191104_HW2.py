# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np

FPS = 60   # frames per second
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1000

def CirclesOverlap (c1, c2):
    dist12 = np.sqrt( (c1.x - c2.x)**2 + (c1.y - c2.y)**2 )
    if dist12 < c1.radius + c2.radius:
        return True # if overlaps
    return False

class MyCircle():
    def __init__(self, x, y, vx, vy, radius=40, color=None, sound = None):
        self.radius = radius 
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy 
        self.ax = 0
        self.ay = .1
        self.org_color = color if color is not None else (100, 200, 255)
        self.color = self.org_color
        self.sound = sound
        return
    
    def update(self):
        
        self.x = self.x + self.vx 
        if self.x + self.radius >= WINDOW_WIDTH:
            self.vx = -1. * self.vx 
        if self.x - self.radius < 0:
            self.vx = -1. * self.vx 

        self.y = self.y + self.vy
        self.vy = self.vy + self.ay 
        if self.y + self.radius >= WINDOW_HEIGHT:
            self.vy = -1 * self.vy 
            if self.sound is not None:
                self.sound.play()
        # 과제 2번: 스크린 상단에 닿을 때 velocity와 y값 초기화 하기
        if self.y - self.radius < 0:
            self.vy = 0
            self.y = self.radius
        return
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           [self.x, self.y], 
                           radius = self.radius, )

    def print(self,):
        print("my class self.number = ", self.number)
        return
# 



def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("assets/diyong.mp3")
    crash_sound = pygame.mixer.Sound("assets/crash.mp3")

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    circ = MyCircle(x=200, y=100, vx=9., vy=0, radius=30, sound=sound, color=(255,0,0))
    
    list_of_circles = []
    for i in range(5):
        c = MyCircle(x = np.random.uniform(100, WINDOW_WIDTH-100),
                    y = np.random.uniform(100, 300),
                    vx = np.random.uniform(-30, 15),
                    vy = np.random.uniform(0, 15),
                    radius=np.random.uniform(20, 70),
                    color=np.random.uniform(0, 256, size=3),
                    # 과제 1번: 각각의 공에 서로 다른 사운드 주기
                    sound = pygame.mixer.Sound("assets/sound%d.mp3" %i))
        list_of_circles.append(c)

    done = False
    while not done:
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # drawing
        screen.fill( (200, 254, 219))

        circ.update()

        for c in list_of_circles:
            c.update()

        # check overlap/collision
        list_of_overlapped = []
        for c in list_of_circles:
            if CirclesOverlap(circ, c) == True:
                list_of_overlapped.append(c)

        # 과제 3번: 부딪힌 공이 하나라도 있으면 crash 사운드 재생
        if len(list_of_overlapped) != 0:
            crash_sound.play()
        # 과제 3번: 부딪힌 공들을 랜덤한 위치로 옮김
        for c in list_of_overlapped:
            c.x = np.random.uniform(c.radius, WINDOW_WIDTH-c.radius)
            c.y = np.random.uniform(c.radius, WINDOW_HEIGHT-c.radius)

        for c in list_of_circles:
            if c not in list_of_overlapped:
                c.color = c.org_color

        # circ.print() 
        circ.draw(screen)

        for c in list_of_circles:
            c.draw(screen)

        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()