
from openai import OpenAI

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"
OLLAMA_VIA_OPENAI = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')