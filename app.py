# from flask import Flask, request, jsonify
# import openai
# import os

# # Initialize Flask app
# app = Flask(__name__)

# from flask import Flask, request, jsonify, send_from_directory

# # Route for serving the frontend
# @app.route('/')
# def serve_frontend():
#     return send_from_directory('static', 'index.html')

# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # Set OpenAI API key (ensure this is your actual API key)
# openai.api_key = os.environ.get("OPENAI_API_KEY", "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")

# # Define a route for the chatbot
# import json
# @app.route('/chat', methods=['POST'])
# def chat():
#     # Get user input from the request
#     user_message = request.json.get("message")
    
#     # Validate user input
#     if not user_message:
#         return jsonify({"error": "Message field is required"}), 400
    
#     # Load FAQs from JSON file
#     with open("faqs.json", "r") as f:
#         faqs = json.load(f)

#     # Check if the user's message matches an FAQ
#     if user_message in faqs:
#         return jsonify({"reply": faqs[user_message]})

#     # If no match, call the OpenAI API for chat completion
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Replace with "gpt-4" if needed
#             #model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a helpful and concise customer service assistant. Keep your responses short and to the point."},
#                 {"role": "user", "content": user_message}
#             ]
#             #max_tokens=50  # Limit the response to ~50 tokens
#         )
#         # Extract the chatbot's reply
#         chatbot_reply = response['choices'][0]['message']['content']
        
#         # Post-process the reply to make it concise (optional)
#         # Limit the response to 2 sentences, keeping it short
#         concise_reply = ". ".join(chatbot_reply.split(". ")[:2]).strip()  # Trim to 2 sentences
        
#         return jsonify({"reply": concise_reply})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)



# import re
# import requests
# import openai
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# #from flask import Flask, request, jsonify, send_from_directory

# # # Route for serving the frontend
# from flask import Flask, request, jsonify, send_from_directory

# # Serve the frontend (index.html)
# @app.route('/')
# def serve_frontend():
#     return send_from_directory('static', 'index.html')

# # Serve static files (e.g., CSS, JS)
# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # OpenAI API key (replace with your actual key)
# openai.api_key = "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"

# # Base URL of the product API
# PRODUCT_API_BASE_URL = "https://uat.api.foodstories.shop/rest/V1/products"

# # Map product names to SKUs (as an example; could also be dynamic)
# product_sku_mapping = {
#     "Premium French Cheese": "2502",
#     "Dark Belgian Chocolate": "3504",
#     "Organic Avocado": "4506",
# }

# @app.route('/chat', methods=['POST'])
# def chat():
#     # Get user input from the request
#     user_message = request.json.get("message")
    
#     # Validate user input
#     if not user_message:
#         return jsonify({"error": "Message field is required"}), 400

#     # Step 1: Detect product queries
#     product_match = re.search(r"(Premium French Cheese|Dark Belgian Chocolate|Organic Avocado)", user_message, re.IGNORECASE)
#     if product_match:
#         product_name = product_match.group(0)  # Extract the product name
#         sku = product_sku_mapping.get(product_name)  # Get the corresponding SKU

#         if not sku:
#             # No SKU found, fallback to OpenAI
#             return fallback_to_openai(user_message)

#         # Build the API URL dynamically
#         api_url = (
#             f"{PRODUCT_API_BASE_URL}?"
#             f"searchCriteria[filterGroups][0][filters][0][field]=sku&"
#             f"searchCriteria[filterGroups][0][filters][0][condition_type]=eq&"
#             f"searchCriteria[filterGroups][0][filters][0][value]={sku}&"
#             f"searchCriteria[filterGroups][0][filters][1][field]=status&"
#             f"searchCriteria[filterGroups][0][filters][1][value]=1&"
#             f"searchCriteria[filterGroups][0][filters][1][condition_type]=eq"
#         )

#         # Call the product API
#         try:
#             response = requests.get(api_url)
#             response.raise_for_status()  # Raise an error for bad HTTP responses
#             product_data = response.json()  # Parse the response JSON

