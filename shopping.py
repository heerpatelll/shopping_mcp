from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("shopping")


## some of this setup is not needed, taken directly from tutorial, ok for now

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
    return {
        "message": f"Added '{added_item['name']}' (Travel size, Black) to cart.",
        "cart": [added_item],
        "image_path": "mascara.png"  # Path to the mascara image
    }


@mcp.tool()
async def get_delivery_option(shipping_address: dict) -> dict:
    """
    Takes a shipping address and returns a delivery option for 2025-09-05.
    Args:
        shipping_address (dict): Shipping address details.
    Returns:
        dict: Delivery option with delivery date.
    """
    return {
        "delivery_option": "Standard Shipping",
        "delivery_date": "2025-09-05",
        "shipping_address": shipping_address
    }


@mcp.tool()
async def process_payment(email: str, customer_name: str, card_info: dict) -> dict:
    """
    Processes payment with provided customer and card info.
    Args:
        email (str): Customer's email address.
        customer_name (str): Customer's full name.
        card_info (dict): Card information (mocked).
    Returns:
        dict: Payment status and summary.
    """
    # Mock payment processing
    return {
        "message": "Payment processed successfully!",
        "customer": {
            "name": customer_name,
            "email": email
        },
        "payment_status": "Processed",
        "card_info": {"last4": str(card_info.get("number", "0000"))[-4:]}
    }



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
