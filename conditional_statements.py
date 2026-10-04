age = 18
print(age <= 18)

age = int(input("Enter your age: "))
if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible.")

marks = int(input("Enter marks: "))
if marks >= 90:
    print("Grade A")
elif marks >= 80:
    print("Grade B")
elif marks >= 70:
    print("Grade C")
else:
    print("Grade D")

marks = [10, 20, 30, 40]
foods = ["Samosa", "Pizza", "Burger"]
student = ["Sonu Kushwaha", 20, "Bihar"]

print(foods[0]) # Samosa
print(foods[2]) # Burger
print(student[0])
print(marks)

print(len(marks))
print(max(marks))
print(min(marks))

marks.append(99)
marks.insert(1, 80)
marks.remove(40)

print(marks)

tup = (87, 64, 33, 95, 76)
print(tup[3]) # 87
