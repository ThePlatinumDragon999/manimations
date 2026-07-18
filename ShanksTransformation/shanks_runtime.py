import math
prev_sum = 0
sum = 1
next_sum = 2/3
shanks = 0
for x in range(2, 10):
    prev_sum = sum
    sum = next_sum
    next_sum += ((-1)**x)/(2*x + 1)
    shanks = (prev_sum*next_sum-sum**2)/(next_sum-2*sum+prev_sum)
    print("Regular: {:.30f}     Shanks: {:.30f}".format(abs(4*sum - math.pi), abs(4*shanks - math.pi)))

