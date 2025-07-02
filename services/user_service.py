from repository.user_repository import UserRepository
from werkzeug.exceptions import BadRequest

def get_user_by_id(db, user_id):
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    if not user:
        raise BadRequest("User not found")
    return user

def get_all_users(db):
    user_repository = UserRepository(db)
    users = user_repository.list_all()
    return users

def get_managed_branches(db, user_id):
    user_repository = UserRepository(db)
    managed_branches = user_repository.get_managed_branches_by_user_id(user_id)
    return managed_branches

def get_working_branch(db, user_id):
    user_repository = UserRepository(db)
    branch = user_repository.get_branch_by_user_id(user_id)
    if not branch:
        raise BadRequest("No working branch found")
    
def get_transactions_by_user_id(db, user_id):
    user_repository = UserRepository(db)
    transactions = user_repository.get_transactions_by_user_id(user_id)
    return transactions
    
def create_user(db, new_user):
    repo = UserRepository(db)
    return repo.create(new_user)

def delete_user(db, user_id):
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    if not user:
        raise BadRequest("User not found")
    user_repository.delete(user)

def update_user(db, user_id, updates):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise BadRequest("User not found")
    return repo.update(user, updates)

def get_orders_by_user_id(db, user_id):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise BadRequest("User not found")
    return user.orders
