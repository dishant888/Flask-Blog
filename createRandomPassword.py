import string
import random

def createPassword(length):
    s = []
    s.extend(string.ascii_uppercase)
    s.extend(string.ascii_lowercase)
    s.extend(string.digits)
    s.extend(string.punctuation)
    random.shuffle(s)
    password = "".join(s[:length])
    return password

# lenOfPass = int(input('Enter password length: '))



# password = ''

# for i in range(lenOfPass):
#     password += random.choice(s)
#
# print(password)

# print(random.sample(s,lenOfPass))



# print(string.ascii_letters)
#
# print(string.ascii_lowercase)
#
# print(string.ascii_uppercase)
#
# print(string.digits)
#
# print(string.punctuation)
if __name__ == '__main__':
    print(createPassword(12))