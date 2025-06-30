from repository.base_repository import BaseRepository
from models import Client
from sqlalchemy import select, func


class ClientRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Client)

    # Gets all orders of a client
    def get_orders_by_client_id(self, client_id):
        stmt = select(Client).where(Client.id == client_id)
        result = self.db.execute(stmt).scalars().first()
        return result.orders if result else None

    # Finds client by full name (first and last)
    def find_by_full_name(self, first_name: str, last_name: str):
        stmt = select(Client).where(
            func.lower(Client.first_name) == first_name.lower(),
            func.lower(Client.last_name) == last_name.lower()
        )
        return self.db.execute(stmt).scalars().first()

    # Finds clients by phone number (exact match)
    def find_by_phone(self, phone: str):
        stmt = select(Client).where(Client.phone_number == phone.strip())
        return self.db.execute(stmt).scalars().first()