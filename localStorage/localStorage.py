from storage_backends import TextStorageBackend

class localStoragePy:
    def __init__(self, app_namespace: str, storage_backend: str = "text") -> None:
        self.storage_backend_instance = TextStorageBackend(app_namespace)

    def getItem(self, item: str) -> any:
        return self.storage_backend_instance.get_item(item)

    def setItem(self, item: str, value: any) -> None:
        self.storage_backend_instance.set_item(item, value)

    def removeItem(self, item: str) -> None:
        self.storage_backend_instance.remove_item(item)

    def clear(self):
        self.storage_backend_instance.clear()

