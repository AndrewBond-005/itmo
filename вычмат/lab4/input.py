
import math
def input_from_console():
    print("Enter number of points (8-12):")
    n = int(input())

    x = []
    y = []

    print("Enter pairs x y (space separated):")
    for i in range(n):
        line = input(f"Point {i+1}: ")
        parts = line.split()
        x.append(float(parts[0]))
        y.append(float(parts[1]))

    return x, y, n

def input_from_file(filename):
    x = []
    y = []

    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.split()
                x.append(float(parts[0]))
                y.append(float(parts[1]))

    n = len(x)
    return x, y, n

