import sys
from view.ViewManager import ViewManager


class PresenterManager:
    def start_application(self):
        view_manager = ViewManager()
        view_manager.show_application()

