import json
import os

'''
This file implement the abstract method for the json database manger.
'''
class JsonManagerBase:
    def __init__(self, path="database.json"):
        self.DB_FILE = path

    #base method to load database
    def load_db(self):
        if not os.path.exists(self.DB_FILE):
            default_db = {
                "books": [],
                "users": [],
                "comments": [],
                "taboo_words": [],
                "financial_logs": []
            }
            self.save_db(default_db)
            return default_db

        with open(self.DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    #base method to save database
    def save_db(self, data):
        with open(self.DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    #base method to get all elements from table
    def get_all(self, table_name):
        db = self.load_db()
        return db.get(table_name, [])

    #base method to get a element correspond to a field name
    def get_by_field(self, table_name, field_name, value):
        items = self.get_all(table_name)
        for item in items:
            if item.get(field_name) == value:
                return item
        return None

    #base method to add a item to database
    def add_item(self, table_name, id_field, new_item):
        db = self.load_db()
        if self.get_by_field(table_name, id_field, new_item[id_field]):
            print(f"Error: {new_item[id_field]} already exists in {table_name}")
            return False
        db[table_name].append(new_item)
        self.save_db(db)
        return True

    #base method to update a item in database
    def update_item(self, table_name, id_field, target_id, update_fields):
        db = self.load_db()
        for item in db.get(table_name, []):
            if item.get(id_field) == target_id:
                item.update(update_fields)
                self.save_db(db)
                return True
        return False

    #base method to delete a item in database
    def delete_item(self, table_name, id_field, target_id):
        db = self.load_db()
        items = db.get(table_name, [])
        for item in items:
            if item.get(id_field) == target_id:
                items.remove(item)
                self.save_db(db)
                return True
        return False