#             # Extract product details (customize based on API structure)
#             if "items" in product_data and len(product_data["items"]) > 0:
#                 product = product_data["items"][0]  # Assume the first item is the correct one
#                 reply = (
#                     f"{product['name']} costs {product['price']} {product['currency_code']}. "
#                     f"It is currently {product['availability']}."
#                 )
#                 return jsonify({"reply": reply})
#             else:
#                 # No product found in the API, fallback to OpenAI
#                 return fallback_to_openai(user_message)

#         except requests.exceptions.RequestException:
#             # API error, fallback to OpenAI
#             return fallback_to_openai(user_message)

#     # Step 2: Fallback to OpenAI for non-product queries or edge cases
#     return fallback_to_openai(user_message)


# def fallback_to_openai(user_message):
#     """
#     Fallback to OpenAI for generating a response when API data is unavailable.
#     """
#     try:
#         # Call OpenAI's ChatCompletion API
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant for a premium food brand. Provide concise and accurate information about premium food products like fruits, vegetables, cheese, bakery, and chocolates."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
    
#      #Extract the chatbot's reply
#         chatbot_reply = response['choices'][0]['message']['content']
        
#         # Post-process the reply to make it concise (optional)
#         # Limit the response to 2 sentences, keeping it short
#         concise_reply = ". ".join(chatbot_reply.split(". ")[:3]).strip()  # Trim to 3 sentences
        
#         return jsonify({"reply": concise_reply})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)







# import re
# import requests
# import openai
# from flask import Flask, request, jsonify, send_from_directory

# app = Flask(__name__)

# # Serve the frontend (index.html)
# @app.route('/')
# def serve_frontend():
#     return send_from_directory('static', 'index.html')

# # Serve static files (e.g., CSS, JS)
# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # OpenAI API key (replace with your actual key)
# openai.api_key = "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"

# # API Authentication Token
# API_AUTH_TOKEN = "12emkijw2m5u4l2gnsmdvohlzit9go3x"  # Replace with your actual API token

# # Base URL of the product API
# PRODUCT_API_BASE_URL = "https://uat.api.foodstories.shop/rest/V1/products"

# @app.route('/chat', methods=['POST'])
# def chat():
#     # Get user input from the request
#     user_message = request.json.get("message")
    
#     if not user_message:
#         return jsonify({"error": "Message field is required"}), 400

#     # Step 1: Detect product-related queries
#     product_keywords = detect_product_keywords(user_message)

#     if product_keywords:
#         # Build the dynamic API URL for product search
#         api_url = (
#             f"{PRODUCT_API_BASE_URL}?"
#             f"searchCriteria[filterGroups][0][filters][0][field]=name&"
#             f"searchCriteria[filterGroups][0][filters][0][condition_type]=like&"
#             f"searchCriteria[filterGroups][0][filters][0][value]={product_keywords}"
#         )

#         # Step 2: Query the API with authentication
#         try:
#             headers = {
#                 "Authorization": f"Bearer {API_AUTH_TOKEN}"  # Add the Bearer token
#             }
#             response = requests.get(api_url, headers=headers, timeout=10)  # Pass the headers
#             response.raise_for_status()
#             product_data = response.json()

#             # Debugging
#             print(f"API URL: {api_url}")
#             print(f"API Response: {product_data}")

#             # Parse the API response
#             if "items" in product_data and len(product_data["items"]) > 0:
#                 product = product_data["items"][0]  # First matching product
                
#                 # Extract relevant fields
#                 product_name = product.get("name", "Unknown Product")
#                 product_price = product.get("price", "Unavailable")
#                 product_status = "In Stock" if product.get("status") == 1 else "Out of Stock"
                
#                 # Extract description from custom attributes
#                 product_description = next(
#                     (attr["value"] for attr in product.get("custom_attributes", []) if attr["attribute_code"] == "description"), 
#                     "No description available."
#                 )

