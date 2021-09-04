import util

def is_palindrome_num(n):
    return util.is_palindrome(str(n))

def is_palindrome_bin(n):
    return util.is_palindrome(util.dec2bin(n))

print(sum(i for i in range(1000000) if is_palindrome_num(i) and \
                                        is_palindrome_bin(i)))
