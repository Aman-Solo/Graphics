import pygame
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
R, C = 20, 25
CELL_SIZE = 1

# DATA STRUCTURES REQUIRMENTS
# About the wall integrity: if northwall [i][j] is 1, the ij-th wall cell has a solid upper wall, otherwise the wall is missing.
# The Bottom Edge: The zeroth row is a phantom row of cells below the maze whose north walls make up the bottom edge of the maze.
northwall = [[1 for _ in range(C+1)] for _ in range(R+1)]

# the Left Edge: similarly, eastwall[i][0] specifies where any gaps appear in the left edge of the maze.
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
def draw_mouse(mi, mj, color):
    x = (mj -1)*CELL_SIZE - (C*CELL_SIZE/2)
    y = (mi -1)*CELL_SIZE - (R*CELL_SIZE/2)
    glColor3f(*color)
    glBegin(GL_QUADS)
    p = 0.2
    glVertex2f(x+p, y+p)
    glVertex2f(x+CELL_SIZE-p, y+p)
    glVertex2f(x+CELL_SIZE-p, y+CELL_SIZE-p)
    glVertex2f(x+p, y+CELL_SIZE-p)
    glEnd()

# THE MAZE GENERATION LOGIC
# The mouse randomely eats through walls to connect adjacent cells.
# and we use stack for the DFS generation.
def generate_step():
    global curr_i, curr_j, generating
    neighbours = []

    # this part checks the four neighbour cells which are above, below, left and right for unvisited candidates.
    if curr_i < R and not visited[curr_i +1][curr_j]:
        neighbours.append(('N', curr_i +1, curr_j))
    if curr_i > 1 and not visited[curr_i -1][curr_j]:
        neighbours.append(('S', curr_i -1, curr_j))
    if curr_j < C and not visited[curr_i][curr_j +1]:
        neighbours.append(('E', curr_i, curr_j+1))
    if curr_j >1 and not visited[curr_i][curr_j -1]:
        neighbours.append(('W', curr_i, curr_j -1))
    if neighbours:
        # 1. this chooses one candidate randomely and eat through the connecting wall.
        direction, next_i, next_j = random.choice(neighbours) 
        stack.append((curr_i, curr_j)) # saving the layout location of the remaining candidates on a stack.
        
        # 2. this part is for the wall that is eaten and that it will be erased (set to zero).
        if direction == 'N':
            northwall[curr_i][curr_j - 1] = 0
        elif direction == 'S':
            northwall[curr_i - 1][curr_j - 1] = 0
        elif direction == 'E':
            eastwall[curr_i - 1][curr_j] = 0
        elif direction == 'W':
            eastwall[curr_i - 1][curr_j - 1] = 0

        # CHALLENGE / ADDENDUM BONUS
        # i in 20 times, eat an extra wall.
        # this creates cycles that encircle the ending cell and defeat the shoulder to wall maze solving method.
        if random.randint(1,20) ==1:
            extra_dirs = []
            if curr_i < R: extra_dirs.append('N')
            if curr_i >1: extra_dirs.append('S')
            if curr_j <C: extra_dirs.append('E')
            if curr_j >1: extra_dirs.append('W')
            if extra_dirs:
                rogue_dir = random.choice(extra_dirs)
                if rogue_dir == 'N':
                    northwall[curr_i][curr_j -1] = 0
                elif rogue_dir =='S':
                    northwall[curr_i -1][curr_j -1] =0
                elif rogue_dir == 'E':
                    eastwall[curr_i-1][curr_j] = 0
                elif rogue_dir == 'W':
                    eastwall[curr_i -1][curr_j -1] =0
        curr_i, curr_j = next_i, next_j
        visited[curr_i][curr_j] = True
    
    # 3. this is when trapped in a dead end (like surrounded by visited cells), pop unvisited cell and continue.
    elif stack:
        curr_i, curr_j = stack.pop()
    # 4. when stack is empty, all cells have been visited, so maze is complete.
    else:
        generating = False
        setup_solver()
solving = False
solve_visited = [[False for _ in range(C+1)] for _ in range(R+1)]
solve_stack = []
solve_i, solve_j = 1,1
solve_visited[solve_i][solve_j] = True
path = []
def setup_solver():
    global solving
    solving = True
    solve_stack.append((solve_i, solve_j))

# RUNNING THE MAZE (BACKTRACKING ALGORITHM)
def solve_step():
    global solve_i, solve_j, solving
    if solve_i ==R and solve_j ==C:
        solving = False
        return
    neighbours = []
    if solve_i < R and northwall[solve_i][solve_j -1] ==0 and not solve_visited[solve_i +1][solve_j]:
        neighbours.append((solve_i +1, solve_j))
    if solve_i >1 and northwall[solve_i -1][solve_j -1] ==0 and not solve_visited[solve_i -1][solve_j]:
        neighbours.append((solve_i -1, solve_j))
    if solve_j <C and eastwall[solve_i -1][solve_j] ==0 and not solve_visited[solve_i][solve_j +1]:
        neighbours.append((solve_i, solve_j +1))
    if solve_j >1 and eastwall[solve_i -1][solve_j-1]==0 and not solve_visited[solve_i][solve_j -1]:
        neighbours.append((solve_i, solve_j-1))
    if neighbours:
        # we try to move in an available direction.
        # places its position on a stack and moves to the next cell.
        solve_stack.append((solve_i, solve_j))
        solve_i, solve_j = neighbours[0]
        solve_visited[solve_i][solve_j] = True
    elif solve_stack:
        # when the mouse runs into a dead end, it backtracks by popping the last position from the stack.
        solve_i, solve_j = solve_stack.pop()
def draw_path():
    glColor3f(0,0,1)
    glPointSize(5)
    glBegin(GL_POINTS)
    for (si, sj) in solve_stack:
        x=(sj -1)*CELL_SIZE - (C*CELL_SIZE/2)+ (CELL_SIZE/2)
        y=(si -1)*CELL_SIZE - (R*CELL_SIZE/2)+ (CELL_SIZE/2)
        glVertex2f(x,y)
    glEnd()
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
        elif solving:
            solve_step()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_grid()
        if generating:
            draw_mouse(curr_i, curr_j, (1,0,0))
        if not generating:
            draw_path()
            if solving:
                draw_mouse(solve_i, solve_j, (0,1,0))
        pygame.display.flip()
        clock.tick(40)
if __name__ == "__main__":
    main()