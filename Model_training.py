import os

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API Key not found in environment variables!")


