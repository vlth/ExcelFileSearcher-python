import sys
from model.data_entities.ModelDatatableRow import ModelDatatableRow


class ModelSearchResult:
    def __init__(self, rows: [ModelDatatableRow]):
        self.rows = rows
