import util
from tqdm import tqdm
import numpy as np

bound = 1_000_000

total = util.fast_totients(bound).sum()

print(total)
