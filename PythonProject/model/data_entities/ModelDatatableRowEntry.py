import sys


class ModelDatatableRowEntry:
    def __init__(self,
                 datatable_name,
                 column_name,
                 value):
        self.datatable_name = datatable_name
        self.column_name = column_name
        self.value = value

    def get_datatable_name(self):
        return self.datatable_name

    def get_column_name(self):
        return self.column_name

    def get_value(self):
        return self.value
