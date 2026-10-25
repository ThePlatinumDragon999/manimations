import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from multiprocessing import Pool, cpu_count

# Check if (v, f1, f2) form a vampire number
# A vampire number is a number v that can be written as the product of
# two numbers called "fangs", f1 and f2, satisfying some conditions:
#   - v = f1 * f2
#   - v has an even number of digits, say 2n
#   - Each fang has exactly n digits
#   - The fangs' digits, taken together, are exactly the digits of v, inclusing multiplicity
#   - The fangs cannot both end in 0
#   - For example, 1260 = 21 * 60
def is_vampire(v, f1, f2):
    s_v = str(v)
    # Vampires have to be even
    if len(s_v) % 2 != 0:
        return False

    n = len(s_v) // 2

    # Make sure that each fang is n digits long
    if not (10**(n-1) <= f1 < 10**n and 10**(n-1) <= f2 < 10**n):
        return False

    # Make sure that both fangs do not end in 0
    if f1 % 10 == 0 and f2 % 10 == 0:
        return False

    # Checks to see if the fangs multiply to 0 and the digits of the fangs rearrange to the digits of v
    return (f1 * f2 == v) and (sorted(str(f1) + str(f2)) == sorted(s_v))


# Worker function for parallel processing
def process_range(args):
    f1_start, f1_end, limit = args
    found = []
    for f1 in range(f1_start, f1_end):
        for f2 in range(10, limit):
            product = f1 * f2
            if len(str(product)) % 2 != 0:
                continue
            if is_vampire(product, f1, f2):
                found.append((f1, f2))
    return found

# Find vampire pairs efficiently (parallel or single-core)
def find_vampire_pairs(limit=1000, parallel=True):
    if parallel:
        n_proc = max(1, cpu_count() - 1)
        chunk_size = limit // n_proc
        ranges = [(i, min(i + chunk_size, limit), limit) for i in range(10, limit, chunk_size)]

        with Pool(n_proc) as pool:
            results = pool.map(process_range, ranges)
        pairs = [pair for sublist in results for pair in sublist]
    else:
        pairs = []
        for f1 in range(10, limit):
            for f2 in range(10, limit):
                product = f1 * f2
                if len(str(product)) % 2 != 0:
                    continue
                if is_vampire(product, f1, f2):
                    pairs.append((f1, f2))
    return pairs

# Generate and save symmetric vampire density image
def generate_vampire_image(
    limit=1000,
    scale=20,
    parallel=True,
    background_color="#000000",
    highlight_min="#ff0000",
    highlight_max="#ffff00",
    output_path="vampire_density.png",
    dpi=300
):
    """
    Generates a high-resolution symmetric image of vampire number density.

    Parameters:
        limit: upper bound for fang values
        scale: grouping factor for fangs
        parallel: use multiprocessing
        background_color: base color for zero density
        highlight_min: color for low-density vampire regions
        highlight_max: color for high-density vampire regions
        output_path: where to save the image
        dpi: dots per inch for image quality
    """

    # Find vampire pairs
    pairs = find_vampire_pairs(limit, parallel)

    # Create grid
    grid_size = limit // scale + 1
    grid = np.zeros((grid_size, grid_size))

    for f1, f2 in pairs:
        x = f1 // scale
        y = f2 // scale
        grid[y, x] += 1
        grid[x, y] += 1  # symmetric

    # Normalize to [0,1] for color mapping
    norm_grid = grid / np.max(grid) if np.max(grid) > 0 else grid

    # Custom colormap with background → highlight_min → highlight_max
    cmap = LinearSegmentedColormap.from_list(
        "vampire_map",
        [background_color, highlight_min, highlight_max]
    )

    # Create the image (no axes, high-quality render)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=dpi)
    ax.imshow(norm_grid, cmap=cmap, origin="lower", interpolation="nearest")
    ax.axis("off")

    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"Vampire density image saved to {output_path}")

# Example usage
if __name__ == "__main__":
    limit = 100_000
    scale = 50

    generate_vampire_image(
        limit=limit,
        scale=scale,
        parallel=True,
        background_color="#000000",
        highlight_min="#aaaaaa",
        highlight_max="#ffffff",
        output_path=f"vampire_density_6_lim{limit}_scale{scale}.png",
        dpi=600
    )