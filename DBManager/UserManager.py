from DBManagerBase import JsonManagerBase

'''
This file implement the manager for user database.
'''
class UserManager(JsonManagerBase):
    def __init__(self, path="database.json"):
        super().__init__(path)
        self.TABLE_NAME = "users"
        self.ID_FIELD = "username"

    # new user register
    def register_user(self, username, role="RC", initial_balance=0.0):
        new_user = {
            "username": username,
            "role": role,
            "balance": float(initial_balance),
            "warnings": 0,
            "purchase_count": 0,
            "total_spent": 0.0,
            "status": "active"
        }
        success = self.add_item(self.TABLE_NAME, self.ID_FIELD, new_user)
        if success:
            print(f"User '{username}' registered successfully.")
        else:
            print(f"Error: Username '{username}' already exists.")
        return success

    #get a user in database base on the username
    def get_user(self, username):
        return self.get_by_field(self.TABLE_NAME, self.ID_FIELD, username)

    #get all users in database
    def get_all_users(self):
        return self.get_all(self.TABLE_NAME)

    #check user status
    def check_login_status(self, username):
        user = self.get_user(username)
        if not user:
            print(f"User '{username}' not found.")
            return False, "user_not_found"

        #if user status is suspended, can't login anymore
        if user.get("status") == "suspended":
            print(f"User '{username}' is suspended and cannot log in.")
            return False, "suspended"

        return True, "ok"

    #deposit into account
    def deposit(self, username, amount):
        user = self.get_user(username)
        if not user:
            return False

        new_balance = user["balance"] + float(amount)
        update_fields = {"balance": new_balance}

        return self.update_item(self.TABLE_NAME, self.ID_FIELD, username, update_fields)

    #this method only provide for SU to change user status
    def reopen_account_by_su(self, username, deposit_amount):
        user = self.get_user(username)
        if not user:
            return False

        new_balance = user["balance"] + float(deposit_amount)
        if new_balance <= 0:
            print("Deposit amount must result in a positive balance to reopen account.")
            return False

        update_fields = {
            "balance": new_balance,
            "status": "active"
        }
        success = self.update_item(self.TABLE_NAME, self.ID_FIELD, username, update_fields)
        if success:
            print(f"Account '{username}' reopened successfully by SU.")
        return success

    # purchase methhod
    def process_purchase(self, username, raw_price):
        user = self.get_user(username)
        if not user or user["status"] == "suspended":
            return False

        role = user["role"]

        # 1. VC ($10% discount)
        if role == "VC":
            actual_cost = raw_price * 0.9
        else:
            actual_cost = raw_price

        new_balance = user["balance"] - actual_cost
        new_purchase_count = user.get("purchase_count", 0) + 1
        new_total_spent = user.get("total_spent", 0.0) + actual_cost

        update_fields = {
            "purchase_count": new_purchase_count,
            "total_spent": new_total_spent
        }

        # 2. check the user balance, if negative, have $1 fine and move the status to suspended
        if new_balance < 0:
            new_balance -= 1.0
            update_fields["status"] = "suspended"
            print(f"Overdraft! $1 fine applied. Account '{username}' suspended.")

        update_fields["balance"] = new_balance

        # 3. if purchase more than 3 times and total spend more than $200, upgrade RC to VC
        if role == "RC" and (new_purchase_count > 3 or new_total_spent > 200.0):
            update_fields["role"] = "VC"
            print(f"User '{username}' promoted to VIP Customer (VC)!")

        return self.update_item(self.TABLE_NAME, self.ID_FIELD, username, update_fields)

    # warning
    def add_warning(self, username):
        user = self.get_user(username)
        if not user:
            return False

        current_warnings = user.get("warnings", 0) + 1
        update_fields = {"warnings": current_warnings}
        role = user["role"]

        # punishment logic
        if role == "VC":
            # if VC, downgrade to RC
            update_fields["role"] = "RC"
            print(f"VC User '{username}' received warning {current_warnings} and was demoted to RC.")
        elif role == "RC":
            # if RC, after 2 warning, move status to suspended
            if current_warnings > 2:
                update_fields["status"] = "suspended"
                print(f"RC User '{username}' reached >2 warnings and was suspended.")
            else:
                print(f"RC User '{username}' received warning {current_warnings}.")

        return self.update_item(self.TABLE_NAME, self.ID_FIELD, username, update_fields)