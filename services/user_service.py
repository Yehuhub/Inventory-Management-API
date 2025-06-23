from repository.user_repository import UserRepository
from werkzeug.exceptions import NotFound

def get_user_by_id(db, user_id):
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    if not user:
        raise NotFound("User not found")
    return user

def get_all_users(db):
    user_repository = UserRepository(db)
    users = user_repository.list_all()
    if not users:
        raise NotFound("No users found")
    return users

def get_managed_branches(db, user_id):
    user_repository = UserRepository(db)
    managed_branches = user_repository.get_managed_branches_by_user_id(user_id)
    if not managed_branches:
        raise NotFound("No managed branches found")
    return managed_branches

def get_working_branch(db, user_id):
    user_repository = UserRepository(db)
    branch = user_repository.get_branch_by_user_id(user_id)
    if not branch:
        raise NotFound("No working branch found")
    
def get_transactions_by_user_id(db, user_id):
    user_repository = UserRepository(db)
    transactions = user_repository.get_transactions_by_user_id(user_id)
    if not transactions:
        raise NotFound(f"No transactions found for user. user_id:{user_id}.")
    
def create_user(db, new_user):
    repo = UserRepository(db)
    return repo.create(new_user)

def delete_user(db, user_id):
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    if not user:
        raise NotFound("User not found")
    user_repository.delete(user)

def update_user(db, user_id, updates):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise NotFound("User not found")
    return repo.update(user, updates)

def get_orders_by_user_id(db, user_id):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise NotFound("User not found")
    if not user.orders:
        raise NotFound("No orders found for this user")
    return user.orders
