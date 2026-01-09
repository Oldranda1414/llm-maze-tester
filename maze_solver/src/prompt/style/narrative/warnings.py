from string import Template


illegal_answer = """
Your last answer did not end with a valid direction.

Remember that your answers must end by providing the direction you want to move to.

The valid directions you can provide are north, east, south, west.

The last character in your response must be one of the valid directions, including eventual punctuation, so remove it from your last phrase please

You are allowed to output the direction with any casing you want, as long as it is the last thing in your answer.
Here are some examples of valid end of response, in case you decide to move due north:

- Let's go North
- I want to step N!
- My next move will be north.

"""

illegal_direction = Template(
    """
You try to walk ${direction}.
You walk directly into a wall, hitting your nose. Place more attention on the direcions that are available to you!
"""
)
