import psyco
import util

def is_sequence(seq):
    return seq == range(seq[0], seq[-1]+1)

if __name__ == "__main__":
    last_four = []
    for i in range(100000, 200000):
        prime_factors = list(util.prime_factors_alt(i))
        if len(set(prime_factors)) == 4:
            if len(last_four) < 4:
                last_four.append(i)
            else:
                del last_four[0]
                last_four.append(i)
            if len(last_four) == 4 and is_sequence(last_four):
                print "FOUND!"
                break
    print last_four
