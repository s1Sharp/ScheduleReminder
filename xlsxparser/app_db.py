from db_utils import MongodbService, invalid_returned_id
from xlsxparser import parse_current_schedule


storage = MongodbService.get_instance()

if __name__ == "__main__":
    user_id = 913145924
    gr = ["09-811", "09-812"]
    data_subs = {user_id: [gr]}
    if storage.save_data_subs(data_subs) != invalid_returned_id:
        print("Data groups were successfully saved") 
    print(storage.get_data_by_group_key("09-102 (2)"))

    schedule_strings = parse_current_schedule()

    if storage.save_data_schedule(schedule_strings) != invalid_returned_id:
        print("Data groups were successfully saved") 



'''    data_time = parse_time_idx()
    data_group = parse_group_idx()

    if storage.save_data_time(data_time) != invalid_returned_id:
        print("Data time were successfully saved")
    if storage.save_data_groups(data_group) != invalid_returned_id:
        print("Data groups were successfully saved")'''

#   data_subs = {1:[10],2:[3,10], 1:[12]}
