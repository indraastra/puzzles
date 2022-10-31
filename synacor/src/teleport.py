from functools import lru_cache

# a = 4
# b = 1
# Z = 1
# stack = []
# def f(l=0):
#   global a, b, stack
#   print('>'*l, a, b, stack[:10], len(stack), sum(stack))
#   if a == 0:
#     a = b + 1
#   else:
#     if b != 0:
#       stack.append(a)
#       b = b - 1
#       f(l+1)
#       print('='*(l+1), a, b, stack[:10], len(stack), sum(stack))
#       b = a
#       a = stack.pop()
#       a = a - 1
#       f(l+1)
#     else:
#       a = a - 1
#       b = Z
#       f(l+1)
#   # print('<'*l, a, b, stack[:10], len(stack), sum(stack))


# TODO: rewrite in Rust?
def g():
  for z in range(32768):
    @lru_cache(maxsize=None)
    def f(a, b):
      if a == 0:
        return (b + 1) & 0x7FFF
      elif b == 0:
        return f(a-1, z) & 0x7FFF
      else:
        return f(a - 1, f(a, b - 1)) & 0x7FFF

    print(z)
    for a in range(4):
      for b in range(32768):
        f(a, b)
    if f(4, 1) == 6:
      print('found!', z)
      break


@lru_cache(maxsize=None)
def ack15(m, n):
  print(f'ack({m}, {n})')
  if m == 0:
    return (n + 1) & 0X7FFF
  elif n == 0:
    return ack15(m - 1, 1) & 0X7FFF  # b = Z??
  # elif m == 1:
  #   return (n + 2) & 0x7FFF
  # elif m == 2:
  #   return (2*n + 3) & 0x7FFF
  # elif m == 3:
  #   return (2**(n + 3) - 3) & 0x7FFF
  else:
    return ack15(m - 1, ack15(m, n - 1)) & 0X7FFF


if __name__ == '__main__':
  # m = 2
  # for n in range(4):
  #   print(f'ack15(m={m}, n={n}) = {ack15(m, n)}')
  g()
