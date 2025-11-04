from move import Direction, neighbor
from maze import Maze
from prompt.util import path_length

def is_exit_direction(direction: Direction, maze: Maze) -> bool:
    ip_x, ip_y = maze.position()
    t_x, t_y = maze.target
    pl = path_length(direction, maze)

    if ip_y == t_y:
        if direction == Direction.SOUTH:
            return t_x > ip_x and abs(t_x - ip_x) <= pl
        
        if direction == Direction.NORTH:
            return t_x < ip_x and abs(t_x - ip_x) <= pl
    
    if ip_x == t_x:
        if direction == Direction.EAST:
            return t_y > ip_y and abs(t_y - ip_y) <= pl
        
        if direction == Direction.WEST:
            return t_y < ip_y and abs(t_y - ip_y) <= pl
    
    return False

def is_dead_end(direction: Direction, maze: Maze) -> bool:
    """
    Checks if a corridor from the current position in the given direction is a dead end.
    A dead end is a corridor with no other branches along the way.
    """
    position = maze.position()
    cl = maze.connection_list()
    while cl.connected(position, position := neighbor(position, direction)):
        if cl.num_neighbors(position) > 1:
            return False
    return True

def is_wall(direction: Direction, maze: Maze) -> bool:
    """Check if there is a wall in the given direction from the current position."""
    position = maze.position()
    cl = maze.connection_list()
    return not cl.connected(position, neighbor(position, direction))

def is_out_of_sight(direction: Direction, maze: Maze, sight_depth: int) -> bool:
    return path_length(direction, maze) > sight_depth

