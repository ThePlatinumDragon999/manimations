import numpy as np

# Define the historical benchmark data: (Year, Population, Crude Birth Rate per 1000)
# Note: For the first interval (-50000 to -8000), we use the birth rate of the target period.
intervals = [
    {
        'start_year': -50000,
        'end_year': -8000,
        'N_start': 2,
        'N_end': 5000000,
        'birth_rate_per_1000': 80,
    },
    {
        'start_year': -8000,
        'end_year': 1,
        'N_start': 5000000,
        'N_end': 300000000,
        'birth_rate_per_1000': 80,
    },
    {
        'start_year': 1,
        'end_year': 1200,
        'N_start': 300000000,
        'N_end': 450000000,
        'birth_rate_per_1000': 60,
    },
    {
        'start_year': 1200,
        'end_year': 1650,
        'N_start': 450000000,
        'N_end': 500000000,
        'birth_rate_per_1000': 60,
    },
    {
        'start_year': 1650,
        'end_year': 1750,
        'N_start': 500000000,
        'N_end': 795000000,
        'birth_rate_per_1000': 50,
    },
    {
        'start_year': 1750,
        'end_year': 1850,
        'N_start': 795000000,
        'N_end': 1265000000,
        'birth_rate_per_1000': 40,
    },
    {
        'start_year': 1850,
        'end_year': 1900,
        'N_start': 1265000000,
        'N_end': 1656000000,
        'birth_rate_per_1000': 40,
    },
    {
        'start_year': 1900,
        'end_year': 1950,
        'N_start': 1656000000,
        'N_end': 2516000000,
        'birth_rate_per_1000': 35,  # Average of 31-38 range
    },
    {
        'start_year': 1950,
        'end_year': 1995,
        'N_start': 2516000000,
        'N_end': 5760000000,
        'birth_rate_per_1000': 31,
    },
    {
        'start_year': 1995,
        'end_year': 2011,
        'N_start': 5760000000,
        'N_end': 6987000000,
        'birth_rate_per_1000': 23,
    },
]

total_births = 0

print(f"{'Interval':<20} | {'Calculated Births':<15}")
print('-' * 40)

for interval in intervals:
  a = interval['start_year']
  c = interval['end_year']
  N_a = interval['N_start']
  N_c = interval['N_end']
  b = interval['birth_rate_per_1000'] / 1000.0  # Convert to per person per year

  duration = c - a

  # Calculate net growth rate k using k = ln(Nc / Na) / (c - a)
  k = np.log(N_c / N_a) / duration

  # Calculate total births in this interval using the integral formula:
  # B = (b * N_a / k) * (exp(k * duration) - 1)
  if abs(k) < 1e-9:  # Handle edge case if growth rate is near zero
    births = b * N_a * duration
  else:
    births = (b * N_a / k) * (np.exp(k * duration) - 1)

  total_births += births
  print(f'{a} to {c:<7} | {int(births):,}')

print('-' * 40)
print(f'Total Estimated Births: {int(total_births):,}')