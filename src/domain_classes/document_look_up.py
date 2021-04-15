class DocumentLookUp:
    def __init__(self, lookup_id, repository, database_id, path, type):
        self.lookup_id = lookup_id
        self.repository = repository
        self.database_id = database_id
        self.path = path
        self.type = type

    def to_dict(self):
        return {
            "repository": self.repository,
            "databaseId": self.database_id,
            "lookUpId": self.lookup_id,
            "path": self.path,
            "type": self.type,
        }
