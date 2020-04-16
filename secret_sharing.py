"""
The following Python implementation of Shamir's Secret Sharing is
released into the Public Domain under the terms of CC0 and OWFa:
https://creativecommons.org/publicdomain/zero/1.0/
http://www.openwebfoundation.org/legal/the-owf-1-0-agreements/owfa-1-0

See the bottom few lines for usage. Tested on Python 2 and 3.
"""
from __future__ import division
from __future__ import print_function
from tkinter.filedialog import askopenfilename
import random, functools, os, re

p = [
    2,
    3,
    5,
    7,
    13,
    17,
    19,
    31,
    61,
    89,
    107,
    127,
    521,
    607,
    1279,
    2203,
    2281,
    3217,
    4253,
    4423,
    9689,
    9941,
    11213,
    19937,
    21701,
    23209,
    44497,
    86243,
    110503,
    132049,
    216091,
    756839,
    859433,
    1257787,
    1398269,
    2976221,
    3021377,
    6972593,
    13466917,
    20996011,
]
_shares = 10
_thresh_hold = 5

# Mersenne Prime
_PRIME = 0
_RINT = functools.partial(random.SystemRandom().randint, 0)


def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


def make_random_shares(minimum, shares, secret):
    """
    Generates a random shamir pool, returns the secret and the share
    points.
    """
    global _PRIME
    prime = _PRIME
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")
    poly = [_RINT(prime) for i in range(minimum - 1)]
    poly.insert(0, secret)
    points = [(i, _eval_at(poly, i, prime)) for i in range(1, shares + 1)]
    return points


def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    """Compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"

    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum

    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def recover_secret(shares):
    """
    Recover the secret from share points
    (x, y points on the polynomial).
    """
    global _PRIME
    prime = _PRIME
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    # seperat the x and y like in(1, 1494)
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)


def enc():
    global _PRIME, _thresh_hold, _shares
    filename = askopenfilename()
    fi = open(filename, "rb")
    data = fi.read()
    secret = int.from_bytes(data, "big")
    file_size = os.stat(filename).st_size
    if file_size * 8 > p[-1]:
        raise ValueError("file too big")
    if file_size * 8 in p:
        pass
    else:
        for i in p:
            if i > file_size * 8:
                file_size = i
                break
    _PRIME = 2 ** file_size - 1

    shares = make_random_shares(_thresh_hold, _shares, secret)
    try:
        path = os.path.abspath(os.getcwd())
        os.mkdir(path + "/shares")
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    for i in range(len(shares)):
        fo = open(f"shares/share_{i+1}", "wb")
        fo.write(int.to_bytes(shares[i][1], file_size, "big"))

    f2 = open(f"shares/size", "w")
    f2.write(f"{file_size}\n{os.path.basename(filename)}")


def dec():
    global _thresh_hold
    filecontent = []
    file = open("shares/size", "r")
    for line in file:
        filecontent.append(line)

    print(filecontent[1])
    file_size = int(filecontent[0])

    filename = filecontent[1]

    n_shares = _thresh_hold  # Number of files to be read
    shares = []

    for i in range(n_shares):
        with open(f"shares/share_{i+1}", "rb") as file:
            file_data = file.read()
            shares.append((i + 1, int.from_bytes(file_data, "big")))

    print("Recovering secret...")
    secret = recover_secret(shares[:_thresh_hold])
    with open(os.path.basename(filename), "wb") as file:
        file.write(int.to_bytes(secret, file_size, "big").lstrip(b"\x00"))
    print("DONE!!")


if __name__ == "__main__":
    enc()
    dec()
