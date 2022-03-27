import re
from xlsxparser import xlsx_env


def is_valid_group_number(group_number):
    return re.match(r"^\d{2}-\d{3}$", group_number)


def is_valid_existing_group_number(group_number):
    fixed_groups = [elem.split(' ')[0] for elem in xlsx_env.dgroup]
    return group_number in fixed_groups


def is_valid_time(time):
    return re.match(r"^\d{2}:\d{2}$", time)
