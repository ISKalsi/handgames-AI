import random


def cli_input():
    return int(input('enter a number:'))


def valid(a):
    if 1 <= a <= 10:
        return 1
    else:
        return 0


def batting(target, chasing, *, input_function=cli_input, args=()):
    if chasing:
        print('second innings batting:')
    else:
        print('first innings batting:')
    score = 0

    while 1:
        if chasing:
            print('Target:' + str(target))
        print('score=' + str(score))
        a = input_function(*args)
        b = random.randrange(0, 11, 1) % 11
        if valid(a):
            print('You hit:' + str(a))
            if a == b:
                if chasing and score < target:
                    print('you lost')
                break
            else:
                score = score + a
                if chasing and score >= target:
                    print("You've won")
                    break
        else:
            print('enter a valid number between 1 to 10')
    if not chasing:
        return score


def bowling(target, defending, *, input_function=cli_input, arg=()):
    if defending:
        print("second innings bowling:")
    else:
        print('First Innings bowling')
    score = 0
    while 1:
        if defending:
            print("Target:" + str(target))
        print('Score:' + str(score))
        a = input_function(*arg)
        b = random.randrange(0, 11, 1) % 11
        if valid(a):
            print("comp hit:" + str(b))
            if a == b:
                if defending and score < target:
                    print('you won')
                break
            else:
                score = score + b
                if defending and score >= target:
                    print('you lost')
                    break
        else:
            print('enter a valid number between 1 to 10')
    if not defending:
        return score


def toss():
    while 1:
        coin = int(input('''
    Welcome to our game:
        Toss time
        1-Odd
        2-Even
    Enter:'''))
        if coin == 1 or coin == 2:
            break
        else:
            print("enter appropriate number")

    has_won: int
    while 1:
        number = int(input("Enter number:"))
        # comp=random.randrange(0,11,1)%11
        comp = 2
        # comp=1
        if valid(number):
            if coin == 1 and (number + comp) % 2 != 0:
                has_won = 1
                break
            elif coin == 2 and (number + comp) % 2 == 0:
                has_won = 1
                break
            else:
                has_won = 0
                break

    return has_won
