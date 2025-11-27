import os
from pprint import pprint

import requests
from flask import Flask, request
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
app = Flask(__name__)

BASE_URL = "https://backend.vaulta.digital/api/v1"
COMMERCE_BASE_URL = os.getenv('COMMERCE_BASE_URL')
VAULTA_API_KEY = os.getenv("VAULTA_API_KEY")
COMMERCE_API_KEY = os.getenv("COMMERCE_API_KEY")

ai_persona = """ 
You are Presto Assistant — the digital owner and manager of an online shop.

Your personality:
- Friendly, confident, and professional.
- Helpful, patient, and polite.
- Clear, concise, and solution-focused.
- Warm and human, never robotic.

Your responsibilities:
- Assist customers with placing orders from start to finish.
- Collect all required information such as item, quantity, size/type, delivery method, and customer details.
- Provide product information, availability updates, and personalized recommendations.
- Create, process, and update order status (pending, confirmed, shipped, completed).
- Trigger payment requests when the customer is ready.
- Confirm payments after the customer provides proof or authorization.
- Help customers track their orders and share delivery updates.
- Receive complaints, apologize when needed, and resolve issues calmly and efficiently.
- Escalate technical or complex issues when necessary.
- Keep all communication simple, friendly, and customer-focused.

Your communication rules:
- Always speak as a helpful shop owner or store manager.
- Never sound robotic, overly formal, or corporate.
- Be proactive and ask for missing details instead of making assumptions.
- Use short, clear instructions when telling the customer what to do next.
- Stay polite and reassuring, even when the customer is upset.
- Thank customers for their patience when handling issues.
- Maintain a warm, trustworthy tone at all times.

Your capabilities (when tools are enabled):
- Take and process orders.
- Trigger payment requests.
- Confirm payments.
- Update order status.
- Create and track tickets for complaints or issues.

Tool Call Behavior:
- When a tool call is required, format ONLY the tool call in JSON.
- When the tool returns a JSON result, DO NOT show the JSON to the user.
- Instead, generate a warm, natural follow-up message explaining the result or next step.
- Keep the conversation flowing as a real shop owner would.


Your goal:
Make every customer feel supported, understood, and valued while ensuring smooth order placement, payment confirmation,
 order tracking, and issue resolution.
"""

messages = [{
    "role": "system",
    "content": ai_persona
}]


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


chat_append_message("system", content=ai_persona)


# When the customer wants to:
# - place an order → call create_order()
# - check out or pay → call process_payment()
# - check order status → call track_order()
# - file a complaint → call submit_complaint()
# - get product info → call fetch_product()
#
# Always confirm with the customer before triggering payment functions.
# Never guess — ask for missing details.
# Always respond in a polite, helpful tone.

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


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_all_products",
            "description": "Returns a list of all available shop products.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_rate",
    #         "description": "Gets the exchange rate for a given currency pair from Vaulta API.",
    #         "parameters": {
    #             "pair": {"type": "string"},
    #             "side": {"type": "string"},
    #             "amount_crypto": {"type": "number"},
    #             "amount_fiat": {"type": "number"}
    #
    #         },
    #         "required": ["pair", "side", "amount_crypto", "amount_fiat"]
    #
    #     }
    # },
    # {
    #
    #     "type": "function",
    #     "function": {
    #         "name": "get_product_details_by_description",
    #         "description": "Fetches details of a specific product by query.",
    #         "parameters": {
    #             "query": {"type": "string"}
    #         },
    #         "required": ["query"]
    #     }
    # }
]


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'GET':
        json_body = request.get_json(silent=True)
        query = (json_body.get('query') if json_body else None) or request.args.get('query')
        print("Request.method:", request.method)
        print("Query received:", query)
        response = send_to_ai(query)
        print("AI response (raw):", response)

        # try to extract tool calls from the response object/dict
        tool_calls = getattr(response, "tool_calls", None)
        try:
            if isinstance(response, dict):
                tool_calls = response.get("tool_calls")
            else:
                tool_calls = getattr(response, "tool_calls", None)
        except Exception as e:
            print("Error inspecting response for tool_calls:", e)

        print("Extracted tool_calls:", tool_calls)
        if tool_calls:
            pprint(tool_calls)
            tool_call = tool_calls[0]
            print("Processing tool_call:", tool_call)
            print(type(tool_call.function))
            print(tool_call.function.name)
            tool_name = tool_call.function.name
            args = tool_call.function.arguments

            print("AI triggered tool:", tool_name)
            print("Arguments:", args)

            # RUN THE APPROPRIATE TOOL
            if tool_name == "get_all_products":
                print("Calling get_all_products()")
                result = get_all_products()
                print("get_all_products() result:", result)
                return result
            elif tool_name == "get_product_details_by_description":
                result = get_product_details_by_description(args.get("query"))
                return result
            elif tool_name == "get_rate":
                result = get_rate(
                    args.get("pair"),
                    args.get("side"),
                    args.get("amount_crypto"),
                    args.get("amount_fiat")
                )
                return result

        else:
            # return normal text response
            return response.content
    return None


if __name__ == '__main__':
    app.run(debug=True, port=5001)
