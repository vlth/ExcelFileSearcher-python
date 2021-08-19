import sys
from model.data_entities.ModelDatatableRowEntry import ModelDatatableRowEntry

class ModelDatatableRow:
    def __init__(self,
                 datatable_name,
                 row_entries: [ModelDatatableRowEntry]):
        self.datatable_name = datatable_name
        self.row_entries: [ModelDatatableRowEntry] = row_entries

    def get_datatable_name(self):
        return self.datatable_name

    def get_row_entries(self) -> [ModelDatatableRowEntry]:
        return self.row_entries