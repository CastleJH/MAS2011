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

# 과제 1: 원과 삼각형의 Overlap 함수
def CircleTriangleOverlap (c, t):
    dist12 = np.sqrt( (c.x - (t.position[0] + t.radius/2))**2 + (c.y - t.position[1])**2 )
    if dist12 < c.radius + t.radius:
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
        if self.y < 0:
            self.vy = 0
            self.y = self.radius + 10
        if self.y + self.radius >= WINDOW_HEIGHT:
            self.vy = -1 * self.vy 
            if self.sound is not None:
                # self.sound.play()
                pass
        return
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           [self.x, self.y], 
                           radius = self.radius, )

    def print(self,):
        print("my class self.number = ", self.number)
        return
# 

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices

class myTriangle():
    def __init__(self, radius=50, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.vertices = getRegularPolygon(3, radius=self.radius)

        # self.vertices = np.array([ [100, 100],
        #                           [ 50, 200],
        #                           [150, 200]])
        self.color = color

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
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
        points = self.vertices + self.position
        pygame.draw.polygon(screen, self.color, points)
#

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)

def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("assets/diyong.mp3")

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    circ = MyCircle(x=200, y=100, vx=9., vy=0, radius=30, sound=sound, color=(255,0,0))
    # print("Initial number: ", circ.number)

    list_of_circles = []
    for i in range(5):
        c = MyCircle(x = np.random.uniform(100, WINDOW_WIDTH-100),
                    y = np.random.uniform(100, 300),
                    vx = np.random.uniform(-30, 15),
                    vy = np.random.uniform(0, 15),
                    radius=np.random.uniform(20, 70),
                    color=np.random.uniform(0, 256, size=3),
                    sound = sound)
        list_of_circles.append(c)

    tri = myTriangle(color=(100,200, 255))

    list_of_triangles = []
    for i in range(7):
        t = myTriangle(color=np.random.uniform(0, 256, size=3),
                       vel=np.random.uniform(-10.,10,size=2))
        list_of_triangles.append(t)
    
    # 과제 1: 1+7개 삼각형(모든 삼각형)
    sound_triangles = []
    sound_triangles.append(tri)
    sound_triangles.extend(list_of_triangles)

    # 과제 1: 오버랩중인 삼각형들
    list_of_overlapping_triangles = []

    done = False
    while not done:
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # drawing
        screen.fill( (200, 254, 219))

        circ.update()
        tri.update()

        for c in list_of_circles:
            c.update()
        
        # check overlap/collision
        list_of_overlapped = []
        for c in list_of_circles:
            if CirclesOverlap(circ, c) == True:
                list_of_overlapped.append(c)

        for c in list_of_overlapped:
            c.color = (255, 0, 0)

        for c in list_of_circles:
            if c not in list_of_overlapped:
                c.color = c.org_color

        update_list(list_of_triangles)

        # 과제 1: 하나라도 빨간 공과 겹치는 삼각형이 있으면 사운드 재생
        play_sound = False
        for t in sound_triangles:
            if list_of_overlapping_triangles.count(t) != 0:
                if CircleTriangleOverlap(circ, t) == False: # 이번 프레임부터 겹치지 않음
                    list_of_overlapping_triangles.remove(t)
            elif CircleTriangleOverlap(circ, t):    # 이번 프레임에 처음 겹치기 시작
                list_of_overlapping_triangles.append(t)
                play_sound = True
        if play_sound: # 연속 재생 방지
            sound.play()

        # circ.print() 
        circ.draw(screen)
        for c in list_of_circles:
            c.draw(screen)

        tri.draw(screen)
        draw_list(list_of_triangles, screen)

        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()