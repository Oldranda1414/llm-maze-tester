""" wrapper for Ollama models """
import subprocess
import json
import time
import atexit

import requests

TIMEOUT_TIME = 10  # seconds

class Model:
    """
    Wrapper for Ollama models to handle interactions and manage the server.
    This class ensures that the Ollama server is running and the specified model
    is loaded before making any requests.
    It also provides methods to send prompts to the model and retrieve responses,
    as well as to save the chat history.
    """
    def __init__(self, model_name):
        """
        Initialize with the Ollama model name and load if not available locally.
        Automatically starts ollama if not running.
        
        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name
        self.chat_history = []
        self.base_url = "http://localhost:11434/api"
        self.ollama_process = None

        # Start Ollama if not running
        self._ensure_ollama_running()

        # Check if model is available locally
        self._ensure_model_loaded()

    def _ensure_ollama_running(self):
        """Check if Ollama server is running, start it if not."""
        try:
            # Try to connect to Ollama API
            response = requests.get(f"{self.base_url}/version", timeout=TIMEOUT_TIME)
            print("Ollama is already running.")
            return
        except requests.exceptions.RequestException:
            print("Ollama is not running. Starting Ollama server...")

            # Start the Ollama server as a subprocess
            try:
                self.ollama_process = subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Register cleanup function to terminate Ollama when the script exits
                atexit.register(self._cleanup_ollama)

                # Wait for Ollama to start (check every second for up to 30 seconds)
                for _ in range(30):
                    try:
                        response = requests.get(f"{self.base_url}/version", timeout=2)
                        if response.status_code == 200:
                            print("Ollama server started successfully.")
                            return
                    except requests.exceptions.RequestException:
                        pass
                    time.sleep(1)

                raise RuntimeError("Timed out waiting for Ollama server to start") from None
            except (IOError, OSError) as e:
                raise RuntimeError(f"Failed to start Ollama server: {str(e)}") from e

    def _cleanup_ollama(self):
        """Terminate the Ollama process when the script exits."""
        if self.ollama_process is not None:
            print("Shutting down Ollama server...")
            try:
                self.ollama_process.terminate()
                self.ollama_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ollama_process.kill()
            print("Ollama server shut down.")

    def _ensure_model_loaded(self):
        """Check if the model is loaded and load it if necessary."""
        try:
            # Check if model exists locally
            response = requests.get(f"{self.base_url}/tags", timeout=2)
            if response.status_code != 200:
                raise RuntimeError(f"Failed to get model list. Status code: {response.status_code}")

            try:
                models_data = response.json()
                models = models_data.get("models", [])

                model_exists = any(model["name"] == self.model_name for model in models)

                if not model_exists:
                    print(f"Model {self.model_name} not found locally. Pulling from Ollama...")
                    # Run the command without capturing output to show it in real-time
                    result = subprocess.run(
                        ["ollama", "pull", self.model_name],
                        check=True
                    )
                    if result.returncode != 0:
                        raise RuntimeError(f"Failed to pull model: return code {result.returncode}")
                    print(f"Model {self.model_name} pulled successfully.")
                else:
                    print(f"Model {self.model_name} is already available locally.")
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON response from Ollama API: {e}. Response content: {response.text[:100]}") from e
        except Exception as e:
            raise RuntimeError(f"Error ensuring model is loaded: {str(e)}") from e

    def ask(self, prompt):
        """
        Send a prompt to the model and get its response.
        
        Args:
            prompt (str): The text prompt to send to the model
        
        Returns:
            str: The model's response
        """
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            # Send request to Ollama API
            response = requests.post(f"{self.base_url}/generate", json=payload, timeout=TIMEOUT_TIME)

            if response.status_code != 200:
                return f"Error: API returned status code {response.status_code}"

            try:
                response_data = response.json()
                response_content = response_data.get("response", "")

                # Add the interaction to chat history
                self.chat_history.append({
                    "prompt": prompt,
                    "response": response_content
                })

                return response_content
            except json.JSONDecodeError:
                return "Error: Could not parse API response as JSON"

        except requests.exceptions.RequestException as e:
            error_msg = f"Request error querying model: {str(e)}"
            print(error_msg)
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = f"JSON decode error querying model: {str(e)}"
            print(error_msg)
            return error_msg

    def history(self):
        """
        Get the chat history with this model.
        
        Returns:
            list: A list of dictionaries with prompt and response pairs
        """
        return self.chat_history

    def save(self, filepath):
        """
        Save the chat history to a file.
        
        Args:
            filepath (str): Path to save the chat history file
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False
