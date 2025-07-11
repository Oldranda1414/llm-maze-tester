""" wrapper for LLM models using litellm """
import json
import subprocess
from typing import List, Dict

import litellm
import requests

class Model:
    """
    Wrapper for LLM models using litellm.
    This class provides a unified interface to interact with various LLM models
    through the litellm library, which supports multiple providers including OpenAI,
    Anthropic, Ollama, Hugging Face, etc.
    """
    def __init__(self, model_name: str, timeout: int = 120):
        """
        Initialize the model wrapper.
        
        Args:
            model_name (str): Name of the model to use. For Ollama models, 
                prefix with "ollama/" (e.g., "ollama/llama2").
            timeout (int): Timeout for model answer.
        """
        self.model_name = model_name
        self.timeout = timeout
        self.chat_history: List[Dict[str, str]] = []
        self.base_url = "http://localhost:11434/api"

        # If using an Ollama model but the prefix isn't provided, add it
        if not model_name.startswith("ollama/") and not "/" in model_name:
            self.model_name = f"ollama/{model_name}"
            print(f"Using model: {self.model_name}")

        # Get base model name (without provider prefix)
        self.base_model = self.model_name.split('/')[-1] if '/' in self.model_name else self.model_name

        # Check if Ollama is running and the model exists
        if self.model_name.startswith("ollama/"):
            self._check_ollama_model()

        # Ensure litellm is properly configured
        self._configure_litellm()

    def _check_ollama_model(self):
        """Check if Ollama is running and the specified model exists."""
        try:
            # Check if Ollama is running
            try:
                response = requests.get(f"{self.base_url}/tags", timeout=5)
            except requests.exceptions.ConnectionError as exc:
                print("ERROR: Ollama is not running. Please start it with 'ollama serve'")
                raise RuntimeError("Ollama server is not running") from exc

            # Check if model exists
            if response.status_code == 200:
                models_data = response.json()
                models = models_data.get("models", [])
                available_models = [model["name"] for model in models]

                if self.base_model not in available_models:
                    print(f"Model '{self.base_model}' not found locally. Available models: {', '.join(available_models)}")

                    # Ask if user wants to pull the model
                    user_input = input(f"Do you want to pull the '{self.base_model}' model? (Y/n): ")
                    if user_input.lower() == 'y' or user_input == '':
                        print(f"Pulling model '{self.base_model}'...")
                        subprocess.run(
                            ["ollama", "pull", self.base_model],
                            check=True
                        )
                        print(f"Model '{self.base_model}' pulled successfully.")
                    else:
                        print("Model not pulled. Please use one of the available models.")
                        raise ValueError(f"Model '{self.base_model}' not available")
                else:
                    print(f"Model '{self.base_model}' is available.")
        except Exception as e:
            if not isinstance(e, RuntimeError) and not isinstance(e, ValueError):
                print(f"Error checking Ollama model: {str(e)}")
            raise

    def _configure_litellm(self):
        """Configure litellm settings if needed."""
        # You can add any additional litellm configuration here
        # For example, setting API keys if using commercial services:
        # os.environ["OPENAI_API_KEY"] = "your-key"

        # Log litellm being ready
        print(f"litellm configured for model: {self.model_name}")

    def ask(self, prompt: str) -> str:
        """
        Send a prompt to the model and get its response.
        
        Args:
            prompt (str): The text prompt to send to the model
        
        Returns:
            str: The model's response
        """
        try:
            # Build messages array that includes chat history
            messages: List[Dict[str, str]] = []

            # Add previous history for context
            for entry in self.chat_history:
                messages.append({"role": "user", "content": entry["prompt"]})
                messages.append({"role": "assistant", "content": entry["response"]})

            # Add new user prompt
            messages.append({"role": "user", "content": prompt})

            # Call the model via litellm with a timeout
            response: litellm.ModelResponse = litellm.completion( # type: ignore
                model=self.model_name,
                messages=messages,
                timeout=self.timeout,
            )

            # Extract response content
            if response and hasattr(response, 'choices') and response.choices:
                choice = response.choices[0]
                content = getattr(choice, "message", None)
                if content is not None and hasattr(content, "content"):
                    response_content = content.content if content.content is not None else ""
                else:
                    response_content = "Error: Could not extract response content"
            else:
                response_content = "Error: Received empty response from model"

            # Add the interaction to chat history
            self.chat_history.append({
                "prompt": prompt,
                "response": response_content
            })

            return response_content

        except AttributeError as e:
            error_msg = f"Error querying model: {str(e)}"
            print(error_msg)
            return error_msg

    def history(self) -> List[Dict[str, str]]:
        """
        Get the chat history with this model.
        
        Returns:
            list: A list of dictionaries with prompt and response pairs
        """
        return self.chat_history

    def save(self, filepath: str) -> bool:
        """
        Save the chat history to a file.
        
        Args:
            filepath (str): Path to save the chat history file
        
        Returns:
            bool: True if saving was successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False

    def reset_chat(self):
        """
        Reset the chat history/context for the model.
        """
        self.chat_history = []
