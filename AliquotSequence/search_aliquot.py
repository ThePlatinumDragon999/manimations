from aliquot import sum_of_proper_divisors

target = int(input("Enter target number: "))

largest_max = 0
largest_starting_number = 0

for starting_number in range(1, target + 1):
    n = starting_number
    seen = set()
    sequence_max = starting_number

    while n not in seen and n != 0:
        seen.add(n)

        if n > sequence_max:
            sequence_max = n

        n = sum_of_proper_divisors(n)

    print(f"{starting_number}: max = {sequence_max}")

    if sequence_max > largest_max:
        largest_max = sequence_max
        largest_starting_number = starting_number

        print(
            f"  New record! "
            f"{starting_number} reaches {sequence_max}"
        )

print()
print(f"Largest maximum: {largest_max}")
print(f"Starting number: {largest_starting_number}")