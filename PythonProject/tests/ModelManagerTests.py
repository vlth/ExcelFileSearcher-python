import unittest
import uuid
import os
from pathlib import Path
from model.ModelManager import ModelManager
from model.helper.SaveHelper import get_sql_statement_create_table_for_datatable
from model.data_entities.ModelDatatable import ModelDatatable
from model.data_entities.ModelDatatableRow import ModelDatatableRow
from model.data_entities.ModelDatatableRowEntry import ModelDatatableRowEntry


class ModelManagerTests(unittest.TestCase):

    def setUp(self) -> None:
        # delete test datables to start fresh
        # check if file with datatable_name already existing and delete if existing
        model_manager = ModelManager()
        path_to_folder = model_manager.get_db_folder_name()
        path = Path(path_to_folder)
        if path.is_dir():
            for filename in os.listdir(path):
                path_to_file = path_to_folder + "/" + filename
                path = Path(path_to_file)
                if path.is_file():
                    # remove file
                    os.remove(path_to_file)

        # datatable name
        self.datatable_name = "test_database_file_" + str(uuid.uuid4())
        self.datatable_name = self.datatable_name.replace("-", "_")

        """
                | column 1 | column 2
        
        row 1      111         222 

        row 2      333         444

        """

        # column names
        self.column_name_1 = "column_1"
        self.column_name_2 = "column_2"

        # row 1
        self.row_1_column_1_value = "111"
        self.row_1_column_2_value = "222"
        row_1_entry_1 = ModelDatatableRowEntry(self.datatable_name, self.column_name_1, self.row_1_column_1_value)
        row_1_entry_2 = ModelDatatableRowEntry(self.datatable_name, self.column_name_2, self.row_1_column_2_value)
        row_entries = [row_1_entry_1,
                       row_1_entry_2]
        row_1 = ModelDatatableRow(self.datatable_name, row_entries)

        # row 2
        self.row_2_column_1_value = "333"
        self.row_2_column_2_value = "444"
        row_2_entry_1 = ModelDatatableRowEntry(self.datatable_name, self.column_name_1, self.row_2_column_1_value)
        row_2_entry_2 = ModelDatatableRowEntry(self.datatable_name, self.column_name_2, self.row_2_column_2_value)
        row_entries = [row_2_entry_1,
                       row_2_entry_2]
        row_2 = ModelDatatableRow(self.datatable_name, row_entries)

        # create datatable
        self.datatable = ModelDatatable(self.datatable_name,
                                        [row_1, row_2])

    def test_save_and_get_datatable(self):
        # check column names
        column_name_to_check = self.datatable.get_column_names()[0]
        self.assertEqual(self.column_name_1, column_name_to_check)
        column_name_to_check = self.datatable.get_column_names()[1]
        self.assertEqual(self.column_name_2, column_name_to_check)

        # save datatable
        model_manager = ModelManager()
        model_manager.save_datatable(self.datatable)

        # get datatable
        datatable_result = model_manager.get_datatable_with_name(self.datatable_name)

        # check values
        # datatable name
        self.assertEqual(self.datatable_name, datatable_result.get_datatable_name())
        # column names
        self.assertEqual(self.column_name_1, datatable_result.get_column_names()[0])
        self.assertEqual(self.column_name_2, datatable_result.get_column_names()[1])
        # row 1 - column 1
        row_result: ModelDatatableRow = datatable_result.get_rows()[0]
        entry: ModelDatatableRowEntry = row_result.get_row_entries()[0]
        self.assertEqual(self.row_1_column_1_value, entry.get_value())
        self.assertEqual(self.column_name_1, entry.get_column_name())
        # row 1 - column 2
        entry = row_result.get_row_entries()[1]
        self.assertEqual(self.row_1_column_2_value, entry.get_value())
        self.assertEqual(self.column_name_2, entry.get_column_name())

        # row 2 - column 1
        row_result = datatable_result.get_rows()[1]
        entry = row_result.get_row_entries()[0]
        self.assertEqual(self.row_2_column_1_value, entry.get_value())
        self.assertEqual(self.column_name_1, entry.get_column_name())
        # row 2 - column 2
        entry = row_result.get_row_entries()[1]
        self.assertEqual(self.row_2_column_2_value, entry.get_value())
        self.assertEqual(self.column_name_2, entry.get_column_name())

    def test_null_value_in_datatable(self):
        # row
        column_1_value = "test"
        column_2_value = None  # NONE VALUE
        entry_1 = ModelDatatableRowEntry(self.datatable_name, self.column_name_1, column_1_value)
        entry_2 = ModelDatatableRowEntry(self.datatable_name, self.column_name_2, column_2_value)
        row_entries = [entry_1,
                       entry_2]
        row_1 = ModelDatatableRow(self.datatable_name, row_entries)
        self.datatable.rows.append(row_1)

        # save datatable
        model_manager = ModelManager()
        model_manager.save_datatable(self.datatable)

        # get datatable
        datatable_result = model_manager.get_datatable_with_name(self.datatable_name)

        # get last row
        row: ModelDatatableRow = datatable_result.get_rows()[2]
        # get last entry
        entry: ModelDatatableRowEntry = row.get_row_entries()[1]
        self.assertEqual(entry.get_value(), '')  # NONE value should result in empty string

    def test_get_all_datatables(self):
        # save datatable
        model_manager = ModelManager()
        model_manager.save_datatable(self.datatable)

        # modify datatable to "create a second one"
        # set new datatable name
        datatable_name_2 = "test_database_file_" + str(uuid.uuid4())
        datatable_name_2 = datatable_name_2.replace("-", "_")
        self.datatable.datatable_name = datatable_name_2

        # modify existing rows
        # first row
        existing_row: ModelDatatableRow = self.datatable.rows[0]
        existing_row.datatable_name = datatable_name_2
        # first row first entry
        row_entry: ModelDatatableRowEntry = existing_row.row_entries[0]
        row_entry.value = "123"
        # first row second entry
        row_entry: ModelDatatableRowEntry = existing_row.row_entries[1]
        row_entry.value = "123"
        # second row
        existing_row = self.datatable.rows[1]
        existing_row.datatable_name = datatable_name_2
        # second row first entry
        row_entry: ModelDatatableRowEntry = existing_row.row_entries[0]
        row_entry.value = "123"
        # second row second entry
        row_entry: ModelDatatableRowEntry = existing_row.row_entries[1]
        row_entry.value = "123"

        # add a row
        column_1_value = "123"
        column_2_value = "123"
        entry_1 = ModelDatatableRowEntry(self.datatable_name, self.column_name_1, column_1_value)
        entry_2 = ModelDatatableRowEntry(self.datatable_name, self.column_name_2, column_2_value)
        row_entries = [entry_1,
                       entry_2]
        row_1 = ModelDatatableRow(datatable_name_2, row_entries)
        self.datatable.rows.append(row_1)

        # save second datatable
        model_manager.save_datatable(self.datatable)

        # now get all datatables
        all_datatables: [ModelDatatable] = model_manager.get_datatables()

        # check values
        self.assertEqual(len(all_datatables), 2)  # should be two datatables
        self.assertNotEqual(all_datatables[0], None)
        self.assertNotEqual(all_datatables[1], None)
        # because we dont know which datatable comes first, we need to if here
        if len(all_datatables[0].rows) is 2:
            self.assertEqual(len(all_datatables[1].rows), 3)
        else:
            self.assertEqual(len(all_datatables[1].rows), 2)

        # check second datatable
        datatable_2_result: [ModelDatatable] = None
        if all_datatables[0].get_datatable_name() == datatable_name_2:
            datatable_2_result = all_datatables[0]
            self.assertEqual(len(all_datatables[0].rows), 3)
        elif all_datatables[1].get_datatable_name() == datatable_name_2:
            datatable_2_result = all_datatables[1]
            self.assertEqual(len(all_datatables[1].rows), 3)

        # check some rows
        # check first row
        row_to_check: ModelDatatableRow = datatable_2_result.rows[0]
        row_entry: ModelDatatableRowEntry = row_to_check.get_row_entries()[0]
        self.assertEqual(row_entry.get_value(), "123")

        # check third row
        row_to_check: ModelDatatableRow = datatable_2_result.rows[2]
        row_entry: ModelDatatableRowEntry = row_to_check.get_row_entries()[0]
        self.assertEqual(row_entry.get_value(), "123")

    def test_delete_datatable(self):
        # save datatable
        model_manager = ModelManager()
        model_manager.save_datatable(self.datatable)

        path_to_file = model_manager.get_db_folder_name() + "/" + self.datatable.datatable_name
        path = Path(path_to_file)
        self.assertEqual(path.is_file(), True)

        # delete datatable
        model_manager.delete_datatable(self.datatable.datatable_name)

        path_to_file = model_manager.get_db_folder_name() + "/" + self.datatable.datatable_name
        path = Path(path_to_file)
        self.assertEqual(path.is_file(), False)


if __name__ == '__main__':
    unittest.main()
