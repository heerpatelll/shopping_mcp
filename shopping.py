from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import random

# Initialize FastMCP server
mcp = FastMCP("shopping")


## some of this setup is not needed, taken directly from tutorial, ok for now
## tutorial: https://modelcontextprotocol.io/quickstart/server


# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"



async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""



##### TOOLS ###########

@mcp.tool()
async def search_item(search_phrase: str) -> dict:
    """
    Mock tool that returns 5 hardcoded makeup products, each with travel and regular sizes,
    multiple color options, and fixed prices.
    """
    products = [
        {
            "id": 1,
            "name": "Lipstick",
            "category": "Makeup",
            "variants": [
                {
                    "size": "Travel",
                    "price": 8.99,
                    "colors": [
                        {"name": "Red", "hex": "#FF0000"},
                        {"name": "Coral", "hex": "#FF7F50"}
                    ]
                },
                {
                    "size": "Regular",
                    "price": 15.99,
                    "colors": [
                        {"name": "Red", "hex": "#FF0000"},
                        {"name": "Coral", "hex": "#FF7F50"},
                        {"name": "Nude", "hex": "#C2B280"}
                    ]
                }
            ]
        },
        {
            "id": 2,
            "name": "Mascara",
            "category": "Makeup",
            "variants": [
                {
                    "size": "Travel",
                    "price": 7.49,
                    "colors": [
                        {"name": "Black", "hex": "#000000"}
                    ]
                },
                {
                    "size": "Regular",
                    "price": 12.99,
                    "colors": [
                        {"name": "Black", "hex": "#000000"},
                        {"name": "Brown", "hex": "#654321"}
                    ]
                }
            ]
        },
        {
            "id": 3,
            "name": "Foundation SPF 15",
            "category": "Makeup",
            "variants": [
                {
                    "size": "Travel",
                    "price": 10.99,
                    "colors": [
                        {"name": "Light", "hex": "#FBE8EB"},
                        {"name": "Medium", "hex": "#E1B899"},
                        {"name": "Deep", "hex": "#8D5524"}
                    ]
                },
                {
                    "size": "Regular",
                    "price": 19.99,
                    "colors": [
                        {"name": "Light", "hex": "#FBE8EB"},
                        {"name": "Medium", "hex": "#E1B899"},
                        {"name": "Deep", "hex": "#8D5524"}
                    ]
                }
            ]
        },
        {
            "id": 4,
            "name": "Blush",
            "category": "Makeup",
            "variants": [
                {
                    "size": "Travel",
                    "price": 6.99,
                    "colors": [
                        {"name": "Rose", "hex": "#FF66CC"},
                        {"name": "Peach", "hex": "#FFDAB9"}
                    ]
                },
                {
                    "size": "Regular",
                    "price": 11.99,
                    "colors": [
                        {"name": "Rose", "hex": "#FF66CC"},
                        {"name": "Peach", "hex": "#FFDAB9"},
                        {"name": "Berry", "hex": "#8A0253"}
                    ]
                }
            ]
        },
        {
            "id": 5,
            "name": "Eyeliner Pencil",
            "category": "Makeup",
            "variants": [
                {
                    "size": "Travel",
                    "price": 5.99,
                    "colors": [
                        {"name": "Black", "hex": "#000000"},
                        {"name": "Brown", "hex": "#654321"}
                    ]
                },
                {
                    "size": "Regular",
                    "price": 9.99,
                    "colors": [
                        {"name": "Black", "hex": "#000000"},
                        {"name": "Brown", "hex": "#654321"},
                        {"name": "Blue", "hex": "#0000FF"}
                    ]
                }
            ]
        }
    ]
    return {"items": products}




@mcp.tool()
async def store_offers(cart: list) -> dict:
    """
    Searches for available store offers and automatically applies them.
    In this case, offers $1 off any travel size mascara.
    Args:
        cart (list): List of cart items.
    Returns:
        dict: Offer details and whether it was applied.
    """
    offer = {
        "description": "$1 off any travel size mascara",
        "applies": any(
            item.get("name", "").lower() == "black mascara" and item.get("variant", {}).get("size", "").lower() == "travel"
            for item in cart
        ),
        "discount": 1.00,
        "applied": False
    }
    # Automatically apply the offer if it applies
    if offer["applies"]:
        offer["applied"] = True
    return offer




