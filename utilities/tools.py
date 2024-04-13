# tools.py
import datetime

def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def date_to_str(date_obj):
    return date_obj.strftime('%Y-%m-%d')

def calculate_percentage_change(new_value, old_value):
    return ((new_value - old_value) / old_value) * 100

# Example usage:
if __name__ == "__main__":
    print("Convert string to date:", str_to_date('2021-01-01'))
    print("Convert date to string:", date_to_str(datetime.datetime.now()))
    print("Calculate percentage change from 100 to 150:", calculate_percentage_change(150, 100))
