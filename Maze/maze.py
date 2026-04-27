import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
R, C = 20, 25
CELL_SIZE = 1
northwall = [[1 for _ in range(C+1)] for _ in range(R+1)]
eastwall = [[1 for _ in range(C+1)] for _ in range(R+1)]
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
def main():
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, OPENGL | DOUBLEBUF)
    pygame.display.set_caption("maze foundation")
    gluPerspective(45, (display[0]/display[1]), 0.1, 100)
    glTranslatef(0,0,-40)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_grid()
        pygame.display.flip()
        pygame.time.wait(10)
if __name__ == "__main__":
    main()