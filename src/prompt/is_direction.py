from move import Coordinate, Direction

def is_exit_direction(direction: Direction, position: Coordinate, target: Coordinate, path_lenght: int) -> bool:
    ip_x, ip_y = position
    t_x, t_y = target

    if ip_y == t_y:
        if direction == Direction.SOUTH:
            return t_x > ip_x and abs(t_x - ip_x) <= path_lenght
        
        if direction == Direction.NORTH:
            return t_x < ip_x and abs(t_x - ip_x) <= path_lenght
    
    if ip_x == t_x:
        if direction == Direction.EAST:
            return t_y > ip_y and abs(t_y - ip_y) <= path_lenght
        
        if direction == Direction.WEST:
            return t_y < ip_y and abs(t_y - ip_y) <= path_lenght
    
    return False

def is_dead_end(direction: Direction, position: Coordinate, connection_list: list[Coordinate]) -> bool: ...
