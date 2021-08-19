import os
import sqlite3
from sqlite3 import Error
from pathlib import Path
from model.data_entities.ModelDatatable import ModelDatatable
from model.data_entities.ModelDatatableRow import ModelDatatableRow
from model.data_entities.ModelDatatableRowEntry import ModelDatatableRowEntry
from tools.Logger import logger_log

RESULT_CODE_KEY = "result_code"
RESULT_MESSAGE_KEY = "result_message"


def get_string_from_list_with_seperator(list: [str], seperator: str):
    result = ""
    index = 0
    while index < len(list):
        result = result + list[index]
        if index < len(list) - 1:
            result = result + seperator
        index += 1
    return result

def get_datatable_with_name(datatable_name, folder_name) -> ModelDatatable:
    """
    load datatable
    :param datatable_name: name of db file
    :param folder_name: folder name
    :return: None is not successful
    """
    if datatable_name is None:
        return None

    # check if file with datatable_name is existing
    path_to_file = folder_name + "/" + datatable_name
    path = Path(path_to_file)
    if not path.is_file():
        logger_log("failed. file not existing: " + path_to_file)
        return None

    try:
        # connect to database
        connection = sqlite3.connect(path_to_file)
        logger_log("established db connection. " + "sqlite3.version: " + sqlite3.version)

        # select data
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + datatable_name)  # load ALL rows from datatable
        rows_raw_data = cursor.fetchall()
        column_names = []
        for desc in cursor.description:
            column_name = desc[0]
            column_names.append(column_name)

        # check if there is data
        if len(rows_raw_data) < 1:
            logger_log("datatable returned with no rows. datatable: " + datatable_name)
            return None

        # check if tuple count is equal to column count
        if len(column_names) != len(rows_raw_data[0]):
            logger_log("failed. column count not equal to tuple count of raw data of the first row.")

        column_names_string = get_string_from_list_with_seperator(column_names, " , ")
        logger_log("start creating data for columns: " + column_names_string)

        # create return data
        rows_result = []
        # iterate over all rows
        index_row = 0
        while index_row < len(rows_raw_data):  # rows_raw_data looks like this: [('111', '222', '333'), ('333', '444', '555')]
            row_entries = []
            # get the row as a tuple.
            row_raw_data_tuple = rows_raw_data[index_row]  # this looks like this: ('111', '222', '333')
            # iterate over all values in the row/in the tuple
            index_tuple = 0
            while index_tuple < len(row_raw_data_tuple):
                column_name = column_names[index_tuple]  # this is the column name
                row_entry_value = row_raw_data_tuple[index_tuple]  # this is the actual value of the entry. for example '111'
                # create the row entry
                row_entry = ModelDatatableRowEntry(datatable_name, column_name, row_entry_value)
                # save the row entry
                row_entries.append(row_entry)
                # increment for next entry in tuple
                index_tuple += 1
            # here we are finished with all entries in the row. time to save the row now
            row = ModelDatatableRow(datatable_name, row_entries)
            rows_result.append(row)
            # increment for next row
            index_row += 1

        return ModelDatatable(datatable_name, rows_result)

    except Error as e:
        logger_log("failed. db operation with error: " + e.args[0])

    finally:
        if connection:
            connection.close()
            logger_log("db connection closed: " + datatable_name)

    return None
