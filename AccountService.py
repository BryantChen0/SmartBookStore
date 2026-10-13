from DBManager import UserManager

'''
This file implement the logic of account service.
include follow:
1.deposit money into a user account 
2.super user reopen a suspended account
3.purchase money from a user account
4.decide if user can login to the account or not
'''
class AccountService:
    def __init__(self):
        self.manager = UserManager.UserManager()

    #check user status
    def check_login_status(self, username):
        user = self.manager.get_user(username)
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
        user = self.manager.get_user(username)
        if not user:
            return False

        new_balance = user["balance"] + float(amount)
        update_fields = {"balance": new_balance}

        return self.manager.update_user(username, update_fields)

    #this method only provide for SU to change user status
    def reopen_account_by_su(self, username, deposit_amount):
        user = self.manager.get_user(username)
        #only the superuser allow to use this method
        if not user["role"] == "SU":
            return False

        new_balance = user["balance"] + float(deposit_amount)
        if new_balance <= 0:
            print("Deposit amount must result in a positive balance to reopen account.")
            return False

        update_fields = {
            "balance": new_balance,
            "status": "active"
        }
        success = self.manager.update_item(username, update_fields)
        if success:
            print(f"Account '{username}' reopened successfully by SU.")
        return success

    # purchase method
    def process_purchase(self, username, raw_price):
        user = self.manager.get_user(username)
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

        return self.manager.update_user(username, update_fields)