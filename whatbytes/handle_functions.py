import string
import random


def generate_password():
    uppercase = ''.join(random.choices(string.ascii_uppercase, k=4))  # 4 uppercase letters
    lowercase = ''.join(random.choices(string.ascii_lowercase, k=2))  # 2 lowercase letters
    numbers = ''.join(random.choices(string.digits, k=4))  # 4 numbers
    special_characters = ''.join(random.choices("!@#$%^&*()", k=2))  # 2 special characters

    password = list(uppercase + lowercase + numbers + special_characters)
    random.shuffle(password)

    return ''.join(password)


