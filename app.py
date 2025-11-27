import requests
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
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
API_KEY = "SLItYCvd9M1gTtfY_5Aafo4kQN4njn_tC9vw8KOoCTI"

# Endpoint to create a quote
quotes_url = f"{BASE_URL}/get_quote"

headers = {
    "x-api-key": API_KEY,
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
