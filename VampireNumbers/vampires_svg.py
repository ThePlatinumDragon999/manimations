import numpy as np
from functools import lru_cache
from multiprocessing import Pool, cpu_count
from matplotlib.colors import LinearSegmentedColormap, to_hex

# This script finds vampire numbers and draws a picture of where their "fangs" fall

# A vampire number is a number with an even number of digits (2n) that equals the product of 
# two n-digit numbers (the fangs). The digits of the product must be exactly the digits of the two fangs
# combined, in some order. The fangs can't both end in 0.

# The naive approach (and my original approach lol) is to try every pair of n-digit numbers, multiply
# them, and compare digits. For 5-digit fangs, that's billions of pairs, which is far too slow.
# In my unoptimized code, running this would take a few hours.

# But below is code that I have tried my hardest to optimize. I did make the mistake of writing this in Python,
# so the runtime is a few seconds rather than the milliseconds I could likely get by writing this in C or assembly.

# -----------------------------------------------------------------------------------------------------------

# The hard part is checking "do these two fangs and this product use the same digits?"
# Sorting digit strings for billions of pairs would be slow.
# Instead, the script turns each number's digit multiset into a single integer, called the signature.

# np.arange(10, dtype=np.int64) gives a numpy array [0, 1, ..., 9], so _W is [16^0, 16^1, etc.]
# These are the "weights" for the digits 0 through 9.

# The signature of a number is the sum of 16^d over each digit d in it. The best way to think of this is as
# a row of 10 buckets, one per digit. Each time you see a digit, you can drop a marble into its corresponding
# bucket. Writing the marble counts as one number in base 16 gives you the signature.

# For example, 1260 (the smallest vampire number) with digits 1, 2, 6, 0, would have a signature of:
# 16^1 + 16^2 + 16^6 + 16^0 = 16 + 256 + 16,777,216 + 1 = 16,777,489

# The fangs 21 and 60 have signatures
# sig(21) = 16^2 + 16^1 = 272, sig(60) = 16^6 + 16^0 = 16,777,217, and the sum is 16,777,489, identical
# to sig(1260)

# You may wonder why we are using base 16 and not base 10. The reason is that each bucket holds a count. If a count
# could reach 10 or more, it would "carry" over into the neighboring bucket in base 10 and corrupt the result.
# In base 16, a bucket can hold up to 15 before overflowing, and the vampire numbers never get near that 
# (since both fangs are less than 10^5 (100k), and thus vampire numbers are less than 10^10,
# which means any one digit can appear only 10 times)

# This guarantee is tied to the current limit of 100k. 
# Counts stay under 16 only up to 7-digit fangs (14-digit products). 
# At 8-digit fangs a digit could appear 16 times and corrupt the signature. So this code works for a limit <= 10^7

# So two numbers have the same signature exactly when they have the same digit multiset. 
# The signature is also additive: the signature of both fangs together is sig(f1) + sig(f2), 
# because marbles from two piles just add. That’s why the final test can be sig(product) == sig(f1) + sig(f2).
# Why 16 specifically? Any base above the max count works. 16 is a nice choice for computers because it’s a power of 2.

# As a final note, you may wonder why doing a signature is faster.
# It's because I replace sorting digits with one integer comparison, and even then, the values are precomputed.

# Even with all of these optimizations though, this code still takes a few seconds to run.
# A compiled language would likely be several times faster, but I really really didn't want to have to mess
# with SVG stuff in C or Assembly
_W = 16 ** np.arange(10, dtype=np.int64)

# This is a lookup table for what I call the mod-9 trick. This will be explained a bit later.
_INV9 = {1: 1, 2: 5, 4: 7, 5: 2, 7: 4, 8: 8}

