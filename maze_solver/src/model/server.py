from requests import get, RequestException
from time import sleep
from subprocess import Popen
from subprocess import DEVNULL, TimeoutExpired
import atexit

import ollama

from error.model import ModelAlreadyInstalledError, ModelNotInstalledError
from error.depencency import OllamaNotInstalledError

API_BASE = "http://localhost:11434"
START_COMMAND = ["ollama","serve"]

ollama_process = None
# Tracks if ollama server was started by this program or was already running on the machine
_started_by_me = False

def _is_running() -> bool:
    try:
        get(f"{API_BASE}/api/tags", timeout=1)
        return True
    except RequestException:
        return False

def start() -> None:
    if not _is_running():
        global ollama_process, _started_by_me
        try:
            ollama_process = Popen(
                START_COMMAND,
                stdout=DEVNULL,
                stderr=DEVNULL
            )
        except FileNotFoundError:
            raise OllamaNotInstalledError()
        atexit.register(stop)
        _started_by_me = True

        for _ in range(20):
            if _is_running():
                return
            sleep(0.5)
        raise RuntimeError("Ollama failed to start")

def stop() -> None:
    global ollama_process, _started_by_me
    if not _started_by_me:
        return
    if ollama_process and ollama_process.poll() is None:
        ollama_process.terminate()
        try:
            ollama_process.wait(timeout=5)
        except TimeoutExpired:
            ollama_process.kill()

def is_model_installed(model_name: str) -> bool:
    start()
    installed_models = [model.model.split(":")[0] for model in ollama.list().models if model.model is not None]
    return model_name in installed_models

def install_model(model_name: str):
    start()
    print(f"installing model {model_name}...")
    if is_model_installed(model_name):
        raise ModelAlreadyInstalledError(model_name) 
    ollama.pull(model_name)
    print(f"installed model {model_name}")

def uninstall_model(model_name: str):
    start()
    if not is_model_installed(model_name):
        raise ModelNotInstalledError(model_name) 
    ollama.delete(model_name)

