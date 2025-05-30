from .schemas import Item

# In-memory "database"
fake_items_db: list[Item] = []
_item_id_counter: int = 0


def get_next_item_id() -> int:
    global _item_id_counter
    _item_id_counter += 1
    return _item_id_counter


def reset_db_state():  # For tests
    global _item_id_counter
    fake_items_db.clear()
    _item_id_counter = 0
