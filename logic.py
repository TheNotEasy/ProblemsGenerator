import random
import sys
import traceback
from dataclasses import dataclass
from enum import Enum
from functools import cached_property


class Action(Enum):
    MINUS = '-'
    PLUS = '+'
    MULTIPLY = '*'
    DIVISION = '/'

    @classmethod
    def get_random(cls, exclude=None):
        if exclude is None:
            exclude = ()
        members = [i for i in tuple(cls.__members__) if i not in exclude]
        action = getattr(cls, random.choice(members), None)
        if action is None:
            print("Warning: generated 'None' action")
        return action

    def __repr__(self):
        return f'<Action {self.name}>'


@dataclass
class Problem:
    x: int
    y: int
    action: Action

    @cached_property
    def answer(self):
        return calculate_numbers(self.x, self.y, self.action)

    def __repr__(self):
        return f'<Problem x={self.x} y={self.y} action={self.action} answer={self.answer}>'

    def __str__(self):
        return f'{self.x} {self.action.value} {self.y}'


def generate_problem(num_range, answer_range=None, action=None):
    if num_range <= 2:
        raise ValueError("num_range is too small")
    try:
        x = random.randint(0, num_range)
        if action is None:
            action = Action.get_random((Action.DIVISION,) if num_range <= 10 else None)
        if action is Action.MINUS:
            y = random.randint(2, x)
        elif action is Action.DIVISION:
            y = random.choice([i for i in range(2, num_range+1) if x % i == 0 if not x == i])
            if y == 0:
                y = 1
        elif action is Action.MULTIPLY:
            if x == 0:
                y = random.randint(2, num_range)
            else:
                y = random.randint(2, int(answer_range / x) if answer_range else num_range)
        else:
            y = random.randint(0, answer_range or num_range - x)

        return Problem(x, y, action)
    except Exception:
        print("Error has occured, ignoring and generate new problem", file=sys.stderr)
        traceback.print_exc()
        return generate_problem(num_range, answer_range, action)


def calculate_numbers(x, y, action):
    return eval(f'x {action.value} y', {'x': x, 'y': y})


@dataclass
class Results:
    correct: int = 0
    incorrect: int = 0


if __name__ == '__main__':
    print(generate_problem(20))
