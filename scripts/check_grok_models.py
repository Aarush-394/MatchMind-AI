
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("XAI_API_KEY")
base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")

if not api_key:
    raise SystemExit("XAI_API_KEY is missing from your .env file.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

try:
    models = client.models.list()

    print("\nModels available to this API key:\n")

    for model in models.data:
        print(model.id)

except Exception as error:
    print(f"Could not retrieve models: {error}")
