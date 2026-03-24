shopping_table = """
    CREATE TABLE IF NOT EXISTS shopping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity TEXT NOT NULL,
        purchased INTEGER DEFAULT 0
    )
"""

# CRUD: Create - Read - Update - Delete
# INSERT SELECT UPDATE DELETE

insert_item = "INSERT INTO shopping (item, quantity) VALUES (?, ?)"

select_all = "SELECT id, item, quantity, purchased FROM shopping"

select_purchased = "SELECT id, item, quantity, purchased FROM shopping WHERE purchased = 1"
select_unpurchased = "SELECT id, item, quantity, purchased FROM shopping WHERE purchased = 0"

update_item = "UPDATE shopping SET purchased = ? WHERE id = ?"

delete_item = "DELETE FROM shopping WHERE id = ?"

count_purchased = "SELECT COUNT(*) FROM shopping WHERE purchased = 1"