palindromes = []

def ispalindrome(n):
    s = str(n) 
    return s == s[::-1]

for i in range(999,100,-1):
    for j in range(999,100,-1):
        if ispalindrome(i*j):
            palindromes.append((i*j,i,j))

print max(palindromes, key=lambda x: x[0])
