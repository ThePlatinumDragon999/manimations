def sum_of_proper_divisors(n: int) -> int:
    total = 0

    for i in range(1, n):
        if n % i == 0:
            total += i

    return total


def aliquot_sequence(n: int, terms: int) -> list[int]:
    sequence = []

    for _ in range(terms):
        sequence.append(n)
        n = sum_of_proper_divisors(n)

    return sequence


n = int(input("Enter starting number: "))
terms = int(input("Enter number of terms: "))

sequence = aliquot_sequence(n, terms)

print(sequence)