from repository.branch_repository import BranchRepository
from repository.item_stock_repository import ItemStockRepository
from repository.user_repository import UserRepository
from werkzeug.exceptions import NotFound, BadRequest
from sqlalchemy.exc import SQLAlchemyError

def get_branch_by_id(db, branch_id):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
        raise BadRequest("Branch not found")
    return branch

def get_all_branches(db):
    branch_repository = BranchRepository(db)
    branches = branch_repository.list_all()
    return branches

def get_manager_by_branch_id(db, branch_id):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
    return branch.manager

def get_users_by_branch_id(db, branch_id):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
    return branch.users

def get_transactions_by_branch_id(db, branch_id):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
    return branch.transactions

def get_item_stocks_by_branch_id(db, branch_id):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
    return branch.item_stocks

def create_branch(db, new_branch):
    branch_repository = BranchRepository(db)
    return branch_repository.create(new_branch)

def delete_branch(db, branch_id):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
    branch_repository.delete(branch)

def update_branch(db, branch_id, updates):
    branch_repository = BranchRepository(db)
    branch = branch_repository.get_by_id(branch_id)
    if not branch:
        raise BadRequest("Branch not found")
    return branch_repository.update(branch, updates)

def assign_manager_to_branch(db, branch_id, manager_id):
    try:

        user_repository = UserRepository(db)
        manager = user_repository.get_by_id(manager_id)

        # make sure the user is a manager and can manage the branch
        if not manager:
            raise BadRequest("Manager not found")
        if manager.role != 'manager':
            raise BadRequest("User is not a manager")
        if any(branch.id == branch_id for branch in manager.managed_branches):
            raise BadRequest("Manager is already assigned to this branch")

        # make sure the branch exists and is not already managed by someone else
        branch_repository = BranchRepository(db)
        branch = branch_repository.get_by_id(branch_id)
        if not branch:
            raise BadRequest("Branch not found")
        if branch.manager:
            raise BadRequest("Branch already has a manager")

        # assign the manager to the branch
        branch.manager_id = manager_id
        branch.manager = manager

        # add the branch to the manager's managed branches
        manager.managed_branches.append(branch)
        db.commit()
        db.refresh(branch)
        return branch

    except (BadRequest):
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()
        raise e
    
def remove_manager_from_branch(db, branch_id):
    try:
        branch_repository = BranchRepository(db)
        branch = branch_repository.get_by_id(branch_id)
        if not branch:
            raise BadRequest("Branch not found")
        if not branch.manager:
            raise BadRequest("No manager found for this branch")
    
        manager = branch.manager
        if branch not in manager.managed_branches:
            raise BadRequest("Manager is not managing this branch")
        
        manager.managed_branches.remove(branch)

        branch.manager_id = None
        branch.manager = None
        db.commit()
        db.refresh(branch)
        return branch
    except (BadRequest):
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e

def get_all_item_stocks_for_branch(db, branch_id):
    item_stocks_repository = ItemStockRepository(db)
    item_stocks = item_stocks_repository.get_by_branch_id(branch_id)
    return item_stocks
