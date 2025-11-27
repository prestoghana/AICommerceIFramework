import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)


# Base URL for Vaulta API (live environment)
BASE_URL = "https://backend.vaulta.digital/api/v1"

# Replace with your actual API key from the Vaulta Dashboard
# API_KEY = "VAULTA_TEST_123456789"

# Endpoint to get supported currency pairs
url = f"{BASE_URL}/pairs"

# headers = {
#     "x-api-key": API_KEY
# }

response = requests.get(url)
print(response.json())
if response.status_code == 200:
    pairs = response.json()
    print(f"Supported currency pairs:{pairs['markets']} ")
else:
    print(f"Error {response.status_code}: {response.text}")





# Replace with your actual API key from the Vaulta Dashboard
VAULTA_API_KEY = os.getenv("VAULTA_API_KEY")

# Endpoint to create a quote
quotes_url = f"{BASE_URL}/get_quote"

headers = {
    "x-api-key": VAULTA_API_KEY,
    "Content-Type": "application/json"
}

# Example payload to create a quote
payload = {
    "pair": "BTC-GHS",       # trading instrument
    "side": "sell",           # "buy" or "sell"
    "amount_crypto": 0,  # amount of base currency
    "amount_fiat": 1000.00,    # amount of quote currency

}

response = requests.post(quotes_url, headers=headers, json=payload)

if response.status_code == 200 or response.status_code == 201:
    quote = response.json()
    print("Quote created successfully:")
    print(quote)
else:
    print(f"Error {response.status_code}: {response.text}")
