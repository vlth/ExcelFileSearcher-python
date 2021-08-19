import os
import sqlite3
from sqlite3 import Error
from pathlib import Path
from model.data_entities.ModelDatatable import ModelDatatable
from model.data_entities.ModelDatatableRow import ModelDatatableRow
from model.data_entities.ModelDatatableRowEntry import ModelDatatableRowEntry
from tools.Logger import logger_log
from model.helper.Tools import get_column_names_as_string_incl_comma_using_datatable

RESULT_CODE_KEY = "result_code"
RESULT_MESSAGE_KEY = "result_message"


def get_sql_statement_create_table_for_datatable(datatable: ModelDatatable):
    """
    creates a sql statement to create a table for a ModelDatatable object
    :param datatable: the ModelDatatable object
    :return: None if not successful
    """
    if datatable is None:
        return None

    # sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
    #                                         begin_date text,
    #                                         end_date text
    #                                     ); """
    # begin of statement
    sql_statement = """ CREATE TABLE IF NOT EXISTS """ + \
                    datatable.get_datatable_name() + """("""

    # add column names
    column_names_string = get_column_names_as_string_incl_comma_using_datatable(datatable)
    sql_statement = sql_statement + column_names_string

    # add end of statement
    sql_statement = sql_statement + """);"""
    logger_log("datatable name: "
               + datatable.get_datatable_name()
               + " - result: "
               + sql_statement)
    return sql_statement


def create_datable(db_connection, datatable: ModelDatatable, folder_name):
    """
    Create a datatable. Overrides existing table if existing.
    :param db_connection: the sql connection
    :param datatable: the ModelDatatable object
    :param folder_name: the name of the folder
    :return: code and message
    """

    datatable_name = datatable.get_datatable_name()

    logger_log("now try create datatable with name: " + datatable_name)
    # create database connection to a sqlite database
    try:
        # create table
        # get sql statement
        sql_statement = get_sql_statement_create_table_for_datatable(datatable)

        # get cursor
        cursor = db_connection.cursor()
        # execute
        cursor.execute(sql_statement)

        result_code = 0
        result_message = "success create datatable: " + datatable.get_datatable_name()
    except Error as e:
        logger_log("failed. db operation with error: " + e.args[0])
        result_code = -1
        result_message = "fail create datatable. error: " + e.args[0]
    finally:
        logger_log(result_message)

    return {RESULT_CODE_KEY: result_code,
            RESULT_MESSAGE_KEY: result_message}


def get_sql_statement_insert_data_for_row(datatable_row: ModelDatatableRow):
    """
    Creates a sql statement to insert data
    :param datatable_row: the ModelDatatableRow containing the data
    :return: None if not successful
    """
    if datatable_row is None:
        return None

    # sql = ''' INSERT INTO projects(name,begin_date,end_date)
    #               VALUES(?,?,?) '''
    # begin of statement
    sql_statement = ''' INSERT INTO ''' + \
                    datatable_row.get_datatable_name() + '''('''

    # get column - value pairs
    row_entries = datatable_row.get_row_entries()
    column_names_string = ''
    values_string = ''
    index = 0
    while index < len(row_entries):
        row_entry: ModelDatatableRowEntry = row_entries[index]
        # check if column name is existing
        if row_entry.get_column_name() is None:
            logger_log("failed. column name is NONE. datatable: " + datatable_row.get_datatable_name())
            return None
        # check if row entry value is existing
        if row_entry.get_value() is None:
            row_entry.value = ""  # set empty string if value is not existing

        column_names_string = column_names_string + row_entry.get_column_name()
        values_string = values_string + "\'" + row_entry.get_value() + "\'"
        if index < len(row_entries) - 1:
            column_names_string = column_names_string + ''', '''  # add comma if index is not the last element
            values_string = values_string + ''', '''  # add comma if index is not the last element
        index += 1

    # add column names
    sql_statement = sql_statement + column_names_string

    # add end of first part: "INSERT INTO projects(name,begin_date,end_date)"
    sql_statement = sql_statement \
                    + ''')'''

    # add values and end of statement
    sql_statement = sql_statement \
                    + ''' VALUES(''' \
                    + values_string \
                    + ');'

    logger_log("datatable name: "
               + datatable_row.get_datatable_name()
               + " - result: "
               + sql_statement)
    return sql_statement

def save_datatable(datatable: ModelDatatable, folder_name):
    """
    Save a datatable. Overrides existing table if existing.
    :param datatable: a ModelDatatable
    :return: code and message
    """
    result = {RESULT_CODE_KEY: 0,
              RESULT_MESSAGE_KEY: "success save datatable: " + datatable.get_datatable_name()}

    # create folder if needed
    Path(folder_name).mkdir(parents=True, exist_ok=True)

    # check if file with datatable_name already existing and delete if existing
    path_to_file = folder_name + "/" + datatable.get_datatable_name()
    path = Path(path_to_file)
    if path.is_file():
        # remove file
        os.remove(path_to_file)

    try:
        # connect to database
        connection = sqlite3.connect(path_to_file)
        logger_log("established db connection. " + "sqlite3.version: " + sqlite3.version)

        # create
        result = create_datable(connection, datatable, folder_name)
        # if not successful
        if not result[RESULT_CODE_KEY] == 0:
            return result

        #
        # insert data
        #
        logger_log("now try insert data into datatable with name: " + datatable.get_datatable_name())

        # for all rows
        for row in datatable.get_rows():
            # get sql statement
            sql_statement = get_sql_statement_insert_data_for_row(row)
            # get cursor
            cursor = connection.cursor()
            # execute
            cursor.execute(sql_statement)
            logger_log("success insert row.")

        result = {RESULT_CODE_KEY: 0,
                  RESULT_MESSAGE_KEY: "success save datatable: " + datatable.get_datatable_name()}
    except Error as e:
        logger_log("failed. db operation with error: " + e.args[0])
        result[RESULT_CODE_KEY] = -1
        result[RESULT_MESSAGE_KEY] = "failed saving datatable. error: " + e.args[0]
    finally:
        if connection:
            connection.commit()
            connection.close()
            logger_log("db connection closed: " + datatable.get_datatable_name())
            logger_log(result[RESULT_MESSAGE_KEY])
    return result
