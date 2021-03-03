"""
Simple testing of computational advantages of numpy over standard python looping.

Created by: Tony Held tony.held@gmail.com
Created on: 2020-10-08
Copyright © 2020 Tony Held.  All rights reserved.
"""

import time
import random
import numpy as np

array_size = 1000000

def test1():
    """Add two random arrays together with simple for loops without pre-allocating list size.
    """
    # initialize list with all 0’s
    a = []
    b = []
    c = []

    # add the arrays
    for i in range(array_size):
        x = random.random()
        y = random.random()
        a.append(x)
        b.append(y)
        c.append(x+y)

    # loop through and change the sign of any value less than 0.5
    for i in range(array_size):
        if a[i] < 0.5:
            a[i] *= -1
        if b[i] < 0.5:
            b[i] *= -1
        if c[i] < 0.5:
            c[i] *= -1


def test2():
    """Add two random arrays together with simple for loops with pre-allocation"""

    # pre allocate lists by initialize initial size and populating with with all 0’s
    a = [0.0] * array_size
    b = [0.0] * array_size
    c = [0.0] * array_size

    for i in range(array_size):
        a[i] = random.random()
        b[i] = random.random()
        c[i] = a[i] + b[i]

    # loop through and change the sign of any value less than 0.5
    for i in range(array_size):
        if a[i] < 0.5:
            a[i] *= -1
        if b[i] < 0.5:
            b[i] *= -1
        if c[i] < 0.5:
            c[i] *= -1


def test3():
    """Add two random arrays together with numpy"""
    a = np.random.rand(array_size)
    b = np.random.rand(array_size)
    c = a + b
    a[a < 0.5] *= -1
    b[b < 0.5] *= -1
    c[c < 0.5] *= -1

if __name__ == '__main__':
    print('\nAdding 2 random arrays of length {array_size} using multiple methods')

    t0 = time.perf_counter()
    test1()
    t1 = time.perf_counter()
    method_1 = t1-t0
    print(f"\nAppending to arrays.  Completion time= {method_1}")

    t0 = time.perf_counter()
    test2()
    t1 = time.perf_counter()
    method_2 = t1-t0
    print(f"\nPre-allocated arrays.  Completion time= {method_2}")
    print(f"Increase in calculation speed compared to appending {method_1/method_2}")


    t0 = time.perf_counter()
    test3()
    t1 = time.perf_counter()
    method_3 = t1-t0
    print(f"\nVectorized Solution.  Completion time= {method_3}")
    print(f"Increase in calculation speed compared to appending {method_1/method_3}")
    print(f"Increase in calculation speed compared to pre-allocating {method_2/method_3}")
