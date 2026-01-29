from string import Template


color_explanation = """
Some of the cells of the maze have a colored floor tiles. Every color appears only once. Keep track of the ones you find, as they can help you navigate the maze.
"""

current_floor_color = Template(
    "The floor you are currently standing on is colored ${color}."
)

no_current_floor_color = (
    "The floor you are currently standing on has no distinctive color."
)

direction = Template("Due ${direction} you can see:")

additional_direction_info = " Also in this direction:"

color_direction = Template(
    "   - After ${distance} there is a floor tile colored ${color}."
)
