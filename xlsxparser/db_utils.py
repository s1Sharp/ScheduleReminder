from pymongo import MongoClient
from xlsxparser.xlsx_env import KEY_WORD_NEXT_DAY
import logging

db_ip               = "localhost"
db_port             = 27017
db_name             = "timetable_db"
time_collection     = "time"
groups_collection   = "groups"
subs_collection     = "subscriptions"
schedule_collection = "schedule"

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

    def check_connection(self) -> bool:
        try:
            self._client.server_info() # will throw an exception if not started
            return True
        except Exception as e:
            logging.error(f"db connection failed {e}") 
            return False

    def get_data(self, colname):
        return list(self._db[str(colname)].find())

    def save_data_time(self, data) -> int:
        try:
            return self._db[time_collection].insert_one(data).inserted_id
        except Exception as e:
            print(e)
            return invalid_returned_id

    def save_data_groups(self, data) -> int:
        try:
            return self._db[groups_collection].insert_one(data).inserted_id
        except Exception as e:
            print(e)
            return invalid_returned_id

    def data_subscriptions(self, group_key, tg_id, time=None, action=None) -> None:
        permited_actions = ['add', 'remove']
        if action in permited_actions:
            try:
                if action == 'add' and time != None:
                    doc = self._db[subs_collection].find_one( {"_id": tg_id} )
                    if doc == None:
                        self._db[subs_collection].insert_one({ '_id': tg_id ,'subs': { group_key:time } })
                        return
                    subs = doc['subs']
                    logging.info(f"db sub before update {tg_id} in time {time} , group {group_key}")
                    subs.clear()
                    subs[group_key] = time
                    self._db[subs_collection].update_one({ '_id': tg_id } , {'$set': { 'subs': subs}})
                    logging.info(f"db set sub {tg_id} in time {time} , group {group_key}")
                    return
                if action == 'remove':
                    doc = self._db[subs_collection].find_one( {"_id": tg_id} )
                    if doc == None:
                        return False
                    self._db[subs_collection].delete_one({ '_id': tg_id })
                    logging.info(f"db remove sub {tg_id}")
                    return True
            except Exception as e:
                print(e)
                return invalid_returned_id

    def get_subscriptions(self):
        '''ret time, tg_id, group_key'''
        result = []
        try:
            doc = self._db[subs_collection].find()
            subs = list(doc)
            for sub in subs:
                for group_key in sub['subs'].keys():
                    result.append( (sub['subs'][group_key], sub['_id'], group_key) )
            return result
        except Exception as e:
            print(e)
            return

    def save_data_schedule(self, data) -> bool:
        try:
            self._db[schedule_collection].delete_many({})
            self._db[schedule_collection].insert_many(data)
            logging.info("db collection schedule updated successfully")
            return True
        except Exception as e:
            logging.error(f"db save_data_schedule error: {e}")
            return False
            
    def get_data_by_group_key(self, group_key, group_sub_key=1):
        try:
            request = f"{group_key} ({group_sub_key})".format(group_key=group_key, group_sub_key=group_sub_key)
            db_ret = self._db[schedule_collection].find_one({'group_key': request})
            day_string = None
            if db_ret != None:
                day_string = db_ret['day_str']
            logging.info("db collect schedule by group key successfully")
            day_strings = day_string.split(KEY_WORD_NEXT_DAY)
            return day_strings
        except Exception as e:
            logging.error(f"db get_data_by_group_key error: {e}")
            return ['Parse schedule error']


if __name__ == "__main__":
    storage = MongodbService.get_instance()
    storage.data_subscriptions(group_key='09-811',tg_id='11111',time='10:00',action='add')
    storage.data_subscriptions(group_key='09-811',tg_id='22222',time='10:00',action='add')
    storage.data_subscriptions(group_key='09-811',tg_id='22222',action='remove')
    storage.data_subscriptions(group_key='09-811',tg_id='00000',action='remove')
    storage.data_subscriptions(group_key='09-822',tg_id='11111',time='12:00',action='add')
    storage.data_subscriptions(group_key='09-822',tg_id='11111',action='remove')
    storage.data_subscriptions(group_key='09-811',tg_id='22222',time='13:00',action='add')
    storage.data_subscriptions(group_key='09-811',tg_id='22222',time='23:00',action='add')
    x = storage.get_subscriptions()
    g=2
