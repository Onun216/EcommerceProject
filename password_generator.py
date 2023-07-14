import secrets
import string
import os

letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation
password_alphabet = letters + digits

# User and Supplier
#password_length = 8

# Admin
password_length = 12


id_length = 16


def gen():
    password = ''
    for i in range(password_length):
        password += ''.join(secrets.choice(password_alphabet))
    return password


def key():
    secret_key = secrets.token_hex(16)
    print(secret_key)


em_password = '***********'

pass_key = gen()
print(pass_key)

