import numpy as np
from scipy.optimize import minimize_scalar

def fit_population(data):
    years = np.array([x[0] for x in data], dtype=float)
    populations = np.array([x[1] for x in data], dtype=float)

    # We minimize the least-squares error after taking logarithms.
    def error(t0):
        x = np.log(t0 - years)
        y = np.log(populations)

        # Fit y = b + m*x
        m, b = np.polyfit(x, y, 1)

        residuals = y - (m * x + b)

        return np.sum(residuals**2)

    # t0 must be later than every observation.
    result = minimize_scalar(
        error,
        bounds=(years.max() + 1, years.max() + 1000),
        method="bounded"
    )

    t0 = result.x

    # Do the final linear least-squares fit.
    x = np.log(t0 - years)
    y = np.log(populations)

    slope, intercept = np.polyfit(x, y, 1)

    k = -slope
    K = np.exp(intercept)

    return K, t0, k

data = [
    # (year, population)
    # First two are from Google, not the original source
    (0, 100_000_000),
    (1000, 200_000_000),
    (1650, 545_000_000),
    (1750, 694_000_000),
    (1800, 906_000_000),
    (1800, 919_000_000),
    (1800, 906_000_000), # This one is sketch (uses the 1936 edition instead of 1937 for source 21)
    (1810, 682_000_000),
    (1828, 847_000_000),
    (1845, 1_009_000_000),
    (1850, 1_171_000_000),
    (1850, 1_094_000_000),
    (1850, 1_098_000_000),  # also sketch for same reason above
    (1874, 1_391_000_000),
    (1886, 1_483_000_000),
    (1900, 1_550_000_000),
    (1920, 1_834_000_000),
    (1935, 1_995_000_000),
    (1939, 2_170_000_000),
    (1950, 2_517_000_000),
    (1950, 2_406_000_000),
]

K, t0, k = fit_population(data)

print(f"K  = {K:.3e}")
print(f"t0 = {t0:.2f}")
print(f"k  = {k:.4f}")