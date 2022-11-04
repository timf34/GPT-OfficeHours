def does_calling_set_randomize_a_list():
    our_str_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    print_experiment(our_str_list)  # This is random!

    our_int_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print_experiment(our_int_list)  # This is in order!


def print_experiment(_list):
    print(f"our_list: {_list}")
    print(f"calling set on our_list: {set(_list)}")
    print("list(set()): ", list(set(_list)))


if __name__ == '__main__':
    does_calling_set_randomize_a_list()
