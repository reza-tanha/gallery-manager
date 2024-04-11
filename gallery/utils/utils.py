import random
import string


def generate_password(length=15):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(all_characters, k=length))
    return password
