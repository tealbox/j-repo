# create a function that print top 50 prime numbers
def print_top_50_primes():
    primes = []
    num = 2
    while len(primes) < 50:
        is_prime = True
        for prime in primes:
            if prime * prime > num:
                break
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    print(primes)   


print_top_50_primes()

