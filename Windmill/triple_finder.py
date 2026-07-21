# This program loops through pseudo-Pythagorean triples (x, y, z) such that
# x^2 + 4yz = a prime of the form 4k + 1 (the prime is passed as a paramter)

# It then applies the Zagier involution to each triple, and sorts them into a dictionary
# by the case that each triple falls into.

# It prints all of the Pythagorean triples used, then prints the result of
# applying the Zagier involution, including the case, and what the image of each
# triple goes to.

# Used for proving Fermat's two squares theorem, as Zagier showed that if there is a
# fixed point in the involution (aka one of the triples maps to itself), 
# then a prime of the form 4k + 1 can be written as the sum of two squares.

from numpy import sqrt
import math
from collections import defaultdict

# List of all pseudo-Pythagorean triples that the Zagier involution will be applied to
triple_list = []

# A dictionary that maps Zagier involution cases to a list of triples that fall into
# that case
grouped = defaultdict(list)

 # Paramter prime of form 4k+1
prime = 61

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

# If y or z = 0, then the maximum value of x is sqrt(p)
for x in range(int(sqrt(prime))+1):
    # If x is 0 and z is 1, then the maximum value of y is p / 4
    for y in range(math.floor(prime/4) + 1):
        # If x is 0 and z is 1, then the maximum value of y is p / 4
        for z in range(math.floor(prime/4) + 1):
            # Iterate over all reasonable combinations of x, y, z
            # Append only if x^2 + 4yz is equal to the parameter prime
            if x**2 + 4*y*z == prime:
                triple_list.append((x, y, z))

# Print out the pseudo Pythagorean triples found
print(f"Pythagorean triples (x, y, z) such that x^2 + 4yz = {prime}:")
for triple in triple_list:
    print(triple)

print(f"\nNumber of triples found: {len(triple_list)}")

print("\nZagier involution images of the triples:")
for triple in triple_list:
    # case refers to the string in the Zagier involution function indicating the case
    # such as "x < y - z"

    # image is the resulting (x, y, z) triple from applying the Zagier involution
    case, image = zagier_involution(*triple)

    # For each case, add all Pythagorean triples that as input go to that case
    # as well as their image
    grouped[case].append((triple, image))

# Iterate over each case
# Print the input triple and the image (result)
for case, entries in grouped.items():
    print(f"\nCase: {case}")
    for triple, image in entries:
        print(f"  Triple: {triple} -> Image: {image}")