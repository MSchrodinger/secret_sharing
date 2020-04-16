def PI(vals):
    accum = 1
    for v in vals:
        accum *= v
    return accum


def _extended_gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    i = 1
    print(
        f"\n--------------------------\ninside _extended_gcd()\n--------------------------"
    )
    print(
        f"start: quot = {0}, a = {a}, b = {b}, x = {x}, y = {y}, last_x = {last_x}, last_y = {last_y}"
    )
    while b != 0:
        # Floor division - division that results into whole number adjusted to the left in the number line
        # 10/4=2,5 <----normal division
        # 10//4=2 <----floor division
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
        print(
            f"{i}    : quot = {quot}, a = {a}, b = {b}, x = {x}, y = {y}, last_x = {last_x}, last_y = {last_y}"
        )
        i += 1
    print(
        f"Coefficient for smaller integer = {last_x}\nCoefficient for bigger integer = {last_y}"
    )
    return last_x, last_y


def test_gcd():
    # First, find the gcd(34, 19).
    # 34 = 19(1) + 15.
    # 19 = 15(1) + 4.
    # 15 = 4(3) + 3.
    # 4 = 3(1) + 1.
    # 3 = 1(3) + 0.
    # Thus, the gcd(34, 19) = 1.

    # Next, work backwards to find x and y.
    # 1 = 4 - 1(3).
    # = 4 - 1(15 - 4(3)) = 4(4) - 1(15).
    # = 4(19 - 15(1)) -1(15) = 4(19) - 5(15).
    # = 4(19) - 5(34 - 19(1)) = 9(19) - 5(34).

    # Thus Bezout's Identity for a=34 and b=19 is 1 = 34(-5) + 19(9).
    a = 34
    b = 19
    c, d = _extended_gcd(a, b)
    print(c)
    print(d)
    # we take the Coefficient for smaller integer in our case not the Greatest Common Divisor


def _divmod(num, den, p):
    inv, _ = _extended_gcd(den, p)
    print(f"\n--------------------------\ninside _divmod()\n--------------------------")
    print(
        f"value from _extended_gcd(): {inv}\nreturn value from _divmod(): {num} * {inv} = {num*inv}"
    )
    return num * inv


def _lagrange_interpolate():
    nums = []
    dens = []
    print(
        f"--------------------------\nOUR EXAMPLE\nthis is our sheres:\n[(1, 1494), (2, 1942), (3, 2578), (4, 3402), (5, 4414), (6, 4514)] we pick D1, D3 and D4\n--------------------------\n"
    )
    list1 = [(1, 1494), (3, 2578), (4, 3402)]
    # [(1, 1494), (2, 1942), (3, 2578), (4, 3402), (5, 4414), (6, 4514)]

    x = 0
    x_s, y_s = zip(*list1)
    print(f"--------------------------\nWhat zip do!!\n--------------------------")
    print(x_s)
    print(y_s)
    k = len(x_s)
    # the mersin prime must be more than the secret
    p = 2 ** 13 - 1

    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    print(
        f"\n--------------------------\nFIRST section of _lagrange_interpolate!!\n--------------------------"
    )
    print(
        f"LOOP → [1, 2, 3] pop 1 → [2, 3] then [0-2, 0-3] then call PI() and so on.\nThe output will be: {nums} "
    )
    print(
        f"\nLOOP → [1, 2, 3] pop 1 → [2, 3] then [1-2, 1-3] then call PI() and so on.\nThe output will be: {dens} "
    )

    print(
        f"\n--------------------------\nSECOND section of _lagrange_interpolate!!\n--------------------------"
    )
    den = PI(dens)
    print(f"call PI({dens}) → {den}")

    print(
        f"\n--------------------------\nTHEARD section of _lagrange_interpolate!!\n--------------------------"
    )
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])
    print(
        f"sum of multiplycation of (Each number in {nums} * {den} * maped with {list(y_s)} % {p})\nwith the inverse of (Each {p} with {dens}).\n OUTPUT: {num} "
    )
    print(
        f"\n--------------------------\nLAST section of _lagrange_interpolate!!\n--------------------------"
    )
    s = _divmod(num, den, p)
    secret = (s + p) % p
    print(
        f"\nFinally the secret is: (_divmod(num, den, p) + p) % p = {s} + {p} % {p} = {secret}\n "
    )


# test_gcd()
_lagrange_interpolate()
