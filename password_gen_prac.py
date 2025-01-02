import random

#define diff characters in the password
lowercase = list(range(97, 123))
uppercase = list(range(65, 91))
digits = list(range(48, 58))
special = list(range(33, 48)) + list(range(58,65)) + list(range(91,97)) + list(range(123,127))

password = ""
temp = lowercase.copy()

size = int(input("How long should the password be?: "))

o1 = input("Has uppercase chars? (Y/N): ")
o2 = input("Has digits? (Y/N): ")
o3 = input("Has special chars? (Y/N): ")

if o1.lower() == "y":
    temp.extend(uppercase)
if o2.lower() == "y":
    temp.extend(digits)
if o3.lower() == "y":
    temp.extend(special)

for i in range(size):
    random_char = chr(random.choice(temp))
    password += random_char

print(f"Generated password: {password}")
