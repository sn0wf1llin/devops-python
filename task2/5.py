
if __name__ == "__main__":
    n = int(input())
    strings_list = []
    
    for i in range(1, n+1):

        if i % 5 == 0 and i % 3 == 0:
            strings_list.append("FizzBuzz")
        elif i % 3 == 0:
            strings_list.append("Fizz")
        elif i % 5 == 0:
            strings_list.append("Buzz")
        else:
            strings_list.append(str(i))

    print(strings_list)
