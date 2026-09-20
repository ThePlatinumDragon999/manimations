def sum_of_proper_divisors(n: int) -> int:
    if n <= 1:
        return 0

    total = 1

    i = 2

    while i * i <= n:
        if n % i == 0:
            total += i

            paired_divisor = n // i

            if paired_divisor != i:
                total += paired_divisor

        i += 1

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