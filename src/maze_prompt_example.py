"""
Generates some example mazes with example prompts
"""
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from maze import Maze
from prompt import generate_step_prompt

output_path = "./maze_prompt_examples"

def get_save_path(dim: int) -> str:
    return f"{output_path}/{dim}x{dim}_maze.png"

def main() -> None:
    mazes: list[tuple[str, str]] = []
    os.makedirs(output_path, exist_ok=True)
    for i in range(2, 7):
        save_path = get_save_path(i)
        m = Maze(i, i, save_path, False, False)
        m.save()
        prompt = generate_step_prompt(m)
        mazes.append((save_path, prompt))

    ## LLM generated code

    # from PIL import Image, ImageDraw, ImageFont
    #
    # # Set font
    # font = ImageFont.load_default()
    #
    # # Parameters
    # padding = 20
    # text_width = 400  # Width reserved for the text
    # background_color = "white"
    # text_color = "black"
    #
    # # Load all images
    # rows = []
    # for img_path, text in mazes:
    #     img = Image.open(img_path)
    #     # Create a blank white image to place the maze + text
    #     row_height = max(img.height, 150)
    #     row_img = Image.new("RGB", (img.width + text_width + padding * 3, row_height), background_color)
    #
    #     # Paste maze
    #     row_img.paste(img, (padding, (row_height - img.height) // 2))
    #
    #     # Draw text next to it
    #     draw = ImageDraw.Draw(row_img)
    #     text_x = img.width + padding * 2
    #     text_y = padding
    #     draw.multiline_text((text_x, text_y), text, fill=text_color, font=font, spacing=4)
    #
    #     rows.append(row_img)
    #
    # # Combine all rows vertically
    # total_height = sum(r.height for r in rows) + padding * (len(rows) + 1)
    # max_width = max(r.width for r in rows)
    # output = Image.new("RGB", (max_width, total_height), background_color)
    #
    # y = padding
    # for r in rows:
    #     output.paste(r, (padding, y))
    #     y += r.height + padding
    #
    # # Save result
    # output.save(f"{output_path}/maze_summary.png")
    # print("✅ Saved maze_summary.png")
    # Prepare figure
        fig, axes = plt.subplots(len(mazes), 2, figsize=(8, len(mazes)*4))
        if len(mazes) == 1:
            axes = [axes]  # Ensure it's iterable even for 1 row

        for i, (img_path, text) in enumerate(mazes):
            # Load the maze image
            img = mpimg.imread(img_path)
            
            # Left: the maze image
            axes[i][0].imshow(img)
            axes[i][0].axis("off")
            
            # Right: text description
            axes[i][1].text(0.0, 0.5, text, fontsize=12, va="center", wrap=True)
            axes[i][1].axis("off")

        plt.tight_layout()
        plt.savefig(f"{output_path}/maze_summary.png", bbox_inches="tight", dpi=150)


if __name__ == "__main__":
    main()
