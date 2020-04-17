print(
    f"Our function:\n\tf(x) = 1234 + 166x + 94x^2\nAnd we have this sit:\n\t[(1, 1494), (2, 1942), (3, 2578), (4, 3402), (5, 4414), (6, 4514)]\n\nIf somehow the attacker knows 2 of the shares!! it will be easy to extract the Secret\nFor example if he find out this sit:\n\t[(1, 1494), (2, 1942)]\nAnd the also the he know the public values witch is Number of shares (n=6) and how many shares he need (k=3)\n So, he knows that:\n\t1- 1494 = S + (A1)×1 + (A2)×1^2\nAND:\n\t2- 1942 = S + (A1)×2 + (A2)×2^2\nAnd if we subtract 2 from 1 we get:\n\t448 = (A1) + 3×(A2)\nFrom this formula he can find all possible values for (A1) BY:\n\tA1 = 448 - 3×(A2)"
)

result = 1
listresult = []
count = 0
while result > 0:
    result = 448 - 3 * count
    if result > 0:
        print(f"\t▬ A2 = {count} → A1 = 448 - 3 × {count} = {result}")
        listresult.append(result)
    count += 1

print(
    f"Now he replace:\n\tA1 = 448 - 3×(A2)\nin:\n\t1494 = S + (A1)×1 + (A2)×1^2\nAnd it will be like:\n\t1494 = S + (448 - 3×(A2)) + (A2)\n\t→ S = 1046 + 2(A2)\nNow he apply the results that he find in it"
)
result = 0
slist = []
for i in listresult:
    result = 1046 + 2 * i
    print(f"\t▬ A2 = {i} → S = 1046 + 2 × {i} = {result}")
    slist.append(result)

print("And so the all the possible for the Secret is:\n\t", end="")
print(slist)

print(
    f"\n\nMersenne Prime solve this problem because the main formulafor it will be:\n\tf(x) = S + (A1)x + (A2)x^2 - (Mersenne Prime) × m\n\tm element of N\nAnd finding A1 will be like:\n\tA1 = 448 - 3×(A2) - Mersenne Prime×(M1 - M2)\ninsted of:\n\tA1 = 448 - 3×(A2)"
)
