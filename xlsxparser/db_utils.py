from pymongo import MongoClient

db_ip = "localhost"
db_port = 27017
db_name = "timetable_db"
time_collection = "time"
groups_collection = "groups"
subs_collection = "subscriptions"

invalid_returned_id = -1


class MongodbService(object):
    _instance = None
    _client = None
    _db = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._client = MongoClient(db_ip, db_port)
        self._db = self._client[db_name]

    def get_data(self, colname):
        return list(self._db[str(colname)].find())

    def save_data_time(self, data):
        try:
            return self._db[time_collection].insert_one(data).inserted_id
        except Exception as e:
            print(e)
            return invalid_returned_id

    def save_data_groups(self, data):
        try:
            return self._db[groups_collection].insert_one(data).inserted_id
        except Exception as e:
            print(e)
            return invalid_returned_id

    def save_data_subs(self, data):
        try:
            return self._db[subs_collection].insert_one(data).inserted_id
        except Exception as e:
            print(e)
            return invalid_returned_id
