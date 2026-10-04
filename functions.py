print("Hello Sonu")
print("Hello Sonu")
print("Hello Sonu")


def pyhack():
    print(
        "Hello learns this course is made for who want to use python as ethical hacker, penteste, bug hunter and domains like it needs scripting"
    )


pyhack()


def welcome():
    print("Welcome to Python, Sonu!")


welcome()


def greet(name):
    print("Hello", name)


greet("Sonu_Kushwaha")


def add(num1, num2):
    print(num1 + num2)


add(5, 3)


def add(num1, num2):
    return num1 + num2


result = add(10, 20)

print(result)


def get_name():
    return "Sonu"


name = get_name()

print(name)


def get_mess(name):
    return "Hello " + name


mess = get_mess("Sonu kushwaha")

print(mess)


def add(a, b):
    print(a + b)


add(5, 3)


def add(a, b):
    return a + b


answer = add(5, 3)

print(answer)
answer = add(5, 3)

print(answer)
print(answer * 2)


def greet(name="Sonu"):
    print("Hello", name)


greet()
greet("Riya")


def country(name="India"):
    print("Country:", name)


country()
country("Japan")
country("Canada")


def student_info(name, age):
    print(name, "is", age, "years old.")


student_info("Sonu", 20)


def student_info(name, age):
    print(name, "is", age, "years old.")


student_info(name="Sonu", age=20)


def book(title, price):
    print(title, "costs ₹", price)


book(price=499, title="Python Basics")


def show():
    message = "Hello"

    print(message)


show()

name = "Sonu Kushwaha"


def show():
    print(name)


show()


print(name)


x = 10


def show():
    x = 5
    print("Inside function:", x)


show()

print("Outside function:", x)


def greet():
    print("Hello Sonu!")


result = greet()

print(result)


def show():
    print("Python is easy!")


value = show()

print(value)


def add(a, b):
    return a + b


result = add(10, 20)

print(result)


def greet():
    print("Hello")


result = greet()

print(result)


def greet():
    return "Hello"


result = greet()

print(result)


def countdown(number):
    if number == 0:
        print("Done!")
        return

    print(number)
    countdown(number - 1)


countdown(5)


def factorial(number):
    if number == 1:
        return 1

    return number * factorial(number - 1)


print(factorial(6))


def fibonacci(number):
    if number <= 1:
        return number

    return fibonacci(number - 1) + fibonacci(number - 2)


for i in range(6):
    print(fibonacci(i), end=" ")
