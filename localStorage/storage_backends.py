import os
import stat
import pathlib
import shutil

class localStoragePyStorageException(Exception):
    pass


class BasicStorageBackend:
    def __init__(self, app_namespace: str) -> None:
        # self.base_storage_path = os.path.join(pathlib.Path.home() , ".config", "localStoragePy")
        if app_namespace.count(os.sep) > 0:
            raise localStoragePyStorageException('app_namespace may not contain path separators!')
        self.app_storage_path = os.path.join(pathlib.Path.home() , ".config", "localStoragePy", app_namespace)
        if not os.path.isdir(self.app_storage_path):
            os.makedirs(os.path.join(self.app_storage_path))

    def raise_dummy_exception(self):
        raise localStoragePyStorageException("Called dummy backend!")

    def get_item(self, item: str) -> str:
        self.raise_dummy_exception()

    def set_item(self, item: str, value: any) -> None:
        self.raise_dummy_exception()

    def remove_item(self, item: str) -> None:
        self.raise_dummy_exception()

    def clear(self) -> None:
        self.raise_dummy_exception()
        

class TextStorageBackend(BasicStorageBackend):
    def __init__(self, app_namespace: str) -> None:
        super().__init__(app_namespace)

    def shutil_error_path(self, func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
        func(path)

    def get_file_path(self, key: str) -> os.PathLike:
        return os.path.join(self.app_storage_path, key)

    def get_item(self, key: str) -> str:
        item_path = self.get_file_path(key)
        if os.path.isfile(item_path):
            with open(item_path, "r", encoding="utf8") as item_file:
                return str(item_file.read())
        else:
            return None

    def set_item(self, key: str, value: any) -> None:
        item_path = self.get_file_path(key)
        with open(item_path, "w", encoding="utf8") as item_file:
            item_file.write(str(value))

    def remove_item(self, key: str) -> None: 
        item_path = self.get_file_path(key)
        if os.path.isfile(item_path):
            os.remove(item_path)

    def clear(self) -> None:
        if os.path.isdir(self.app_storage_path):
            shutil.rmtree(self.app_storage_path, onerror=self.shutil_error_path)
        os.makedirs(self.app_storage_path)
