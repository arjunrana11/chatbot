from flask import Flask, request, jsonify
import google.generativeai as genai
import requests

app = Flask(__name__)

# Gemini API
genai.configure(api_key="AIzaSyAeVA8G5LTLalm_OcCVh17kPM-Fgx6FbkI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Shopify credentials
SHOP = "https://furniture-store18.myshopify.com/"
TOKEN = "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"


# Function to fetch products from Shopify
def get_products():

    url = f"https://{SHOP}/admin/api/2024-01/products.json"

    headers = {
        "X-Shopify-Access-Token": TOKEN
    }

    response = requests.get(url, headers=headers)

    return response.json()


@app.route("/")
def home():
    return "Gemini Chatbot API Running"


@app.route("/chat", methods=["GET","POST"])
def chat():

    if request.method == "GET":
        return "Send POST request with message"


    user_message = request.json["message"].lower()


    # If user asks for products
    if "product" in user_message or "show" in user_message:

        products = get_products()

        product_list = []

        for p in products["products"][:5]:
            title = p["title"]
            handle = p["handle"]

            link = f"https://{SHOP}/products/{handle}"

            product_list.append(f"{title} - {link}")

        return jsonify({
            "reply": "Here are some products:\n" + "\n".join(product_list)
        })


    # Otherwise use Gemini AI
    response = model.generate_content(
        f"""
You are an AI assistant for a Shopify store.
Help customers with products, orders, and store questions.

Customer question: {user_message}
"""
    )

    return jsonify({
        "reply": response.text
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)