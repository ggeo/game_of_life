import numpy as np
import matplotlib.pyplot as plt
from JSAnimation.IPython_display import display_animation, anim_to_html
from matplotlib import animation

def initialize_grid(rows, cols):
    """
    Initialize the grid with random values.
    
    Parameters
    ----------
    rows : int
           The number of grid rows.
    cols : int
           The number of grid columns.
    Returns
    -------
    grid : np.ndarray
           The 2D grid filled with random values (0 and 1).
           0 is a dead cell 
           1 is an alive cell
    """
    grid = np.random.randint(2, size=(rows, cols))   
    return grid

def count_neighbours(grid):
    """
    Count the number of the alive neighbours.
    
    Parameters
    ----------
    grid : np.ndarray
           The 2D grid filled with random values (0 and 1).
           
    Returns
    -------
    neighbours : np.ndarray
                 The 2D grid filled with alive neighbours.
    """
    # neighbours has the same dimensions as the grid
    neighbours = np.zeros_like(grid)
    
    for idx in range(1, grid.shape[0] - 1):
        # Instead of the inner loop we are using a numpy array 
        # so, instead of doing a[0, 1] = sth, a[0, 2] =sth,
        # we are doing a[0, [1, 2]] = sth
        idy = np.arange(1, grid.shape[1] - 1)
        # We are taking all neighbours into account
        # right, left, up, down, diagonal
        neighbours[idx, idy] = grid[idx, idy + 1] + grid[idx, idy -1] + grid[idx + 1, idy] + grid[idx - 1, idy] + \
        grid[idx - 1, idy - 1] + grid[idx + 1, idy +1] + grid[idx + 1, idy - 1] + grid[idx - 1, idy + 1]
        
    return neighbours                
        
    
def game_of_life(grid):
    """
    Run the game of life according to following rules:
    
    1) A live cell with fewer than 2 neighbours dies (undepopulation).
    2) A live cell with more than 2 live neighbours dies (overcrowding).
    3) A live cell with 2 or 3 live neighbours lives.
    4) A dead cell with exactly 3 live neighbours becomes a live cell.
    
    Parameters
    ----------
    grid : np.ndarray
           The grid on which the game of life will run.
    
    Returns
    -------
    grid : np.ndarray
           The updated grid after the system has been 
           envolved.
    """
    neighbours = count_neighbours(grid)
    for idx in range(grid.shape[0] - 1):
        for idy in range(grid.shape[1] - 1):
            if grid[idx, idy] == 1 and (neighbours[idx, idy] < 2 or neighbours[idx, idy] > 3):
                grid[idx, idy] = 0
            elif grid[idx, idy] == 1 and (neighbours[idx, idy] == 2 or neighbours[idx, idy] == 3):
                grid[idx, idy] = 1
            elif neighbours[idx, idy] == 3 and grid[idx, idy] == 0:
                grid[idx, idy] = 1
                
    return grid
            
# ------------- Initial setup ------------------------------- #
rows = 128
cols = 128
grid = initialize_grid(rows, cols)
neighbours = count_neighbours(grid)
game = game_of_life(grid)
game_blank = np.zeros_like(game)

# ---------- Just plot the image ----------------------- #
#plt.imshow(game,cmap='viridis', interpolation='nearest')
#plt.grid(False)
#plt.show()
# ------------------------------------------------------ #

def running_JSAnimation():
    dpi = 40
    mode = 'loop'
    figsize = (game.shape[1] * 1. / dpi, game.shape[0] * 1. / dpi)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
    im = ax.imshow(game, cmap=plt.cm.binary, interpolation='nearest')
    # initialization function: plot the background of each frame
    def init():
        im.set_data(game_blank)
        return (im,)

    # animation function.  This is called sequentially
    def animate(i):
        im.set_data(animate.game)
        animate.game = game_of_life(animate.game)
        return (im,)
    animate.game = game

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=100)
    return display_animation(anim, default_mode=mode)

def running_JSAnimation_simpler():
    fig, ax = plt.subplots(1, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    im = ax.imshow(game, cmap='viridis', interpolation='nearest')

    def init():    
        im.set_data(game_blank)
        return im,

    def animate(i):
        im.set_data(game_of_life(game))   
        return im,

    anim = animation.FuncAnimation(fig, animate, frames=50, interval=100)
    #anim.save('game_of_life.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    return anim

# Plot
#running_JSAnimation()
running_JSAnimation_simpler()