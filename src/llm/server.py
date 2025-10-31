from requests import get
from time import sleep
from subprocess import Popen, run
from subprocess import DEVNULL, TimeoutExpired
import atexit

from error.model import ModelNotInstalledError
from error.depencency import OllamaNotInstalledError

API_BASE = "http://localhost:11434"
START_COMMAND = ["ollama","serve"]
LIST_COMMAND = "ollama list"

ollama_process = None

def _is_running() -> bool:
    try:
        get(API_BASE)
        return True
    except:
        return False

def start():
    if not _is_running():
        global ollama_process
        try:
            ollama_process = Popen(
                START_COMMAND,
                stdout=DEVNULL,
                stderr=DEVNULL
            )
        except FileNotFoundError:
            raise OllamaNotInstalledError()
        atexit.register(_stop_server)

        while not _is_running():
            sleep(0.5)

def _stop_server():
    global ollama_process
    if ollama_process and ollama_process.poll() is None:
        ollama_process.terminate()
        try:
            ollama_process.wait(timeout=5)
        except TimeoutExpired:
            ollama_process.kill()

def get_api_base() -> str:
    return API_BASE

def get_server_model_name(model_name: str) -> str:
    return f"ollama/{model_name}"

def is_model_installed(model_name: str) -> bool:
    start()
    command = run(
        LIST_COMMAND + f" | grep {model_name}",
        shell=True,
        stdout=DEVNULL,
        stderr=DEVNULL
    )
    return command.returncode == 0

def install_model(model_name: str):
    start()
    run(
        ["ollama", "pull", model_name],
        stdout=DEVNULL,
        stderr=DEVNULL
    )

def uninstall_model(model_name: str):
    start()
    if not is_model_installed(model_name):
        raise ModelNotInstalledError(model_name) 
    run(
        ["ollama", "rm", model_name],
        stdout=DEVNULL,
        stderr=DEVNULL
    )

