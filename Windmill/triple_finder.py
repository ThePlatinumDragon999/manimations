from numpy import sqrt
import math
from collections import defaultdict

triple_list = []

grouped = defaultdict(list)

prime = 61  # prime of form 4k+1

# Return the Zagier involution of (x, y, z)
def zagier_involution(x, y, z):
    if x < y - z:
        return (
            "x < y - z",
            (x + 2*z, z, y - x - z)
        )
    elif y - z <= x <= 2*y:
        return (
            "y - z ≤ x ≤ 2y",
            (2*y - x, y, x - y + z)
        )
    else:
        return (
            "x > 2y",
            (x - 2*y, x - y + z, y)
        )

# Find all integer triples (x, y, z) such that x^2 + 4yz = p
for x in range(int(sqrt(prime))+1):
    for y in range(math.floor(prime/4) + 1):
        for z in range(math.floor(prime/4) + 1):
            if x**2 + 4*y*z == prime:
                triple_list.append((x, y, z))

print(f"Pythagorean triples (x, y, z) such that x^2 + 4yz = {prime}:")
for triple in triple_list:
    print(triple)

print(f"\nNumber of triples found: {len(triple_list)}")

print("\nZagier involution images of the triples:")
for triple in triple_list:
    case, image = zagier_involution(*triple)
    grouped[case].append(triple)

for case, triples in grouped.items():
    print(f"\nCase: {case}")
    for triple in triples:
        image = zagier_involution(*triple)[1]
        print(f"  Triple: {triple} -> Image: {image}")