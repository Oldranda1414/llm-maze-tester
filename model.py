""" wrapper for LLM models using litellm """
import json
from typing import List, Dict

import litellm

class Model:
    """
    Wrapper for LLM models using litellm.
    This class provides a unified interface to interact with various LLM models
    through the litellm library, which supports multiple providers including OpenAI,
    Anthropic, Ollama, Hugging Face, etc.
    """
    def __init__(self, model_name: str):
        """
        Initialize the model wrapper.
        
        Args:
            model_name (str): Name of the model to use. For Ollama models, 
                prefix with "ollama/" (e.g., "ollama/llama2").
        """
        self.model_name = model_name
        self.chat_history: List[Dict[str, str]] = []

        # If using an Ollama model but the prefix isn't provided, add it
        if not model_name.startswith("ollama/") and not "/" in model_name:
            self.model_name = f"ollama/{model_name}"
            print(f"Using model: {self.model_name}")

        # Ensure litellm is properly configured
        self._configure_litellm()

    def _configure_litellm(self):
        """Configure litellm settings if needed."""
        # Set default timeout
        litellm.request_timeout = 120

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
            # Convert previous chat history to litellm format if it exists
            messages = []

            # Add new user prompt
            messages.append({"role": "user", "content": prompt})

            # Call the model via litellm
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
            )

            # Extract response content
            if response and hasattr(response, 'choices') and response.choices:
                response_content = response.choices[0].message.content
            else:
                response_content = "Error: Received empty response from model"

            # Add the interaction to chat history
            self.chat_history.append({
                "prompt": prompt,
                "response": response_content
            })

            return response_content

        except (litellm.LitellmError, ValueError, TypeError) as e:
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
