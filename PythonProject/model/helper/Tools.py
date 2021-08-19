from tools.Logger import logger_log
from model.data_entities.ModelDatatable import ModelDatatable


def get_column_names_as_string_incl_comma_using_datatable(datatable: ModelDatatable):
    """
    Get column names as a string seperated with a comma
    :param datatable: the ModelDatatable
    :return: None is not successful
    """
    if datatable is None:
        return None

    result = ""

    # get column names
    column_names = datatable.get_column_names()
    index = 0
    while index < len(column_names):
        # add column name as TEXT
        result = result + column_names[index] + """ text"""
        if index < len(column_names) - 1:
            result = result + """, """  # add comma if index is not the last element
        index += 1

    logger_log("result: " + result)
    return result