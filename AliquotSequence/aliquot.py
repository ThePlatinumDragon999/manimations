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

if __name__ == "__main__":
    n = int(input("Enter starting number: "))

    seen = set()

    # Keep calculating terms in a number's aliquot sequence
    # To stop, CTRL + C in terminal
    while True:
        # Check if we've encountered this number before
        if n in seen:
            print(f"Cycle detected! {n} has appeared before.")
            break

        # Add the number to our set
        seen.add(n)
        
        print(n)
        n = sum_of_proper_divisors(n)

    print(f"Path length is {len(seen)}.")
    print(f"Max number in sequence is {max(seen)}.")