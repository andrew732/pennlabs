# Implement modulo without using the (%) operator.
def modulo(a, b):
    return a - (a // b) * b


# Take an input string and determine if exactly 3 question marks
# exist between every pair of numbers that add up to 10.
# If so, return true, otherwise return false. 
def question_mark(s):
    indices = {}
    # Cumulative array of '?' counts
    cumulative = []
    i = -1
    counter = 0

    # On first pass, mark indices of all digits and location of '?'
    for c in s:
        i += 1
        if c.isdigit():
            c = int(c)
            if c in indices:
                temp = indices.get(c)
                temp.append(i)
                indices.update({c: temp})
            else:
                indices.update({c: [i]})
        if c is '?':
            counter = counter + 1
        cumulative.append(counter)

    # print("Indices", indices)
    # print("Cumulative", cumulative)

    # Check each pair of digits for 3 '?'s
    i = -1
    for c in s:
        i += 1
        if c.isdigit():
            c = int(c)
            if 10 - c in indices:
                temp = indices.get(10 - c)
                for j in range(0, len(temp)):
                    if abs(cumulative[temp[j]] - cumulative[i]) != 3:
                        return False
    return True


if __name__ == '__main__':
    print(modulo(1, 3))  # 1
    print(modulo(3, 1))  # 0
    print(modulo(2, 3))  # 2
    print(modulo(3, 2))  # 1
    print(modulo(213, 9))  # 6

    print(question_mark("1234"))  # True, no pairs add to 10
    print(question_mark(""))  # True, no pairs add to 10
    print(question_mark("wqwerq"))  # True, no pairs add to 10
    print(question_mark("123455"))  # False, 5 and 5 have no question marks
    print(question_mark("12345??6"))  # False, 6 and 4 have 2 question marks
    print(question_mark("7???3"))  # True, 7 and 3 are valid
    print(question_mark("7???33"))  # True, 7 and 3, 3 are valid
    print(question_mark("7???33??6???4"))  # True, 7 and 3, 3 and 6, 4 are valid
    print(question_mark("7???33??6???47"))  # False, 3 and the last 7 have more than 3 '?'