#                 # Format the response
#                 reply = (
#                     f"{product_name} costs ₹{product_price}. "
#                     f"It is currently {product_status}. "
#                     f"Description: {product_description}"
#                 )
#                 return jsonify({"reply": reply})
#             else:
#                 # No matching product found
#                 return fallback_to_openai(user_message)

#         except requests.exceptions.RequestException as e:
#             print(f"API Error: {e}")  # Log the error
#             return jsonify({"reply": "Sorry, I'm having trouble fetching product details right now. Please try again later."})

#     # Step 3: Fallback to OpenAI for non-product queries or edge cases
#     return fallback_to_openai(user_message)


# def detect_product_keywords(user_message):
#     """
#     Detect product-related keywords from the user's query.
#     """
#     # Example product names (extend this list as needed)
#     product_names = ["Premium French Cheese", "Dark Belgian Chocolate", "Organic Avocado", "Pink Peppercorns"]

#     # Check if any product name is mentioned in the user's query
#     for product_name in product_names:
#         if product_name.lower() in user_message.lower():
#             return product_name
#     return None


# def fallback_to_openai(user_message):
#     """
#     Fallback to OpenAI for generating a response when API data is unavailable.
#     """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant for a premium food brand. Provide concise and accurate information about premium food products like fruits, vegetables, cheese, bakery, and chocolates."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#         chatbot_reply = response['choices'][0]['message']['content']
#         return jsonify({"reply": chatbot_reply})
#     except Exception as e:
#         print(f"OpenAI Error: {e}")
#         return jsonify({"reply": "Sorry, I'm unable to assist with your query right now. Please try again later."})


# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)








# import requests
# import openai
# from flask import Flask, request, jsonify, send_from_directory

# app = Flask(__name__)

# # Serve the frontend (index.html)
# @app.route('/')
# def serve_frontend():
#     return send_from_directory('static', 'index.html')

# # Serve static files (e.g., CSS, JS)
# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # OpenAI API key (replace with your actual key)
# openai.api_key = "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"

# # API Authentication Token
# API_AUTH_TOKEN = "12emkijw2m5u4l2gnsmdvohlzit9go3x"  # Replace with your actual API token

# # Base URL of the product API
# PRODUCT_API_BASE_URL = "https://uat.api.foodstories.shop/rest/V1/products"

# # Cache for storing all product names and SKUs
# product_cache = {}

# def fetch_all_products():
#     """
#     Fetch a list of all products from the API and update the cache.
#     """
#     try:
#         api_url = f"{PRODUCT_API_BASE_URL}?searchCriteria"
#         headers = {"Authorization": f"Bearer {API_AUTH_TOKEN}"}
#         response = requests.get(api_url, headers=headers, timeout=15)
#         response.raise_for_status()
#         product_data = response.json()

#         if "items" in product_data:
#             for product in product_data["items"]:
#                 product_name = product.get("name", "").lower()
#                 sku = product.get("sku", "")
#                 if product_name and sku:
#                     product_cache[product_name] = sku

#         print(f"Product cache updated: {product_cache}")

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching all products: {e}")

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get("message")
#     if not user_message:
#         return jsonify({"error": "Message field is required"}), 400

#     product_keywords = detect_product_keywords(user_message)
#     if product_keywords:
#         sku = product_cache.get(product_keywords)
#         if sku:
#             api_url = (
#                 f"{PRODUCT_API_BASE_URL}?"
#                 f"searchCriteria[filterGroups][0][filters][0][field]=sku&"
#                 f"searchCriteria[filterGroups][0][filters][0][condition_type]=eq&"
#                 f"searchCriteria[filterGroups][0][filters][0][value]={sku}"
#             )
#             try:
#                 headers = {"Authorization": f"Bearer {API_AUTH_TOKEN}"}
#                 response = requests.get(api_url, headers=headers, timeout=15)
#                 response.raise_for_status()
#                 product_data = response.json()

