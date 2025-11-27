import pprint

import requests

from main import messages, COMMERCE_BASE_URL, VAULTA_API_KEY, BASE_URL, COMMERCE_API_KEY, client, tools


def follow_up_with_ai(messages, tool_json):
    """
    Sends the tool result back into the AI model to create a human-friendly response.
    """

    content = f"The tool has returned this JSON result: {tool_json}. Convert it into a helpful, human-friendly message."

    # Add the tool result to the conversation (this is important)
    messages.append({
        "role": "system",
        "content": f"The tool has returned this JSON result: {tool_json}."
                   f" Convert it into a helpful, human-friendly message."
    })

    response = send_to_ai(content)

    return response


def chat_append_message(role: str, content: str):
    messages.append({"role": role, "content": content})
    return messages


def get_product_details_by_description(query: str):
    product_url = f"{COMMERCE_BASE_URL}/products/{query}"
    headers = {
        "x-api-key": COMMERCE_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(product_url, headers=headers)
    if response.status_code == 200:
        product = response.json()
        print("Product retrieved successfully:")
        pprint(product)
        return follow_up_with_ai(messages, product)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_all_products():
    products_url = f"{COMMERCE_BASE_URL}/products"
    headers = {
        "x-api-key": COMMERCE_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(products_url, headers=headers)
    if response.status_code == 200:
        products = response.json()
        print("Products retrieved successfully:")
        pprint(products)

        return follow_up_with_ai(messages, products)

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def send_to_ai(incoming_message: str):
    all_messages = chat_append_message("user", incoming_message)

    print("Messages sent to AI:", incoming_message)
    pprint(f'these are all the messages{all_messages}')
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=all_messages,
        tools=tools,
        tool_choice="auto"
    )
    message = completion.choices[0].message

    return message


def get_rate():
    quotes_url = f"{BASE_URL}/get_quote"
    headers = {
        "x-api-key": VAULTA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "pair": "BTC-GHS",  # trading instrument
        "side": "sell",  # "buy" or "sell"
        "amount_crypto": 1,  # amount of base currency
        "amount_fiat": 1000.00,  # amount of quote currency

    }
    response = requests.post(quotes_url, headers=headers, json=payload)
    quote = response.json()
    print("Quote created successfully:")
    print(quote)
    return {quote}
