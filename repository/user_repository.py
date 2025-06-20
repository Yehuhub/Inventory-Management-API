from repository.base_repository import BaseRepository
from models import User
from sqlalchemy import select

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, User)

    #gets the branch associated to the user
    def get_branch_by_user_id(self, user_id):
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt).scalars().first()
        return result.branch if result else None
    
    #gets the branches managed by the user
    def get_managed_branches_by_user_id(self, user_id):
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt).scalars().first()
        return result.managed_branches if result else None
    
    #gets the transactions made by the user
    def get_transactions_by_user_id(self, user_id):
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt).scalars().first()
        return result.transactions if result else None
