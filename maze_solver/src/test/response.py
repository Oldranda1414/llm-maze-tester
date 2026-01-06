
from util import extract_direction


def run():
    response = """
      'I''m starting in the center of a 3x3 grid maze. From my current position,
      I have four directions to consider: North, East, South, and West.


      - Due North: Wall, blocked. Can''t go there.

      - Due East: Wall, blocked. Can''t go there.

      - Due South: Corridor that goes two meters before a wall. I can move forward
      and explore this path.

      - Due West: Wall, blocked. Can''t go there.


      Since North, East, and West are blocked, the only possible move is South. The
      corridor to the South is two meters long, so I should move forward to gather
      more information about this path.


      Moving South might lead me closer to the exit or provide insight into the maze''s
      layout. Since the exit is on the border, and I''m in the center, moving South
      could potentially bring me closer to the bottom edge of the maze.


      The corridor is two meters long, so after moving one meter, I''ll be at the
      midpoint of this corridor. From there, I can reassess the situation with more
      information.


      My next move is to go South. This will allow me to explore the corridor and
      potentially find the exit or gather more data about the maze.


      Final decision: Move South.'
    """

    print("response:" + response)

    direction = extract_direction(response)
    if direction:
        print("extracted direction:" + direction.to_coordinate())
    else:
        print("no direction could be extracted")
