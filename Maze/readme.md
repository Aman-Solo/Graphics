## Rendering engine and data visualization for 2D maze visualized in 3D OpenGL environment.
1 => //Maze logic// = relies on two 2D matrices that track which wall are currently standing
        Northwall: store the presence of horizontal walls
        eastwall: stores the presence of vertical walls
    both initialized to 1(binary True), meaning maze start as solid grid where every possible wall exists so to generate a path later we just change these values to 0.
2 => //Rendering engine// = the draw_grid function transate the wall matrice to a visual representation using OpenGL pipeline:
    coordinate mapping: transform grid indices into centered coordinate system, enduring the maze is rendered around the origin.
    primitive assembly: uses GL_LINES to draw horizontal(northwall) and vertical(eastwall) segments only where the matrice value is 1.
3 => 3D projection: gluPerspective establishes a 3D field of view and glTranslate sets the camera distance, so these 2 allow the 2D grid to be viewed within a 3D space.
        
## Maze generation (The eater mouth)
the GOAL here is to transform a solid grid into a navigable maze using a randomized traversal algorithm.
=> the ALGORITHM implemented a depth first search(DFS) using stack data structure.
=> the EATING MECHANISM:
      ->mouse starts at (1,1) and moves to random unvisited neighbours.
      -> as it moves it sets corresponding value in northwall or eastwall matrices to 0, effectively EATING the wall
      -> if the mouse hit a dead end, it uses the stack to backtrack to last cell with unvisited neighbours.
    => ROGUE logic(cycle):
      -> moving beyond a simple SPANNING TREE maze, a (1 in 20) chance was added for the mouse to eat an extra wall during movement. this creates cycle/ loops which defeat the simple wall following solvers.
      