from random import shuffle, randint
from typing import Callable, Union
import inspect

def main():
    print(play(100000, 100, random_choice))

def play(num_runs: int, num_prisoners: int, method: Callable, all_info = False) -> Union[float, dict]:
    """
    Master function that allows you to easily call between the functions
    :param num_prisoners: The number of prisoners you would like to run the simulation on
    :param num_runs: The number of runs you would like to do
    :param method: A function that will run the simulation
    :param all_info: Bool when set to true will return a dictionary of all the information you could possible need about
    each run
    :return: A float of the percentage of the success or a dictionary of all outcomes
    """

    num_wins = 0
    boxes = [i for i in range(num_prisoners)]  # makes a list from 0 to num_prisoners
    shuffle(boxes)  # shuffles the list
    boxes = {i: boxes[i] for i in range(num_prisoners)}  # assigns each number 0 to num_prisoners-1 to a random
    # number that corresponds to a box
    try:
        method(boxes, num_prisoners)
    except NameError:
        raise NameError(f"Function {method} does not exist")
    except TypeError:
        raise TypeError(f"Function {method} expected {inspect.getfullargspec(method)} but did not receive it")

    for _ in range(num_runs):
        if method(boxes, num_prisoners):
            num_wins += 1
        boxes = shuffle_dict(boxes)
    if not all_info:
        return num_wins/num_runs
    else:
        return None






def random_choice(boxes: dict, num_prisoners: int) -> bool:  # this works. The probabilities work out
    """
    The function where each individual prisoner randomly chooses num_prisoners/2 boxes
    :param boxes: A dictionary where the key is a integer representing the number on the box and value an int
    representing number in the box
    :param num_prisoners: int representing number of prisoners
    :return: bool True if all made it out, False if they failed
    """
    for i in range(num_prisoners):
        choices = list(range(num_prisoners))  # a list of the boxes that have not been looked in by prisoner i yet
        for j in range(num_prisoners//2):
            look_box = randint(0, num_prisoners - 1 - j)  # random index representing the box number to be looked int
            box = choices[look_box]  # the actual box number of the box to be looked at
            del choices[look_box]  # removes the box from the list of boxes that haven't been looked at
            if boxes[box] == i:
                break
            elif j == (num_prisoners//2) - 1:
                return False
    return True


def loop_method(boxes: dict, num_prisoners: int) -> bool:
    """
    The function where the prisoner opens the box that is his number, and then opens the box with the number inside
    the previous box next
    :param boxes: A dictionary where the key is a integer representing the number on the box and value an int
    representing number in the box
    :param num_prisoners: int representing number of prisoners
    :return: bool True if all made it out, False if they failed
    """
    for i in range(num_prisoners):
        current_box = i
        count = 0
        for _ in range(num_prisoners//2):
            count += 1
            next_box = boxes[current_box]
            if next_box == i:
                break
            elif count == num_prisoners//2:
                return False
            current_box = next_box
    return True


def shuffle_dict(d:dict):
    lst = list(d.values())
    shuffle(lst)
    keys = list(d.keys())
    return dict(zip(keys, lst))


if __name__ == '__main__':
    main()