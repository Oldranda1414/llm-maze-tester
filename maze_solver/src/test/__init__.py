import sys
import os
import importlib.util


def main():
    test_dir = "maze_solver/src/test/"

    if len(sys.argv) != 2:
        print(f"Error: Expected exactly 1 argument, but got {len(sys.argv) - 1}")
        print(f"Usage: python {sys.argv[0]} <filename>")
        file_names = [
            os.path.splitext(f)[0]
            for f in os.listdir(test_dir)
            if f.endswith(".py") and f != "__init__.py"
        ]
        file_names.sort()
        print("Available tests:")
        print("   " + "\n   ".join(file_names))
        sys.exit(1)
    filename = sys.argv[1]
    if not filename.endswith(".py"):
        filename += ".py"
    file_path = os.path.join(test_dir, filename)

    if not os.path.exists(file_path):
        print(f"Error: '{filename}' is not a valid test")
        sys.exit(1)

    try:
        module_name = filename[:-3] if filename.endswith(".py") else filename
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            print(f"Error: Could not load module from '{file_path}'")
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "run"):
            print(f"Error: Module '{module_name}' does not have a 'run()' function")
            sys.exit(1)
        module.run()
    except Exception as e:
        print(f"Error running test '{filename}':\n{e}")
        sys.exit(1)
