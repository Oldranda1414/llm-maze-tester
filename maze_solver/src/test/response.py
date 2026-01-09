from util import extract_direction


def run():
    response = """
Based on the current description, we're at a position where the East direction is blocked by a wall, and the North and South directions are also walls or have limited corridors. However, the West direction has a corridor that is two meters long with lateral paths open, meaning it's not a dead end.

Since we're trying to reach the exit, which is on the border of this 3x3 grid, moving West could lead us to a new area with potential paths to the exit. The previous move was East, and now West is the only viable open direction. This avoids oscillating and focuses on progress.

Moving West now might bring us closer to the exit. Let's go with that.
    """

    print("response:" + response)

    direction = extract_direction(response)
    if direction:
        print("extracted direction:" + direction.to_coordinate())
    else:
        print("no direction could be extracted")
