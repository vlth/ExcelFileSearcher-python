import os
from pathlib import Path
from model.data_entities.ModelDatatable import ModelDatatable
from model.helper.SaveHelper import save_datatable
from model.helper.LoadDataHelper import get_datatable_with_name
from model.search.ModelSearchCriteria import ModelSearchCriteria
from model.search.ModelSearchResult import ModelSearchResult


class ModelManager:
    def get_db_folder_name(self):
        return "_persistent_data_"

    def save_datatable(self, datatable: ModelDatatable):
        """
        Save a datatable. Overrides existing table if existing.
        :param datatable: a ModelDatatable
        :return: message if successful or not
        """
        return save_datatable(datatable, self.get_db_folder_name())

    def get_datatables(self) -> [ModelDatatable]:
        """
        Get all existing datatables
        :return: None is not successful
        """

        # get all files in folder
        datatables = []
        path_to_folder = self.get_db_folder_name()
        path = Path(path_to_folder)
        if path.is_dir():
            for filename in os.listdir(path):
                datatable = self.get_datatable_with_name(filename)
                datatables.append(datatable)

        return datatables

    def get_datatable_with_name(self, datatable_name) -> ModelDatatable:
        """
        get datatable with name
        :param datatable_name: name of datatable
        :return: ModelDatatable
        """
        return get_datatable_with_name(datatable_name, self.get_db_folder_name())

    def search_with_criterias(self, criterias: [ModelSearchCriteria]) -> ModelSearchResult:  # param: array of search criterias
        """

        :param criterias:
        :return:
        """
        # TODO...
        return None

    def delete_datatable(self, datatable_name: str):
        """
        Deletes a datatable
        :param datatable_name: name of the datatable
        """
        # check if file with datatable_name already existing and delete if existing
        path_to_file = self.get_db_folder_name() + "/" + datatable_name
        path = Path(path_to_file)
        if path.is_file():
            # remove file
            os.remove(path_to_file)

