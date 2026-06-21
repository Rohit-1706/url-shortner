import random
import string

ALPHABET = string.ascii_letters + string.digits # a-z, A-Z, 0-9 = 62 chars
CODE_LENGTH = 6

def generate_code()->str:
    # 62^6 = 56 billion possible codes
    # collision probability is negligible untill 100M request
    return "".join(random.choices(ALPHABET, k=CODE_LENGTH))