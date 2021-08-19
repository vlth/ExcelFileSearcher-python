import sys


class ModelSearchCriteria:
    def __init__(self, datatable_names: [str], column_names: [str], search_text: str ):
        self.datatable_names = datatable_names
        self.column_names = column_names
        self.search_text = search_text
