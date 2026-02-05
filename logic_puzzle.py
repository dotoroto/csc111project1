import random

LOCK_CODE = random.randint(1000, 9999)
CRYPIC_MESSAGE = hex(LOCK_CODE)



lock_code_input = input("Please input the locker combination")
if lock_code_input == str(LOCK_CODE):
    #get item
else:
    print("That was not the correct locker combination. Please try again")