#                 if "items" in product_data and len(product_data["items"]) > 0:
#                     product = product_data["items"][0]
#                     product_name = product.get("name", "Unknown Product")
#                     product_price = product.get("price", "Unavailable")
#                     product_status = "In Stock" if product.get("status") == 1 else "Out of Stock"
                    
#                     product_description = next(
#                         (attr["value"] for attr in product.get("custom_attributes", []) if attr["attribute_code"] == "short_description"), 
#                         "No description available."
#                     )

#                     reply = (
#                         f"{product_name} costs ₹{product_price}. "
#                         f"It is currently {product_status}. "
#                         f"Description: {product_description}"
#                     )
#                     return jsonify({"reply": reply})

#             except requests.exceptions.RequestException as e:
#                 print(f"API Error: {e}")
#                 return jsonify({"reply": "Sorry, I'm having trouble fetching product details right now. Please try again later."})

#     return fallback_to_openai(user_message)

# def detect_product_keywords(user_message):
#     user_message = user_message.lower()
#     for product_name in product_cache.keys():
#         if product_name in user_message:
#             return product_name
#     return None

# def fallback_to_openai(user_message):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant for a premium food brand. Provide concise and accurate information about premium food products."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#         chatbot_reply = response['choices'][0]['message']['content']
#         return jsonify({"reply": chatbot_reply})
#     except Exception as e:
#         print(f"OpenAI Error: {e}")
#         return jsonify({"reply": "Sorry, I'm unable to assist with your query right now. Please try again later."})


# if __name__ == "__main__":
#     fetch_all_products()  # Fetch all products and update the cache
#     app.run(debug=True)





# import requests
# import openai
# from flask import Flask, request, jsonify, send_from_directory

# app = Flask(__name__)

# # Serve the frontend (index.html)
# @app.route('/')
# def serve_frontend():
#     return send_from_directory('static', 'index.html')

# # Serve static files (e.g., CSS, JS)
# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # OpenAI API key (replace with your actual key)
# openai.api_key = "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"

# # API Authentication Token
# API_AUTH_TOKEN = "12emkijw2m5u4l2gnsmdvohlzit9go3x"  # Replace with your actual API token

# # Base URL of the product API
# PRODUCT_API_BASE_URL = "https://uat.api.foodstories.shop/rest/V1/products"

# # Cache for storing all product names and SKUs
# product_cache = {}

# def fetch_all_products():
#     """
#     Fetch a list of all products from the API and update the cache.
#     """
#     try:
#         api_url = f"{PRODUCT_API_BASE_URL}?searchCriteria"
#         headers = {"Authorization": f"Bearer {API_AUTH_TOKEN}"}
#         response = requests.get(api_url, headers=headers, timeout=15)
#         response.raise_for_status()
#         product_data = response.json()

#         if "items" in product_data:
#             for product in product_data["items"]:
#                 product_name = product.get("name", "").lower()
#                 sku = product.get("sku", "")
#                 if product_name and sku:
#                     product_cache[product_name] = sku

#         print(f"Product cache updated: {product_cache}")

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching all products: {e}")

# def detect_user_intent(user_message):
#     """
#     Detect the user's intent based on the query.
#     """
#     user_message = user_message.lower()

#     # Check for price-related keywords
#     if any(keyword in user_message for keyword in ["price", "cost", "how much"]):
#         return "price"
    
#     # Check for stock/availability-related keywords
#     if any(keyword in user_message for keyword in ["in stock", "availability", "is it available", "available"]):
#         return "stock"
    
#     # Check for description-related keywords
#     if any(keyword in user_message for keyword in ["description", "tell me about", "details"]):
#         return "description"
    
#     # Default to general query (provide all details)
#     return "general"

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get("message")
#     if not user_message:
#         return jsonify({"error": "Message field is required"}), 400

