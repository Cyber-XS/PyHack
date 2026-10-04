student = {
    "name" : "Sonu Kushwaha",
    "Age" : "20",
    "State" : "Bihar",
    "Gender" : "Male"
}

print(student["name"])
print(student["Age"])
print(student["State"])

student["college"] = "Cyber XS Academy"

print(student)

student["Age"] = "21"

print(student)

student.pop("Gender")

print(student)

print(student.keys())
print(student.values())
print(student.items())
print(student.get("name"))

profile = {
"username": "sonukushwaha",
"details": {
"followers": 1200,
"verified": True
}
}
print(profile["details"]["followers"])    # 1200


languages = {"Python", "Java", "C++", "Python"}
print(languages)

empty_set = set()
nums = {1, 2, 3}
num2 = {"1", "2", "3","4"}
nums.add(5)

print(empty_set)
print(nums)
print(num2)

# Creating two sets
set1 = {"Python", "Java", "C++"}
set2 = {"Java", "JavaScript", "Go"}

# Combining both sets
result = set1.union(set2)

print(result)

# Creating two sets
set1 = {"Python", "Java", "C++"}
set2 = {"Java", "JavaScript", "Python"}

# Finding common elements
result = set1.intersection(set2)

print(result)