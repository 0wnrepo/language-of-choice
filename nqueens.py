"""
The N-queens problem as a BDD.
"""

import dd
from functools import reduce
import sys
import time

## queens(2)
#. none
## queens(4)
#. . . Q .
#. Q . . .
#. . . . Q
#. . Q . .

def queens(n):
    before = time.time()
    problem = queens_problem(n)
    print(len(dd.build_node._memos))
    print("made bdd in {}s".format(time.time() - before))
    env = dd.satisfy(problem, 1)
    if env is None:
        print( 'none')
    else:
        show_board(n, env)

def show_board(n, env):
    for row in make_board(n):
        for var in row:
            sys.stdout.write('.Q'[env[var]])
        sys.stdout.write('\n')

def queens_problem(n):
    return conjoin(disjoin(place_queen(n, r, c) for c in range(n))
                   for r in range(n))

def conjoin(nodes): return reduce(lambda x, y: x & y, nodes)
def disjoin(nodes): return reduce(lambda x, y: x | y, nodes)

def place_queen(n, r, c):
    env = {}
    def exclude(rr, cc):
        if 0 <= rr < n and 0 <= cc < n:
            env[queen(n, rr, cc)] = False
    for cc in range(n): exclude(r, cc)
    for rr in range(n): exclude(rr, c)
    for dd in range(-n+1, n):
        exclude(r+dd, c+dd)
        exclude(r+dd, c-dd)
        exclude(r-dd, c+dd)
        exclude(r-dd, c-dd)
    env[queen(n, r, c)] = True
    return match(env)

def match(env):
    """Return a BDD that evaluates to 1 just when every variable
    in env has its given value."""
    tree = dd.lit1
    for var, value in sorted(env.items(), reverse=True):
        v = dd.Variable(var)
        tree = v(dd.lit0, tree) if value else v(tree, dd.lit0)
    return tree

def queen(n, r, c):
    "The variable for a queen at (row r, column c) in an n*n board."
    return 1 + n*r + c

def make_board(n):
    """Return a 2-d array of distinct variables: each means there's a
    queen at its position."""
    return [range(1+r*n, 1+(r+1)*n) for r in range(n)]


if __name__ == '__main__':
    from sys import argv as args
    if len(args) == 2:
        queens(int(args[1]))
    else:
        print('Usage: %s board-size' % args[0])
