# 1. List:
# Create a list of numbers from 1 to 10 and print only the even numbers.

# numbers = list(range(1, 11))  # 1 to 10 list

# #first method
# for num in numbers:
#     if num % 2 == 0:
#         print(num, end=" ")
# print()

#second method (using index)
# for num in range(len(numbers)):
#     if numbers[num] % 2 == 0:
#         print(numbers[num], end=" ")
# print()

#third method (using enumerate)
# for index, num in enumerate(numbers):
#     if num % 2 == 0:
#         print(num, end=" ")
# print()

# 2. Tuple:
# Given t = (3, 5, 7, 3), count how many times 3 appears.
# t = (3, 5, 7, 3)
# print(t.count(3))  # count occurrences of 3

# 3. Set:
# Find the common elements between {1,2,3,4} and {3,4,5,6}.
# s1 = {1,2,3,4}
# s2 = {3,4,5,6}
# print(s1.intersection(s2))  # {3, 4}

# 4. For Loop:
# Print all numbers from 1 to 20 that are divisible by 3.
# for num in range(1, 21):
#     if num % 3 == 0:
#         print(num, end=" ")
        
# 5. Dictionary:
# Create a dictionary of 3 students with their marks, then print the student with
# the highest mark.

# first method
# students = {
#     "Alice": 88,
#     "Bob": 92,
#     "Charlie": 79
# }
# print(max(students, key=students.get))  # Bob   

# second method
# highest_student = None
# highest_marks = -1   # any small value keep at the beginning

# for name, marks in students.items():
#     if marks > highest_marks:
#         highest_marks = marks
#         highest_student = name

# print(f"Highest marks: {highest_student} = {highest_marks}")


# 6. List & Function:
# Write a function that takes a list and returns a new list with all elements doubled.
# def double_list(lst):
#     return [x * 2 for x in lst] # using list comprehension
# print(double_list([1, 2, 3, 4]))

# 7. Dictionary & Loop:
# Given {'a': 1, 'b': 2, 'c': 3}, write a loop to print keys with even values.
# d = {'a': 1, 'b': 2, 'c': 3}
# for key, value in d.items():
#     if value % 2 == 0:
#         print(key)

# 8. Set & Function:
# Write a function that takes a list and returns a set of unique elements.
# def unique_set(lst):
#     return set(lst) # using set function
# print(unique_set([1, 2, 2, 3, 4, 4]))

# 9. Combined Challenge:
# Given a list of dictionaries like [{'name':'Ali','age':20},{'name':'Sara','age':25}], write code to print names of people older than 21.
# people = [{'name':'Ali','age':20},{'name':'Sara','age':25}]
# for person in people:
#     if person['age'] > 21:
#         print(person['name'])