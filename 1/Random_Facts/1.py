import random
def random_fact():
    with open('corona.txt') as f:
        a = f.read()
        b = a.split('\n')
    print(random.choice(b))
