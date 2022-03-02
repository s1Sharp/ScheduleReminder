from pymongo import MongoClient


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
        self._client = MongoClient("localhost", 27017)
        self._db = self._client['timetable_db']

    def get_data(self, colname):
        return list(self._db[str(colname)].find())

    def save_data_time(self, dto) -> bool:
        try:
            self._db['time'].insert_one(dto)
            return True
        except Exception as e:
            print(e)
            return False

    def save_data_groups(self, dto) -> bool:
        try:
            self._db['groups'].insert_one(dto)
            return True
        except Exception as e:
            print(e)
            return False