#     product_keywords = detect_product_keywords(user_message)
#     if product_keywords:
#         sku = product_cache.get(product_keywords)
#         if sku:
#             api_url = (
#                 f"{PRODUCT_API_BASE_URL}?"
#                 f"searchCriteria[filterGroups][0][filters][0][field]=sku&"
#                 f"searchCriteria[filterGroups][0][filters][0][condition_type]=eq&"
#                 f"searchCriteria[filterGroups][0][filters][0][value]={sku}"
#             )
#             try:
#                 headers = {"Authorization": f"Bearer {API_AUTH_TOKEN}"}
#                 response = requests.get(api_url, headers=headers, timeout=10)
#                 response.raise_for_status()
#                 product_data = response.json()

#                 if "items" in product_data and len(product_data["items"]) > 0:
#                     product = product_data["items"][0]
#                     product_name = product.get("name", "Unknown Product")
#                     product_price = product.get("price", "Unavailable")
#                     product_status = "In Stock" if product.get("status") == 1 else "Out of Stock"
                    
#                     product_description = next(
#                         (attr["value"] for attr in product.get("custom_attributes", []) if attr["attribute_code"] == "description"), 
#                         "No description available."
#                     )

#                     # Detect the user's intent
#                     intent = detect_user_intent(user_message)

#                     # Build the response based on intent
#                     if intent == "price":
#                         reply = f"The price of {product_name} is ₹{product_price}."
#                     elif intent == "stock":
#                         reply = f"{product_name} is currently {product_status}."
#                     elif intent == "description":
#                         reply = f"{product_name}: {product_description}"
#                     else:  # General query
#                         reply = (
#                             f"{product_name} costs ₹{product_price}. "
#                             f"It is currently {product_status}. "
#                             f"Description: {product_description}"
#                         )

#                     return jsonify({"reply": reply})

#             except requests.exceptions.RequestException as e:
#                 print(f"API Error: {e}")
#                 return jsonify({"reply": "Sorry, I'm having trouble fetching product details right now. Please try again later."})

#     return fallback_to_openai(user_message)

# def detect_product_keywords(user_message):
#     user_message = user_message.lower()
#     for product_name in product_cache.keys():
#         if product_name in user_message:
#             return product_name
#     return None

# def fallback_to_openai(user_message):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant for a premium food brand. Provide concise and accurate information about premium food products."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#         chatbot_reply = response['choices'][0]['message']['content']
#         return jsonify({"reply": chatbot_reply})
#     except Exception as e:
#         print(f"OpenAI Error: {e}")
#         return jsonify({"reply": "Sorry, I'm unable to assist with your query right now. Please try again later."})

# if __name__ == "__main__":
#     fetch_all_products()  # Fetch all products and update the cache
#     app.run(debug=True)






import re
import requests
import openai
from flask import Flask, request, jsonify, send_from_directory
from rapidfuzz import fuzz, process  # Import fuzzy matching functions

app = Flask(__name__)

# Serve the frontend (index.html)
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

# Serve static files (e.g., CSS, JS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# OpenAI API key (replace with your actual key)
openai.api_key = "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"

# API Authentication Token
API_AUTH_TOKEN = "12emkijw2m5u4l2gnsmdvohlzit9go3x"  # Replace with your actual API token

# Base URL of the product API
PRODUCT_API_BASE_URL = "https://uat.api.foodstories.shop/rest/V1/products"

# Cache for storing all product names and SKUs
product_cache = {}

def fetch_all_products():
    """
    Fetch a list of all products from the API and update the cache.
    """
    try:
        api_url = f"{PRODUCT_API_BASE_URL}?searchCriteria"
        headers = {"Authorization": f"Bearer {API_AUTH_TOKEN}"}
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        product_data = response.json()

        if "items" in product_data:
            for product in product_data["items"]:
                product_name = product.get("name", "").lower()
                sku = product.get("sku", "")
                if product_name and sku:
                    product_cache[product_name] = sku

        print(f"Product cache updated: {product_cache}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching all products: {e}")

