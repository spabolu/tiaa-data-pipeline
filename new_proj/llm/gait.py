import requests
import json
from typing import Optional

class gAit:
    def __init__(self, token_file: str = "access_token.txt"):
        # Read the access token from the text file
        with open(token_file, "r") as token_file:
            self.access_token = token_file.read().strip()
        
        self.url = "https://api-llm.ctl-gait.clientlabsaft.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "x-api-key": "Bearer sk-pyzdF3wj2CFkA_C0jzzdgA"
        }

    def ask_llm(self, prompt: str, model: str = "Azure OpenAI GPT-4o (External)") -> Optional[str]:
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
                    return choices[0].get("response", {}).get("content")
            else:
                print(f"Error: API request failed with status code {response.status_code}")
                print(response.text)
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
