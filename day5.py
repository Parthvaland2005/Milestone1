# Task-1: Fibonacci & Factorial using Recursion

# Factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Testing
num = 5
print(f"Factorial of {num}:", factorial(num))

print(f"Fibonacci Series up to {num} terms:")
for i in range(num):
    print(fibonacci(i), end=" ")

# Task-2: Using OS, MATH, RANDOM modules

import os
import math
import random

# --- OS Module ---
print("\n--- OS Module ---")
print("Current Working Directory:", os.getcwd())
print("List of Files:", os.listdir())

# --- MATH Module ---
print("\n--- MATH Module ---")
print("Square root of 16:", math.sqrt(16))
print("Factorial of 5:", math.factorial(5))
print("Power (2^3):", math.pow(2, 3))
print("Pi value:", math.pi)

# --- RANDOM Module ---
print("\n--- RANDOM Module ---")
print("Random number between 1-10:", random.randint(1, 10))
print("Random float [0,1):", random.random())
print("Random choice from list:", random.choice(["apple", "banana", "cherry"]))

# Task-3: Comprehensions & Arguments

# --- List Comprehension ---
squares = [x**2 for x in range(1, 6)]
print("\nList Comprehension (Squares):", squares)

# --- Tuple Comprehension (Generator Expression then tuple) ---
evens = tuple(x for x in range(10) if x % 2 == 0)
print("Tuple Comprehension (Evens):", evens)

# --- Dictionary Comprehension ---
squares_dict = {x: x**2 for x in range(1, 6)}
print("Dictionary Comprehension:", squares_dict)


# --- *args Example ---
def sum_numbers(*args):
    return sum(args)

print("\nSum using *args:", sum_numbers(1, 2, 3, 4, 5))

# --- **kwargs Example ---
def print_student(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} : {value}")

print("\nStudent Details using **kwargs:")
print_student(name="Parth", age=20, course="CS")
