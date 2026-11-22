"""A simple command-line calculator."""

import sys


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return round(a / b, 2)


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a, op, b):
    if op not in OPERATIONS:
        raise ValueError(f"Unsupported operator: {op}")
    return OPERATIONS[op](a, b)


def main(argv):
    if len(argv) != 4:
        print("Usage: python calculator.py <number> <operator> <number>")
        print("Operators: " + " ".join(OPERATIONS))
        return 1
    a, op, b = float(argv[1]), argv[2], float(argv[3])
    print(calculate(a, op, b))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
