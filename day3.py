# Task-2: Functions Manipulating Lists

fruits = ["apple", "banana", "cherry"]

# Adding elements
fruits.append("orange")      # add at end
fruits.insert(1, "mango")    # add at index 1

# Removing elements
fruits.remove("banana")      # remove by value
popped_item = fruits.pop()   # remove last element
del fruits[0]                # delete by index

# Other functions
fruits.extend(["grape", "kiwi"])  # add multiple elements
fruits.sort()                     # sort list
fruits.reverse()                  # reverse order
count_kiwi = fruits.count("kiwi") # count occurrence

print("Final List:", fruits)
print("Popped Item:", popped_item)
print("Count of 'kiwi':", count_kiwi)

# Task-3: Built-in Functions for Dictionary

student = {
    "name": "Parth",
    "age": 20,
    "course": "CS"
}

# Access keys, values, items
print("Keys:", student.keys())
print("Values:", student.values())
print("Items:", student.items())

# Add / Update
student.update({"age": 21, "grade": "A"})

# Remove
removed_value = student.pop("course")   # remove by key
last_item = student.popitem()           # remove last inserted item

# Get value safely
print("Age:", student.get("age"))
print("Grade:", student.get("grade"))

print("Updated Dictionary:", student)
print("Removed Course:", removed_value)
print("Last Popped Item:", last_item)

# Task-4: Functions to Modify Set

numbers = {1, 2, 3}

# Add elements
numbers.add(4)
numbers.update([5, 6, 7])

# Remove elements
numbers.remove(2)          # error if not found
numbers.discard(10)        # no error if not found
removed_item = numbers.pop()  # remove random element

# Clear set
temp_set = {100, 200}
temp_set.clear()

print("Modified Set:", numbers)
print("Removed Random Item:", removed_item)
print("Cleared Set:", temp_set)

# Task-5: Set Operations

A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

# Union
print("Union:", A | B)

# Intersection
print("Intersection:", A & B)

# Difference
print("Difference (A - B):", A - B)

# Symmetric Difference
print("Symmetric Difference:", A ^ B)

# Subset / Superset
print("Is A subset of B?", A.issubset(B))
print("Is A superset of B?", A.issuperset(B))
