"""Inventory management system with static code analysis fixes."""

import json
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

stock_data = {}


def add_item(item: str, qty: int, logs: list = None):
    """Add a quantity of an item to stock data."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning(
            "Invalid types for item: %s or qty: %s. Skipping.",
            item,
            qty
        )
        return

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_msg = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_msg)


def remove_item(item: str, qty: int):
    """Remove a quantity of an item from stock data."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info(
                "Item '%s' stock reached zero and removed.",
                item
            )
    except KeyError:
        logging.warning(
            "Attempted to remove non-existent item: %s.",
            item
        )


def get_qty(item: str):
    """Get stock quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load stock data from a JSON file into global stock_data."""
    global stock_data  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
        logging.info("Data loaded successfully.")
    except FileNotFoundError:
        logging.warning(
            "File %s not found. Starting with empty stock.",
            file
        )
    except json.JSONDecodeError:
        logging.error(
            "Error decoding JSON from file. Content may be corrupted."
        )


def save_data(file="inventory.json"):
    """Save the current stock data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
        logging.info("Data saved successfully.")
    except OSError as e:
        logging.error("Failed to save data: %s", e)


def print_data():
    """Print a report of all items and their quantities."""
    print("Items Report")
    for item in stock_data:
        print(f"{item} -> {stock_data[item]}")


def check_low_items(threshold=5):
    """Return a list of items below the given threshold."""
    result = []
    for item in stock_data:
        if stock_data[item] < threshold:
            result.append(item)
    return result


def main():
    """Demonstrate inventory system functionality."""
    load_data()

    logs = []
    add_item("apple", 10, logs)
    add_item("banana", -2, logs)
    add_item(123, "ten")

    remove_item("apple", 3)
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    save_data()
    print_data()

    print("Security note: dangerous eval() removed!")


if __name__ == "__main__":
    main()
