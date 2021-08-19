import sys
from model.data_entities.ModelDatatableRow import ModelDatatableRow
from model.data_entities.ModelDatatableRowEntry import ModelDatatableRowEntry


class ModelDatatable:
    def __init__(self,
                 datatable_name: str,
                 rows: [ModelDatatableRow]):
        self.datatable_name: str = datatable_name
        self.rows: [ModelDatatableRow] = rows

    def get_datatable_name(self) -> str:
        return self.datatable_name

    def get_column_names(self) -> [str]:
        if self.rows is None:
            return None
        if len(self.rows) < 1:
            return None

        # filter out column names from rows
        row = self.rows[0]
        index = 0
        column_names = []
        while index < len(row.get_row_entries()):
            row_entry = row.get_row_entries()[index]
            if not column_names.__contains__(row_entry.get_column_name()):
                column_names.append(row_entry.get_column_name())
            index += 1

        return column_names

    def get_rows(self) -> [ModelDatatableRow]:
        return self.rows
