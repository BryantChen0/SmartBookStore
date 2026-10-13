from JsonManagerBase import JsonManagerBase

'''
This file implement the CRUD manager for user database.
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

    #update a user in database base on the username
    def update_user(self, username, update_fields):
        return self.update_item(self.TABLE_NAME, self.ID_FIELD, username, update_fields)

    #get a user in database base on the username
    def get_user(self, username):
        return self.get_by_field(self.TABLE_NAME, self.ID_FIELD, username)

    #get all users in database
    def get_all_users(self):
        return self.get_all(self.TABLE_NAME)

    #delete a user in database
    def delete_user(self, username):
        return self.delete_item(self.TABLE_NAME, self.ID_FIELD, username)

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