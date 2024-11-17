import os
import requests
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

class gAit:
    def __init__(self, token_file: str = "access_token.txt"):
        try:
            with open(token_file, "r") as file:
                self.access_token = file.read().strip()
        except FileNotFoundError:
            raise ValueError(f"The file {token_file} was not found. Please provide a valid file path.")
        
        self.url = "https://api-llm.ctl-gait.clientlabsaft.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "x-api-key": f"Bearer {os.getenv('X_API_KEY')}"
        }

    def ask_llm(self, prompt: str, model: str = "Azure OpenAI GPT-4o (External)") -> Optional[str]:
        """
        Generate a response from the GenAI model.
        
        Args:
            prompt (str): The input prompt for the model
            model (str): The model name to use

        Returns:
            Optional[str]: The generated response or None if the request fails
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "stream": False
        }

        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                choices = result.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content")
            else:
                print(f"Error: API request failed with status code {response.status_code}")
                print(response.text)
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

# ai = gAit()
# response = ai.ask_llm("What is (5+5)?")
# print(response)