# The @lru_cache is a decorator: it wraps the function so that calling _sig_table(1000000) a second time
# returns the stored answer immediately. maxsize=None means "remember everything"
@lru_cache(maxsize=None)
def _sig_table(size):
    """sig[x] for every integer 0 <= x < size, built block by block."""
    # This makes an array of size that are all zeroes.
    # sig[x] will hold the signature of the number x. int64 means 64-bit integers, which are big enough
    # that nothing overflows.
    sig = np.zeros(size, dtype=np.int64)
    # For single-digit numbers 0 through 9, the signature is just that digit's weight. sig[3] = 16^3, and so on.
    sig[:10] = _W

    # This fills in the signatures in sig by working in blocks: First all 2-digit numbers (10 to 99), 
    # which depend only on 1-digit numbers; then 3-digit numbers (100 to 999), which depend on the 2-digit ones; 
    # and so on.
    # This table lets us look up a fang’s signature instantly, sig[f1], instead of recomputing it.
    lo = 10
    while lo < size:
        # min(lo*10, size) stops the last block at the table’s end.
        hi = min(lo * 10, size)
        # Creates an np array [lo, lo+1, ..., hi-1]. np arrays are nice since you can do per-element operations.
        # Thus, each block is done in one vectorized step, with no per-number Python loop.
        idx = np.arange(lo, hi)
        # This uses the observation that a number's digits are "all but the last digit" plus "the last digit"
        # So for example, sig[472] = sig[47] + _W[2]. The signature of 47 was already computed, so we just add
        # one weight.
        # idx // 10 is integer division, which chops off the last digit, and idx % 10 is the remainder,
        # which is the last digit.
        sig[lo:hi] = sig[idx // 10] + _W[idx % 10]
        lo *= 10
    return sig

# args is one tuple so the function can be handed to Pool.map (it passes one argument per job). It means:
# "find fangs with n digits, trying f1 values start, start+step, start+2*step, ... < stop, with f2 allowed
# up to f_max (exclusive)"
def _search(args):
    """Find vampire fang pairs with f1 in range(start, stop, step), n digits each."""
    n, start, stop, step, f_max = args
    sig = _sig_table(f_max)
    # lo_prod is the smallest 2n-digit number (for n=2 it's 1000). Products must be at least this big.
    lo_prod = 10 ** (2 * n - 1)
    # This collects the results
    out = []

    # This loops over every candidate first fang
    for f1 in range(start, stop, step):
        # So this is some clever math I call the mod 9 trick (and where the _INV9 lookup table from above) comes
        # into play.

        # So a bit of background about "casting out nines": Any number leaves the same remainder when divided by
        # 9 as its digit sum does. For example, 472 has digit sum 13, and 13 has digit sum 4, and 472 = 9*52 + 4

        # The product v = f1 * f2 has the same digits as the two fangs together. So the digit sum of v equals
        # the digit sum of f1 plus the digit sum of f2. Taking everything mod 9, we have
        # f1 * f2 ≡ f1 + f2      (mod 9)
        # Move everything to one side and add 1 to both sides:
        # f1 * f2 - f1 - f2 + 1 ≡ 1      (mod 9)
        # (f1 - 1)(f2 - 1) ≡ 1      (mod 9)
        # So (f1-1) and (f2-1) must multiply to something with remainder 1 mod 9
        # This makes them modular inverses of each other. For example, 2 * 5 = 10, which has remainder 1, so 2
        # and 5 are inverses mod 9

        # This is much nicer computationally than just multiplying the numbers out and doing checks.

        # This is the remainder of f1-1
        r = (f1 - 1) % 9

        # Not every number has an inverse. If r is 0, 3 or 6 (multiples of 3), then r times anything
        # is a multiple of 3, and can never leave remainder 1. So if r % 3 == 0, continue skips those f1
        # values entirely. This throws away one third of all f1 values for free.
        if r % 3 == 0:
            continue
        # For the rest, _INV9 gives the inverses: {1:1, 2:5, 4:7, 5:2, 7:4, 8:8}
        # And you can check it yourself. 4 * 7 = 28 = 3 * 9 + 1, and 8 * 8 = 64 = 7 * 9 + 1

        # res is the required remainder of f2 itself (since f2-1 ≡ inverse, f2 ≡ inverse + 1)
        # This gives quite a nice payoff. For a given f1, only 1 in 9 values of f2 can possibly work.
        # Combined with skipping a third of the f1 values, and that is roughly 13.5 times fewer pairs to 
        # test (9 / (2/3)), and is mathematically guaranteed not to miss any real vampire numbers.
        res = (1 + _INV9[r]) % 9

        # First, we need to pick where f2 starts.
        # We want f2 >= f1 since we want each unordered pair once. The image function adds the mirror pairs
        # back later.
        # -(-lo_prod // f1) is a Python trick for ceiling division. // rounds down, so negating, dividing, and
        # negating again rounds up. This gives the smallest f2 for which f1 * f2 >= lo_prod (i.e. the product
        # has the full 2n digits).
        f2_start = max(f1, -(-lo_prod // f1))
        # This second line nudges f2_start up to the nearest number with remainder res mod 9.
        # In Python, % of a negative number is still non-negative, so (res - f2_start) % is exactly how
        # far to step forward.
        f2_start += (res - f2_start) % 9
        # If we've overshot the top of the range, there's nothing left to test for this f1
        if f2_start >= f_max:
            continue

        # Once we have a start for f2, we can make a numpy array so we can again do vectorized operations.
        # Since f2 starts on the correct remainder, we can step by 9.
        f2 = np.arange(f2_start, f_max, 9, dtype=np.int64)
        # This enforces the rule “fangs can’t both end in 0.” If f1 ends in 0, drop any f2 that does too. 
        # f2[mask] keeps only entries where the mask is True. If nothing is left, move on.
        if f1 % 10 == 0:
            f2 = f2[f2 % 10 != 0]
        if f2.size == 0:
            continue

        # This is the digit check.
        # v is an array of all the products at once (one f1 times a whole array of f2).
        # Products can be huge (up to about 10^10 here) which is too much for a lookup table. So instead,
        # we compute their signatures directly.
        # Peel off the last digit with %10, look up its weight with _W[...] (indexing with an array) looks
        # up every entry at once), add it, then drop that digit with //= 10. We repeat exactly 2n times because
        # every product has exactly 2n digits, so no leading zeroes get miscounted.
        v = f1 * f2
        sig_v = np.zeros_like(v)
        t = v.copy()
        for _ in range(2 * n):
            sig_v += _W[t % 10]
            t //= 10

        # This is the key comparison. sig_v == sig[f1] + sig[f2] compares for all candidates at once, giving
        # True/False per entry. sig[f1] is a single number and sig[f2] looks up each candidate's
        # signature from the table. f2[...] keeps only the f2 values where the digits match. 
        # Each hit is stored as the pair (f1, f2). int(b) converts numpy’s integer type into a plain Python int.
        hits = f2[sig_v == sig[f1] + sig[f2]]
        out.extend((f1, int(b)) for b in hits)

    return out

# This function orchestrates the whole search with parallelization.
def find_vampire_pairs(limit=1000, parallel=True):
    """
    Return an (m, 2) int64 array of unordered fang pairs (f1 <= f2), with
    every fang < limit. Covers every digit length n >= 2 that fits under limit.
    """
    # Build the big signature table once up front. On systems that "fork" worker processes (such as Linux), the
    # workers inherit it for free instead of rebuilding it.
    _sig_table(limit)

    jobs = []
    # Use all cores but one (leave one for your system), or just 1 if parallel is off.
    n_proc = max(1, cpu_count() - 1) if parallel else 1
    # n_strides is the number of slices to cut each digit_length's work into.
    n_strides = n_proc * 4

    # It starts at n = 2. One-digit fangs would give 2-digit products, and no vampire numbers exist there
    # (the smallest is 1260)
    n = 2
    # For each digit length, lo...hi is the range of n-digit numbers (2-digit: 10 to (not including) 100, and 
    # so on), capped at limit.
    # Each digit length is split into n_strides jobs. Job k handles f1 = lo+k, lo_k_n_strides, lo+k+2*n_strides, ...
    # It's an interleaved split, like dealing cards, rather than giving job 0 to the first chunk.
    # The reason I interleave is that work per f1 isn't constant. Small f1 values have more f2 candidates to test,
    # so a contiguous split would give one worker much more work than another. "Dealing cards" gives every
    # job a similar mix of cheap and expensive f1's.
    while 10 ** (n - 1) < limit:
        lo, hi = 10 ** (n - 1), min(10 ** n, limit)
        for k in range(n_strides):
            jobs.append((n, lo + k, hi, n_strides, hi))
        n += 1

    # Pool.map hands the jobs out to the workers and collects the results. 
    # chunksize=1 means workers grab one job at a time as they become free, so a worker that finishes early 
    # just takes another. Having 4× more jobs than workers smooths out any remaining imbalance. 
    # The with block cleans up the workers afterward.
    if parallel and n_proc > 1:
        with Pool(n_proc) as pool:
            results = pool.map(_search, jobs, chunksize=1)
    else:
        results = map(_search, jobs)

    # This flattens the list of lists, sorts it, and makes an array with 2 columns 
    # (-1 means “figure out the number of rows”). 
    # The reshape ensures you still get a proper 0-row, 2-column array if nothing was found.
    pairs = [p for chunk in results for p in chunk]
    return np.array(sorted(pairs), dtype=np.int64).reshape(-1, 2)

# This makes the image
def generate_vampire_image(
    limit,
    scale,
    parallel,
    background_color,
    highlight_min,
    highlight_max,
    output_path,
    gamma=1.0,
):
    """
    Write a symmetric vampire-fang density map as an SVG.

    Cell (x, y) counts ordered fang pairs (f1, f2) with f1 // scale == x and
    f2 // scale == y. Empty cells show background_color; nonzero cells are
    colored from highlight_min (sparsest) to highlight_max (densest).
    gamma < 1 brightens sparse regions if the density is heavy-tailed.
    """
    pairs = find_vampire_pairs(limit, parallel)

    # The search only kept pairs with f1 ≤ f2. For a symmetric picture we need both (21, 60) and (60, 21)
    # pairs[:, 0] != pairs[:, 1]. A pair like (x, x) mirrors onto itself, and adding it twice would double count it.
    # [:, ::-1] reverses the column order, swapping f1 and f2. I love Python slicing.
    swapped = pairs[pairs[:, 0] != pairs[:, 1]][:, ::-1]
    # vstack stacks the originals and the swapped copies.
    ordered = np.vstack([pairs, swapped])

    # Imagine a square grid where each pixel covers a scale × scale block of (f1, f2) values. 
    # With scale=50 and limit=100000, that’s a 2001 × 2001 picture.
    # // scale converts a fang value into a pixel coordinate.
    size = limit // scale + 1
    # row * size + col converts a 2D position into one flat index.
    cells = (ordered[:, 1] // scale) * size + (ordered[:, 0] // scale)
    # np.bincount counts how many times each flat index appears, i.e. how many vampire pairs land in each pixel.
    # reshape(size, size) turns it back into a 2D grid, so grid[y, x] = number of pairs in that pixel. 
    # Because we added the mirrored pairs, grid[y,x] == grid[x,y]
    grid = np.bincount(cells, minlength=size * size).reshape(size, size)

    # Build a gradient from highlight_min to highlight_max, then pre-compute 256 hex color strings along it 
    # (a lookup table called lut). That’s far faster than converting a color for every pixel.
    cmap = LinearSegmentedColormap.from_list("vampire", [highlight_min, highlight_max])
    lut = [to_hex(cmap(i / 255)) for i in range(256)]

    # This turns counts into a color index from 0 to 255. grid / grid.max() rescales so the densest pixel is 1.0
    # ** gamma is a curve. With gamma=1, it does nothing. With gamma < 1 (like 0.5), small values get boosted, so 
    # sparse regions are easier to see.
    # Then you multiply by 255, round, and make it an integer.
    # The if grid.max() else grid guards against dividing by zero if no pairs were found.
    levels = np.rint(255 * (grid / grid.max()) ** gamma).astype(int) if grid.max() else grid

    # An SVG is a text file of drawing instructions. 
    # This writes the header: a canvas of size × size units (one unit per grid cell) with crispEdges so there’s 
    # no blurry anti-aliasing between neighboring pixels. Then it draws one big background-colored rectangle.
    with open(output_path, "w", encoding="utf-8") as svg:
        svg.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}" shape-rendering="crispEdges">\n'
            f'<rect width="{size}" height="{size}" fill="{background_color}"/>\n'
        )

        # For each row, xs is the list of columns with non-zero counts. 
        # Empty rows are skipped, and empty cells stay background-colored since we never draw them. 
        # lv is the color level of each non-empty cell.
        for y in range(size):
            xs = np.nonzero(grid[y])[0]
            if xs.size == 0:
                continue
            lv = levels[y, xs]

            # This is a file size optimization. Instead of one <rect> per pixel, it merges neighboring pixels 
            # with the same color into one wide rectangle (“run-length encoding”).
            # np.diff(xs) gives gaps between consecutive columns. A gap != 1 means a hole.
            # np.diff(lv) != 0 means the color changed.
            # Either one starts a new run. The + 1 is because diff entry i compares positions i and i+1, 
            # so the new run starts at i+1. np.split cuts the arrays at those break points.
            breaks = np.nonzero((np.diff(xs) != 1) | (np.diff(lv) != 0))[0] + 1
            for seg_x, seg_lv in zip(np.split(xs, breaks), np.split(lv, breaks)):
                # Write one rectangle per run. x is the run’s first column, width its length. 
                # size - 1 - y flips the vertical axis: SVG’s y=0 is the top, but graphs conventionally 
                # have the origin at the bottom-left. The fill color comes from the lookup table.
                svg.write(
                    f'<rect x="{seg_x[0]}" y="{size - 1 - y}" '
                    f'width="{len(seg_x)}" height="1" fill="{lut[seg_lv[0]]}"/>\n'
                )

        # Close the SVG
        svg.write("</svg>\n")

    print(f"{len(pairs)} fang pairs found; SVG saved to {output_path}")

# This code only runs when you execute the file directly, not when it’s imported. 
# It’s also required for multiprocessing on Windows and macOS: those systems launch each worker by 
# re-importing your file, and without the guard every worker would start its own workers.
if __name__ == "__main__":
    limit = 100_000
    scale = 50

    generate_vampire_image(
        limit=limit,
        scale=scale,
        parallel=True,
        background_color="#000000",
        highlight_min="#1D243C",
        highlight_max="#9ab5ff",
        output_path=f"graphs/vampire_density_blue_lim{limit}_scale{scale}.svg",
    )