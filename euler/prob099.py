import math

def log_exp(pair):
    return pair[1] * math.log(pair[0])
        
def solve(pairs):
    solution = max(enumerate(pairs), key=lambda x: log_exp(x[1]))
    print("line", solution[0] + 1)
    pair = solution[1]
    print(pair[0], "^", pair[1])

if __name__ == "__main__":
    pairs = [l.rstrip().split(",") for l in open("base_exp.txt")]
    pairs = [(int(p[0]), int(p[1])) for p in pairs]
    solve(pairs)