def detect_product_keywords(user_message):
    """
    Detect the closest matching product name based on the user's query using fuzzy matching.
    """
    user_message = user_message.lower()

    # Check if the product cache is empty
    if not product_cache:
        print("Product cache is empty. Unable to perform product detection.")
        return None

    # Use fuzzy matching to find the best matching product name
    matches = process.extract(user_message, product_cache.keys(), scorer=fuzz.ratio)

    # Debug: Log fuzzy matches
    print(f"Fuzzy matches for '{user_message}': {matches}")

    if matches:
        best_match, score, _ = matches[0]  # Unpack the first two values and ignore the index
        # Return the best match if the score is above the threshold
        if score >= 40:  # Adjust the threshold as needed
            print(f"Fuzzy Match Found: {best_match} (Score: {score})")
            return best_match

    # Fallback: Use substring matching from the working code
    for product_name in product_cache.keys():
        if product_name in user_message:
            print(f"Substring Match Found: {product_name}")
            return product_name

    # No match found
    print("No match found for user query.")
    return None

def detect_user_intent(user_message):
    """
    Detect the user's intent based on the query.
    """
    user_message = user_message.lower()

    # Check for price-related keywords
    if any(keyword in user_message for keyword in ["price", "cost", "how much"]):
        return "price"
    
    # Check for stock/availability-related keywords
    if any(keyword in user_message for keyword in ["in stock", "availability", "is it available", "quantity"]):
        return "stock"
    
    # Check for description-related keywords
    if any(keyword in user_message for keyword in ["description", "tell me about", "details"]):
        return "description"
    
    # Default to general query (provide all details)
    return "general"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message field is required"}), 400

    product_keywords = detect_product_keywords(user_message)
    if product_keywords:
        sku = product_cache.get(product_keywords)
        if sku:
            api_url = (
                f"{PRODUCT_API_BASE_URL}?"
                f"searchCriteria[filterGroups][0][filters][0][field]=sku&"
                f"searchCriteria[filterGroups][0][filters][0][condition_type]=eq&"
                f"searchCriteria[filterGroups][0][filters][0][value]={sku}"
            )
            try:
                headers = {"Authorization": f"Bearer {API_AUTH_TOKEN}"}
                response = requests.get(api_url, headers=headers, timeout=15)
                response.raise_for_status()
                product_data = response.json()

                if "items" in product_data and len(product_data["items"]) > 0:
                    product = product_data["items"][0]
                    product_name = product.get("name", "Unknown Product")
                    product_price = product.get("price", "Unavailable")
                    product_status = "In Stock" if product.get("status") == 1 else "Out of Stock"
                    
                    product_description = next(
                        (attr["value"] for attr in product.get("custom_attributes", []) if attr["attribute_code"] == "description"), 
                        "No description available."
                    )

                    # Detect the user's intent
                    intent = detect_user_intent(user_message)

                    # Build the response based on intent
                    if intent == "price":
                        reply = f"The price of {product_name} is ₹{product_price}."
                    elif intent == "stock":
                        reply = f"{product_name} is currently {product_status}."
                    elif intent == "description":
                        reply = f"{product_name}: {product_description}"
                    else:  # General query
                        reply = (
                            f"{product_name} costs ₹{product_price}. "
                            f"It is currently {product_status}. "
                            f"About {product_name},  {product_description}"
                        )

                    return jsonify({"reply": reply})

            except requests.exceptions.RequestException as e:
                print(f"API Error: {e}")
                return jsonify({"reply": "Sorry, I'm having trouble fetching product details right now. Please try again later."})

    return fallback_to_openai(user_message)

def fallback_to_openai(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a premium food brand. Provide concise and accurate information about premium food products."},
                {"role": "user", "content": user_message}
            ]
        )
        chatbot_reply = response['choices'][0]['message']['content']
        return jsonify({"reply": chatbot_reply})
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return jsonify({"reply": "Sorry, I'm unable to assist with your query right now. Please try again later."})

if __name__ == "__main__":
    fetch_all_products()  # Fetch all products and update the cache
    app.run(debug=True)