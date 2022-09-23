import random

INSTANCES_NUM = 1000
RANGE_MIN     = 0
RANGE_MAX     = 100000

if __name__ == "__main__":
    min = max = random.randint(0, RANGE_MAX)

    print("1) " + str(min))
    for i in range(0, INSTANCES_NUM - 1):
        num = random.randint(RANGE_MIN, RANGE_MAX)
        print(str(i+2) + ") "  + str(num))
        if num < min:
            min = num
        if num > max:
            max = num

    print("MAX: " + str(max))
    print("MIN: " + str(min))
