from repository.price_repository import PriceRepository
from werkzeug.exceptions import InternalServerError, BadRequest

def get_price_by_id(db, price_id: int):
    price_repository = PriceRepository(db)
    price = price_repository.get_by_id(price_id)
    if not price:
        raise BadRequest("Price not found")
    return price

def list_prices(db):
    price_repository = PriceRepository(db)
    return price_repository.list_all()

def create_price(db, price_data: dict):
    price_repository = PriceRepository(db)
    price = price_repository.model(**price_data)
    return price_repository.create(price)

def update_price(db, price_id: int, updates: dict):
    price_repository = PriceRepository(db)
    price = price_repository.get_by_id(price_id)
    if not price:
        raise BadRequest("Price not found")
    return price_repository.update(price, updates)

def delete_price(db, price_id: int):
    price_repository = PriceRepository(db)
    price = price_repository.get_by_id(price_id)
    if not price:
        raise BadRequest("Price not found")
    try:
        price_repository.delete(price)
        return price
    except Exception:
        raise InternalServerError("Error deleting price")

def get_prices_by_item_id(db, item_id: int):
    price_repository = PriceRepository(db)
    prices = price_repository.get_prices_by_item_id(item_id)
    return prices

def get_best_price_for_quantity(db, item_id: int, quantity: int):
    price_repository = PriceRepository(db)
    price = price_repository.get_best_price_for_quantity(item_id, quantity)
    if not price:
        raise BadRequest(
            f"No suitable price found for item_id={item_id} and quantity={quantity}"
        )
    return price
