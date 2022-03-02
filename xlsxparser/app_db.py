from db_utils import MongodbService
from xlsxparser import parse_time_idx, parse_group_idx
storage = MongodbService.get_instance()


if __name__ == "__main__":
    data_time = parse_time_idx()
    data_group = parse_group_idx()

    if storage.save_data_time(data_time):
        print("Data time were successfully saved")
    if storage.save_data_groups(data_group):
        print("Data groups were successfully saved")    
