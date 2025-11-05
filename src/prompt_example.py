"""
Generates some example mazes with example prompts
"""
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from maze.factory import create_maze
from prompt import step_prompt

output_path = "./maze_prompt_examples"

def get_save_path(dim: int) -> str:
    return f"{output_path}/{dim}x{dim}_maze.png"

def main() -> None:
    mazes: list[tuple[str, str]] = []
    os.makedirs(output_path, exist_ok=True)
    for i in range(2, 7):
        save_path = get_save_path(i)
        m = create_maze(i)
        m.save(save_path)
        sight_depth = 2
        prompt = step_prompt(m, sight_depth)
        mazes.append((save_path, prompt))

        _, axes = plt.subplots(len(mazes), 2, figsize=(8, len(mazes)*4))
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
