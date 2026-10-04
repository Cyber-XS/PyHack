f = open("text.txt", "r")
print(f.read())
f.close()


with open("text.txt", "r") as f:
    data = f.read()
    print(data)


with open("text.txt", "r") as f:
    data = f.readline()
    print(data)


with open("text.txt", "r") as f:
    data = f.readlines()
    print(data)


with open("text.txt", "w") as f:
    f.write("Cyber XS")


with open("text.txt", "a") as f:
    f.write("\nWelcome to cyber world")
