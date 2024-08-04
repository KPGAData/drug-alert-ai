
import random

def generate_random_phone_number():
    # Generate a random phone number in the format (XXX) XXX-XXXX
    area_code = random.randint(100, 999)
    first_part = random.randint(100, 999)
    second_part = random.randint(1000, 9999)
    return f"({area_code}) {first_part}-{second_part}"