@mcp.tool()
async def add_to_cart(item_phrase: str) -> dict:
    """
    Mock tool that adds an item to the cart based on the input phrase.
    Always adds Black Mascara (Travel size, Black color) to the cart.
    Args:
        item_phrase (str): The phrase describing the item to add.
    Returns:
        dict: Confirmation and details of the added item.
    """
    added_item = {
        "id": 2,
        "name": "Black Mascara",
        "category": "Makeup",
        "variant": {
            "size": "Travel",
            "price": 7.49,
            "color": {"name": "Black", "hex": "#000000"}
        },
        "quantity": 1
    }
    cart = [added_item]
    offer = await store_offers(cart)
    return {
        "message": f"Added '{added_item['name']}' (Travel size, Black) to cart.",
        "cart": cart,
        "offer": offer,
        "image_path": "mascara.png"  # Path to the mascara image
    }


@mcp.tool()
async def remove_from_cart(cart: list) -> dict:
    """
    Removes travel-size mascara items from the provided cart.
    Args:
        cart (list): The current cart (list of item dicts).
    Returns:
        dict: Updated cart and a list of removed items.
    """
    if not cart:
        return {"message": "Cart is empty.", "cart": [], "removed": []}

    removed = []
    updated_cart = []
    for item in cart:
        name = item.get("name", "").lower()
        size = item.get("variant", {}).get("size", "").lower()
        if "mascara" in name and size == "travel":
            removed.append(item)
        else:
            updated_cart.append(item)

    message = f"Removed {len(removed)} item(s) from cart." if removed else "No matching travel-size mascara found in cart."
    return {"message": message, "cart": updated_cart, "removed": removed}




@mcp.tool()
async def get_delivery_option(shipping_address: dict) -> dict:
    """
    Takes only a shipping address and returns available delivery options.
    This tool does not prompt for payment or card confirmation, and does not proceed to payment steps.
    The user must first confirm the shipping address and select a shipping option; only then should payment be handled separately.
    Args:
        shipping_address (dict): Shipping address details (optional).
    Returns:
        dict: Available delivery options and the provided shipping address.
    """
    return {
        "available_options": [
            {
                "delivery_option": "Standard Shipping",
                "delivery_date": "2025-09-05",
                "cost": 0.0
            },
            {
                "delivery_option": "2-Day Shipping",
                "delivery_date": "2025-08-25",
                "cost": 9.99
            }
        ],
        "shipping_address": shipping_address
    }


@mcp.tool()
async def confirm_card_on_file() -> dict:
    """
    Asks the user if they want to use the card on file ending in 1234 for payment.
    Returns:
        dict: Confirmation message and user response (mocked as True for demo).
    """
    # In a real system, prompt the user. Here, we assume user says yes.
    return {
        "message": "Would you like to use the card on file ending in 1234?",
        "card_last4": "1234",
        "confirmed": True
    }



@mcp.tool()
async def process_payment(email: str, customer_name: str, shipping_selection: dict) -> dict:
    """
    Processes payment with provided customer and card info.
    Args:
        email (str): Customer's email address.
        customer_name (str): Customer's full name.
        shipping_selection (dict): Selected shipping option.
    Returns:
        dict: Payment status, order confirmation number, and summary.
    """
    # For demo, assume cart is always a single travel size mascara
    cart = [{
        "id": 2,
        "name": "Black Mascara",
        "category": "Makeup",
        "variant": {
            "size": "Travel",
            "price": 7.49,
            "color": {"name": "Black", "hex": "#000000"}
        },
        "quantity": 1
    }]

    offer = await store_offers(cart)
    subtotal = cart[0]["variant"]["price"] * cart[0]["quantity"]
    discount = offer["discount"] if offer["applied"] else 0.0
    total = subtotal - discount

    # Generate a random order number (e.g., 8-digit number) to include in the response
    order_number = str(random.randint(10000000, 99999999))

    # Instead of a separate tool, just return a message asking for confirmation
    return {
        "message": "Would you like to use the card on file ending in 1234 for payment?",
        "order_number": order_number,
        "card_last4": "1234",
        "cart": cart,
        "offer": offer,
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "shipping_selection": shipping_selection,
        "customer": {
            "name": customer_name,
            "email": email
        },
        "payment_status": "Awaiting confirmation"
    }




if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
