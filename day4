# Task-1: Calculator with +, -, *, /, %, //, **

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
op = input("Enter operator (+, -, *, /, %, //, **): ")

if op == "+":
    print("Result:", num1 + num2)
elif op == "-":
    print("Result:", num1 - num2)
elif op == "*":
    print("Result:", num1 * num2)
elif op == "/":
    if num2 != 0:
        print("Result:", num1 / num2)
    else:
        print("Error: Division by zero!")
elif op == "%":
    print("Result:", num1 % num2)
elif op == "//":
    print("Result:", num1 // num2)
elif op == "**":
    print("Result:", num1 ** num2)
else:
    print("Invalid operator")

# Task-2: For loop examples

# Tuple
fruits = ("apple", "banana", "cherry")
print("\nTuple Loop:")
for fruit in fruits:
    print(fruit)

# Dictionary
student = {"name": "Parth", "age": 20, "course": "CS"}
print("\nDictionary Loop:")
for key, value in student.items():
    print(key, ":", value)

# Set
numbers = {1, 2, 3, 4, 5}
print("\nSet Loop:")
for num in numbers:
    print(num)

# Task-3: Calculator with match-case

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
op = input("Enter operator (+, -, *, /, %, //, **): ")

match op:
    case "+":
        print("Result:", num1 + num2)
    case "-":
        print("Result:", num1 - num2)
    case "*":
        print("Result:", num1 * num2)
    case "/":
        if num2 != 0:
            print("Result:", num1 / num2)
        else:
            print("Error: Division by zero!")
    case "%":
        print("Result:", num1 % num2)
    case "//":
        print("Result:", num1 // num2)
    case "**":
        print("Result:", num1 ** num2)
    case _:
        print("Invalid operator")


# Task-4: File Concepts in Python

# 1. Create and write to file
with open("example.txt", "w") as f:
    f.write("Hello World!\nThis is Python file handling.")

# 2. Append to file
with open("example.txt", "a") as f:
    f.write("\nAppending new line.")

# 3. Read file
with open("example.txt", "r") as f:
    content = f.read()
print("\nFile Content:\n", content)

# 4. Read line by line
with open("example.txt", "r") as f:
    for line in f:
        print("Line:", line.strip())

# 5. Delete a file (import os)
import os
# os.remove("example.txt")  # Uncomment to delete file

# 6. Check if file exists
print("Does file exist?", os.path.exists("example.txt"))

# 7. Rename file
# os.rename("example.txt", "new_example.txt")  # Uncomment to rename
