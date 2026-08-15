# 1. c = 60, d = 22 ‘Conversion int to float’
c = 60
d = 22
print("Before Conversion:", c, d)
c = float(c)
d = float(d)
print("After Conversion:", c, d)


# 2. Create a dictionary & print your info
my_info = {
    "name": "Faruk Ahmed",
    "age": 22,
    "batch": "CMT-10",
    "institute": "TMSS Technical Institute Bogura",
    "is_student": True
}
print("My Information Dictionary:", my_info)


# 3. Give an example: if, elif, else condition
marks = int(input("Enter your marks: "))

if marks >= 80:
    print("Grade: A+")
elif marks >= 70:
    print("Grade: A")
elif marks >= 60:
    print("Grade: A-")
elif marks >= 50:
    print("Grade: B")
else:
    print("Grade: Fail")
