#!/usr/bin/env/python3

'''
    Another sudoku solver (ASS)
    First right, then down.

    1. cross checking

    2. remove cants

    3. speculate on unresolved positions. Starting with ones with few alternatives.

    Lesson:
    Don't rely on a a nested list copy!
'''

import pprint as pp

l = 3
L = l ** 2
# SOL = [0] * L ** 2
game = \
'''
803000000
000000750
957000000
060500009
048900000
000420000
000730490
604008005
000000028
'''.replace('\n', '')


SOL = [[a[0], int(a[1])] for a in zip(*(range(L ** 2), game))]

# space = [range(1,L+1) for a in range(L**2)]
Bl = range(l)
BL = range(L)
HO = [[a * L + i for i in BL] for a in BL]
VE = [[i * L + a for i in BL] for a in BL]

# Universe, HO, VE, SQ index
Ui = [[a] + [1 for i in range(L)] for a in range(L ** 2)]
HOi = sorted([[b, HO.index(a)] for a in HO for b in a], key=lambda i: i[0])
VEi = sorted([[b, VE.index(a)] for a in VE for b in a], key=lambda i: i[0])
SQi = sorted([[a[0], int(b[1] / 3) * 3 + int(a[1] / 3)] for a in VEi for b in HOi if a[0] == b[0]], key=lambda i: i[0])

Ui = [u + [h[1], ] for u in Ui for h in HOi if u[0] == h[0]]
Ui = [u + [v[1], ] for u in Ui for v in VEi if u[0] == v[0]]
Ui = [u + [s[1], ] for u in Ui for s in SQi if u[0] == s[0]]


def reset_li(u_, vals):
    """

    :type u: list
    """
    for i in vals:
        u_[i] = 0
    return u_


def solve_pos(u_, pos, val):
    h, v, s = u_[pos][L + 1:L + 4]
    u_ = [reset_li(r, range(1, 10)) if r[0] == pos else r for r in u_]
    u_ = [reset_li(r, [val]) if r[L + 1] == h else r for r in u_]
    u_ = [reset_li(r, [val]) if r[L + 2] == v else r for r in u_]
    u_ = [reset_li(r, [val]) if r[L + 3] == s else r for r in u_]
    return u_


def solve_simple(u_):
    '''
    :param u_: universe list
    :return: universe list
    '''
    res = set()
    remain = {'H': [], 'V': [], 'S': []}
    r = None
    for lvl in range(L):
        for v in [1, 2, 3]:
            r = [a for a in u_ if a[L + v] == lvl]
            for i in range(1, L + 1):
                x = [[a[0], i] for a in r if a[i] == 1]
                if len(x) == 1:
                    res.add(tuple(x[0]))
                elif len(x) > 1:
                    remain['H' if v == 1 else 'V' if v == 2 else 'S'].append(x)
    return res, remain


def prepare_universe(u_, sol_):
    for pos, val in sol_:
        if val != 0:
            u_ = solve_pos(u_, pos, val)
    return u_


def remove_cants(u_, alist):
    if len(alist) > 3:
        # all cannot be inline
        return
    pos, val = zip(*alist)
    hh, vv, ss = zip(*[[a[L + 1], a[L + 2], a[L + 3]] for a in u_ if a[0] in pos])

    if len(set(hh)) == 1:
        u_ = [reset_li(r, list(val)) if r[L + 1] == hh[0] else r for r in u_ if r[L + 3] != ss[0]]
    elif len(set(vv)) == 1:
        u_ = [reset_li(r, list(val)) if r[L + 2] == vv[0] else r for r in u_ if r[L + 3] != ss[0]]


def try_solve(u_, sol_):
    counter_ = 20
    while counter_ > 0:
        prepare_universe(u_, sol_)
        sol_set_, t = solve_simple(u_)

        for maybes in t['S']:
            remove_cants(u_, maybes)

        if len(sol_set_) == 0:
            return u_, t, sol_

        for s in sol_set_:
            sol_[s[0]] = [s[0], s[1]]

        counter_ -= 1
        if counter_ <= 0:
            break


# caveat! 
# There is an issue with the script not working correctly if the 
# Ui list has been altered.
Ui_copy = [a.copy() for a in Ui]

candidate, sol_space, sol_x = try_solve(Ui_copy, SOL.copy())
snap_ui1 = candidate.copy()
snap_sol1 = sol_space.copy()
sol_sol1 = sol_x.copy()

Ui_copy = [a.copy() for a in Ui]

solutions = []
cc = 20
for temp in sorted(sol_space['S'], key=lambda i: len(i)):
    for tt in temp:
        Ui_ = [a.copy() for a in Ui_copy]
        sol_ = [[tt[0], tt[1]] if a[0] == tt[0] else a for a in SOL.copy()]

        ssu, ssol, solol = try_solve(Ui_, sol_)

        if '0' not in ''.join([str(a[1]) for a in solol]):
            solutions.append(''.join([str(a[1]) for a in solol]))

        cc -= 1
    if cc < 0:
        break


print()
solutions = set(solutions)
pp.pprint(solutions)
