"""calculate_the_sum.py"""


def read_numbers_from_file():
    file = open("file.txt")
    return list(file.read())


def calculate_the_sum_of_evens_in_a_list(list_of_numbers):
    return sum([n for n in list_of_numbers if not n % 2])
