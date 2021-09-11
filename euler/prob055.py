import util

_lychrels = {}
def is_lychrel(n, iteration):
    # consider it lychrel if it's the 50th iteration
    if iteration >= 50:
        _lychrels[n] = True
    # if it's a palindrome and it's the sum of another number and its reverse,
    # return False
    elif iteration > 0 and util.is_palindrome(str(n)):
        _lychrels[n] = False
    # if we already know this to be a lychrel number, we return True
    elif _lychrels.get(n):
        pass
    # otherwise, we have no idea yet
    else:
        # let's try this again
        _lychrels[n] = is_lychrel(n + int(str(n)[::-1]), iteration + 1)
    return _lychrels[n]

def solve():
    count = 0
    for n in range(9999, 0, -1):
        if is_lychrel(n, 0):
            count += 1
            #print n, "is lychrel"
    print(count, "total lychrels")

if __name__ == "__main__":
    solve()
    #pass
