import json
import logging
import os
from pathlib import Path

home = Path.home()

DEFAULT_FILE_LOCATION = f"{home}/.meeting-summariser/"


class Files:
    folder_path: str
    logger = logging.getLogger(__name__)

    def __init__(self, folder_path: str = DEFAULT_FILE_LOCATION):
        self.folder_path = folder_path
        self.ensure_folder_exists(folder_path)

    def ensure_folder_exists(self, folder_path: str = DEFAULT_FILE_LOCATION):
        """
        Checks if a folder exists at the specified path.
        If it does not exist, creates the folder.

        :param folder_path: The path of the folder to check/create.
        """
        self.logger.info(f"Ensuring path {folder_path} exists, and creating if not")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.logger.info(f"Folder '{folder_path}' created.")
        else:
            self.logger.info(f"Folder '{folder_path}' already exists.")

    def get_output_path(self, file_name: str) -> str:
        return f"{self.folder_path}{file_name}"

    def write_file(self, file_name: str, contents: str):
        file_path = self.get_output_path(file_name)
        with open(file_path, "w") as file:
            file.write(contents)

        self.logger.info(f"Successfully wrote file {file_path}")

    def read_file(self, file_name: str) -> str:
        file_path = self.get_output_path(file_name)

        with open(file_path, "r") as file:
            data = file.read()
        return data

    def read_json_file(self, file_name: str) -> dict:
        file_path = self.get_output_path(file_name)

        with open(file_path, "r") as file:
            data = json.load(file)
        return data
