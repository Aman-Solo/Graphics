import pygame
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
R, C = 20, 25
CELL_SIZE = 1
northwall = [[1 for _ in range(C+1)] for _ in range(R+1)]
eastwall = [[1 for _ in range(C+1)] for _ in range(R+1)]
visited = [[False for _ in range(C+1)] for _ in range(R+1)]
eastwall[0][0] = 0
eastwall[R-1][C] = 0
curr_i, curr_j = 1,1
visited[curr_i][curr_j] = True
stack = []
generating = True
def draw_grid():
    glColor3f(1,1,1)
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(R+1):
        for j in range(C+1):
            x = j*CELL_SIZE - (C*CELL_SIZE/2)
            y = i*CELL_SIZE - (R*CELL_SIZE/2)
            if j<C and northwall[i][j] == 1:
                glVertex2f(x,y)
                glVertex2f(x+CELL_SIZE, y)
            if i<R and eastwall[i][j] == 1:
                glVertex2f(x,y)
                glVertex2f(x, y+CELL_SIZE)
    glEnd()
def draw_mouse():
    x = (curr_j -1)*CELL_SIZE - (C*CELL_SIZE/2)
    y = (curr_i -1)*CELL_SIZE - (R*CELL_SIZE/2)
    glColor3f(1,0,0)
    glBegin(GL_QUADS)
    p = 0.2
    glVertex2f(x+p, y+p)
    glVertex2f(x+CELL_SIZE-p, y+p)
    glVertex2f(x+CELL_SIZE-p, y+CELL_SIZE-p)
    glVertex2f(x+p, y+CELL_SIZE-p)
    glEnd()
def generate_step():
    global curr_i, curr_j, generating
    neighbours = []
    if curr_i < R and not visited[curr_i +1][curr_j]:
        neighbours.append(('N', curr_i +1, curr_j))
    if curr_i > 1 and not visited[curr_i -1][curr_j]:
        neighbours.append(('S', curr_i -1, curr_j))
    if curr_j < C and not visited[curr_i][curr_j +1]:
        neighbours.append(('E', curr_i, curr_j+1))
    if curr_j >1 and not visited[curr_i][curr_j -1]:
        neighbours.append(('W', curr_i, curr_j -1))
    if neighbours:
        direction, next_i, next_j = random.choice(neighbours)
        stack.append((curr_i, curr_j))
        if direction == 'N':
            northwall[curr_i][curr_j - 1] = 0
        elif direction == 'S':
            northwall[curr_i - 1][curr_j - 1] = 0
        elif direction == 'E':
            eastwall[curr_i - 1][curr_j] = 0
        elif direction == 'W':
            eastwall[curr_i - 1][curr_j - 1] = 0
        curr_i, curr_j = next_i, next_j
        visited[curr_i][curr_j] = True
    elif stack:
        curr_i, curr_j = stack.pop()
    else:
        generating = False
def main():
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, OPENGL | DOUBLEBUF)
    pygame.display.set_caption("maze foundation")
    gluPerspective(45, (display[0]/display[1]), 0.1, 100)
    glTranslatef(0,0,-40)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        if generating:
            generate_step()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_grid()
        if generating:
            draw_mouse()
        pygame.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main()