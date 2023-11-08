# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1000

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices


def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s],
                   [s,  c]])
    return R

class myPolygon():
    def __init__(self, nvertices = 3, radius=70, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.nvertices = nvertices
        self.vertices = getRegularPolygon(self.nvertices, radius=self.radius)

        self.color = color
        self.color_org = color 

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position
        pygame.draw.polygon(screen, self.color, points)
#

#과제 1: 콜리전 함수의 구현
def checkCollisionRectangle(rect1, rect2):
    flag = False # you will change this flag to True if rect1 and rect2 overlaps
    # implement it below
    diff = rect1.position - rect2.position
    min_diff = (rect1.radius + rect2.radius) / np.sqrt(2)
    flag = abs(diff[0]) <= min_diff and abs(diff[1]) <= min_diff
    # end of implementation
    return flag  

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)

def main():
    pygame.init() # initialize the engine

    #sound = pygame.mixer.Sound("assets/diyong.mp3")

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
#
    # 과제 2: 5개의 rectangles 정의
    rects = []
    for i in range(5):
        rect = myPolygon(4, np.random.uniform(50.0, 90.0), np.random.uniform(0, 256, 3), np.random.uniform(1.5, 4.0, 2))
        rect.angvel = 0
        rects.append(rect)

    done = False
    while not done:
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # drawing
        screen.fill( (200, 254, 219))

        # 과제 2: 5개의 rectangles 의 콜리전 확인
        update_list(rects)
        rects_col = [False for i in rects]
        for i in range(len(rects)):
            for j in range(i):
                if checkCollisionRectangle(rects[i], rects[j]):
                    rects_col[i] = True 
                    rects_col[j] = True
                        
        for i in range(len(rects_col)):
            if rects_col[i]:
                rects[i].color = RED
            else:
                rects[i].color = rects[i].color_org

        # DRAWING
        draw_list(rects, screen)

        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()