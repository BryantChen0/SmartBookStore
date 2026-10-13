from JsonManagerBase import JsonManagerBase

'''
This file implement the CRUD manager for book database.
'''
class BookManager(JsonManagerBase):
    def __init__(self, path="database.json"):
        super().__init__(path)
        self.TABLE_NAME = "books"
        self.ID_FIELD = "id"

    # Add new book into the database
    def add_book(self, book_id, title, author, category, price):
        new_book = {
            "id": book_id,
            "title": title,
            "author": author,
            "category": category,
            "price": float(price),
            "sales_count": 0,
            "views_count": 0,
            "no_order": False,
            "to_order": False
        }
        success = self.add_item(self.TABLE_NAME, self.ID_FIELD, new_book)
        if success:
            print(f"Book add successfully: {title}")
        else:
            print(f"Book {book_id} already exists")
        return success

    # Get all book in database
    def get_all_books(self):
        return self.get_all(self.TABLE_NAME)

    # Get book according to the book id
    def get_book_by_id(self, book_id):
        return self.get_by_field(self.TABLE_NAME, self.ID_FIELD, book_id)

    # Update book in database
    def update_book(self, book_id, title=None, author=None, category=None, price=None):
        update_fields = {}
        if title is not None:
            update_fields["title"] = title
        if author is not None:
            update_fields["author"] = author
        if category is not None:
            update_fields["category"] = category
        if price is not None:
            update_fields["price"] = float(price)

        if not update_fields:
            return True

        success = self.update_item(self.TABLE_NAME, self.ID_FIELD, book_id, update_fields)
        if success:
            print(f"Book {book_id} updated")
        else:
            print(f"Book {book_id} not found")
        return success

    # Update the views count of the book
    def update_book_views(self, book_id):
        book = self.get_book_by_id(book_id)
        if book:
            new_views = book.get("views_count", 0) + 1
            return self.update_item(self.TABLE_NAME, self.ID_FIELD, book_id, {"views_count": new_views})
        return False

    # Delete book from database
    def delete_book(self, book_id):
        success = self.delete_item(self.TABLE_NAME, self.ID_FIELD, book_id)
        if not success:
            print(f"Book {book_id} not found")
        return success