from createRandomPassword import createPassword

SECURE = (('s','$'),('I','|'),('a','@'),('o','0'),('i','1'))

def securePassword(password):
    for a,b in SECURE:
        password = password.replace(a,b)
    return password

if __name__ == '__main__':
    password = createPassword(12)
    print(securePassword(password))