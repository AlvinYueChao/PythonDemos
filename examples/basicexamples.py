# Number
# String
# Tuple
# List
# Set
# Dictionary

# If else 语法拆解： print("A") if a > b else print("=") if a == b else print("B")
def findMax(a, b):
    if a > b:
        print("A")
    else:
        if a == b:
            print("=")
        else:
            print("B")

if __name__ == "__main__":
    print("a = 600, b = 200")
    findMax(600, 200)
    print("a = 200, b = 200")
    findMax(200, 200)
    print("a = 200, b = 600")
    findMax(200, 600)