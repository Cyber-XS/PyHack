print("Hello Sonu")
print("Hello Sonu")
print("Hello Sonu")
print("Hello Sonu")
print("Hello Sonu")

i = 1
while i <= 5:
    print("Hello, Sonu Kushwaha")
    i += 1

foods = ["Pizza", "burger"]
for item in foods:
    print("Sonu likes", item)


for i in range(1, 11):
    if i == 5:
        break
    print(i)


for i in range(1, 11):
    if i ==5:
        continue
    print(i)


for i in range(1, 11):
    if i == 5:
        pass
    print(i)


for table in range(1, 4):
    for number in range(1, 4):
        print(table, "x", number, "=", table * number)
