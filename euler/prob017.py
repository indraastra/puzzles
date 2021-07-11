words = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
        1000: "thousand" }

def toSentence(n):
    if n == 0:
        return ""
    if n <= 20:
        return words[n]
    else:
        if 20 < n <= 99:
            a = (n//10)*10
            m = n%10
            middle = ""
        elif 100 <= n <= 999:
            a = n//100
            m = n%100
            middle = "hundred"
            if m != 0:
                middle += "and"
        elif 1000 <= n <= 9999:
            a = n//1000
            m = n%1000
            middle = "thousand"
        return words[a] + middle + toSentence(m)

total = 0
for i in range(1,1001):
    s = toSentence(i)
    print(i,s, len(s))
    total += len(s)
print(total)
