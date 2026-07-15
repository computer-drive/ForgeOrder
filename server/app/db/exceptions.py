
class MetaDatabaseException(Exception):
    pass

class CategoryNotFoundError(Exception):
    def __init__(self, category_id: int):
        super().__init__(f"Category with ID {category_id} not found")
        self.category_id = category_id