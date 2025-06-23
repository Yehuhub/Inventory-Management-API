from repository.base_repository import BaseRepository
from models import Branch
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class BranchRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Branch)

    #gets the branch manager given the branch id
    def get_manager_by_branch_id(self, branch_id):
        stmt = select(Branch).where(Branch.id == branch_id)
        branch = self.db.execute(stmt).scalars().first()
        return branch.manager if branch else None
    
    #eagrly gets all users working at the branch
    def get_users_by_branch_id(self, branch_id):
        stmt = select(Branch).where(Branch.id == branch_id).options(selectinload(Branch.users))
        branch = self.db.execute(stmt).scalars().first()
        return branch.users if branch else None
    
    #eagrly get all transactions for the branch
    def get_transactions_by_branch_id(self, branch_id):
        stmt = select(Branch).where(Branch.id == branch_id).options(selectinload(Branch.transactions))
        branch = self.db.execute(stmt).scalars().first()
        return branch.transactions if branch else None
    