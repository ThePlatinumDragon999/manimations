from manim import *
import numpy as np

# So this was hell to make working right.
# But it works.

class PopulationTree(MovingCameraScene):
    def construct(self):
        # Config
        # Cat height is the height of every cat. It's measured in Manim world units.
        # Default Manim settings are about 14.22 units wide and 8 units tall (16:9), and 0.6
        # height of the cat's drawing, from the top of its ears to bottom of face
        cat_height = 0.6

        # This is the minimum center-to-center distance between two cats.
        # This is a hard rule; aka never relaxed. If no spot satisfies it, the branch ends instead
        min_dist = 0.6

        # The minimum gap between a cat's center and any line that isn't its own.
        # It is used in two directions: A candate line must stay line_clear away from every existing cat
        # (except its own parent), and a candidate cat must stay line_clear away from every existing line
        line_clear = 0.4

        # The shortest allowed parent to child distance in the layout, and the starting radius of the search
        # for each cat.
        # Raising it spreads the tree out and makes lines longer. Lowering it makes the tree tighter
        edge_min = 1.05

        # This does two jobs: It gives a random radius jitter (since each attempt uses r + uniform(0, edge_step),
        # so neighbors don't all sit at identical distances. It also does search growth; When all 20 atempts
        # at one radius fail, r grows by edge_step.
        edge_step = 0.12

        # The angle, in degrees, by which the first generation's children deviate from their parent's direction.
        # The root points straight down (-90), and the first-generation cats therefore point at about -168 and -12
        # These are almost horizontal, near the 180 and 0 of left and right.
        first_spread = 78

        # Each generation's spread is first_spread * 0.75^{g-1}
        # Because directions are inherited (a child's direction is its parent's plus or minus the spread),
        # the tree starts out fanned wide and then straightens, which is why later branches look more fractal like.
        spread_decay = 0.75

        # Randomness on the spread. The angle used is spread × (1 + 0.3 × uniform(−1, 1)), so between 
        # 70% and 130% of the nominal value. 0 gives perfectly regular geometry. 
        # Higher values give a more organic tree.
        spread_jitter = 0.3

        # The depth at which the camera begins scrolling down. Smaller values start the scroll earlier. 
        # Larger values leave the tree centred longer, so more of the tree is visible before it moves.
        scroll_start = 3

        # World units the camera moves down per generation of growth
        scroll_speed = 0.7

        # Animation seconds per unit of depth. The total run_time is seconds_per_level × (end_depth + 1)
        seconds_per_level = 0.7

        # How much longer the animation runs after the root has completely left the top of the screen. 
        # It is converted into depth
        tail_seconds = 3.0

        # The frame width as a multiple of the screen width, at the start and at the end. 
        # The width grows linearly over the whole animation.
        zoom_start = 0.4
        zoom_end = 1.2

        # The maximum number of generations. If the camera needs more generations than this, the bottom of 
        # the tree would be empty. Most deep generations are skipped anyway because the visibility test 
        # discards cats that are never on screen.
        G_cap = 10

        # The largest search radius a cat will try. Beyond 8 units, the cat gives up and the branch ends (skipped). 
        # In practice you rarely get there, because cats outside the camera range are skipped much sooner. 
        # It exists so the while loop can’t run forever.
        r_cap = 8

        # The seed of the random number generator, which makes the layout reproducible. 
        # Every render with the same settings gives the same tree.
        seed = 3

        # W and H are the frame's width and height
        # I know they are bad variable names, but it's like 2 am.
        W = config.frame_width
        H = config.frame_height

        # Just your average seeded NumPy random generator
        rng = np.random.default_rng(seed)

        # Template loads the SVG and scales it to cat_height. cat_w is the resulting width
        template = SVGMobject("white_cat.svg").set_height(cat_height)
        cat_w = template.width

        # min_dist is raised to at least cat_w + 0.1, so the “personal circle” is wider than the cat.
        min_dist = max(min_dist, cat_w + 0.1)

        # edge_min is raised so lines are always longer than the spacing.
        edge_min = max(edge_min, min_dist + 0.15)

        # This is the central idea. It is a continuous "how many generations exist" number.
        # Everything (fade-ins, camera scroll, zoom) is a function of it, so nothing stops at each level
        depth = ValueTracker(-1)

        # This is a smooth version of max(0, x)
        # It's used for camera speed, so this makes the camera smooth
        def softplus(x, k=0.8):
            return k * np.log1p(np.exp(x / k))

        # Returns the opacity of generation g at depth d.
        def born(g, d):
            anticipation = 1.0
            return float(np.clip(d - (g - 1) + anticipation, 0, 1))

        # Returns how far below the root the camera center is. It is zero until
        # about scroll_start, then eases smoothly into a constant scroll speed.
        def c_of(d):
            """Camera centre, in world units below the root."""
            dd = max(d, 0.0)
            return scroll_speed * (softplus(dd - scroll_start) - softplus(-scroll_start))

        # This next code block is the code for the layout. Only the left half of the tree is ever searched.
        # The "left-half" of generation g is local indices 0 ... n/2 - 1. These are exactly the descendants of
        # the root's left-child.
        # Every cat placed there is immediately copied to its mirror position on the right.
        # For example, in generation 2, the local indices are 0, 1, 2, 3. Indices 0 and 1 are children of
        # the root's left child, so they are searched. Then indices 3 and 2 are their mirrors (n - 1 - i), so they
        # are copied over.

        # As for actually positioning the cats, think Poisson-disk

        # This uses heap indexing. Each cat gets one global number, counting row by row: the root is 0, 
        # generation 1 is 1 to 2, generation 2 is 3 to 6, and so on. Node i of generation g has global index 
        # 2**g - 1 + i with its parent as (index - 1) // 2, and its mirror is 2**g - 1 - i in the same generation.

        # This is the total number of slots for generations 0 to G_cap.
        N = 2 ** (G_cap + 1) - 1

        # P[j] is the (x,y) position of cat h. NaN means "never placed", ehat is what lets place_gen detect a
        # missing parent.
        P = np.full((N, 2), np.nan)

        # D[j] id the angle, in radians, of the line that brought the cat there. Children inherit it and deviate
        # by the spread.
        D = np.zeros(N)

        # This is half the wifth of the widest view, plus a margin. No cat is placed further left than -half_x
        half_x = zoom_end * W / 2 + 0.5

        # These are the same cats sotred a second way, packed in placement order. P is indexed by global number
        # and has NaN holes, so it is awkaward to run vector math on. Q[:n] is a clean block of the first n placed
        # cats, which NumPy can slice as a view with no copying.

        # Q[k] is cat k's position
        Q = np.zeros((N, 2))

        # QA[k] is its parent's position, so QA[k] -> Q[k] is its line
        QA = np.zeros((N, 2))

        # Qid[k] is cat k's global number
        Qid = np.zeros(N, dtype=int)

        # cnt starts at 1, because row 0 is already the root. Q[0] is zeroes, which is the origin,
        # and Qid[0] is 0, the root's number. Row 0 has no line, so QA[0] is meaningless
        cnt = [1]

        # The root sits at the origin and points straight down (-90), built[0] is the last generation
        # fully laid out, and it is 0 for now (since we have just the root node)
        P[0] = (0.0, 0.0)
        D[0] = -PI / 2
        built = [0]

        # Geometry helper that converts generation and local index to a global number
        def gidx(g, i):
            return 2 ** g - 1 + i

        # This is the distance from how many points to one segment a->b
        # A "point" is a cat's center, and "segment" is the line between two cats.
        # # This is needed because when a new cat is being placed, the code wants to keep lines from running right
        # through other cats. It makes two checks, and both are in spot_ok.
        # We use the function to check one segmenet, and comparing it against all of the existing cats.

        # The trick is to find a point on the segment that is closest to the cat, then measure to that point.
        # Imagine a segment from a to b, and a cat at p. If you drop a perpendicular from p onto the line ab,
        # where it lands is the cat's "shadow" on the line.

        # ab is the segment's direction vector, and (pts - a) @ ab is each point's dot product with ab.
        # Dividing by ab @ ab (the squared length) gives t: how far along the segment the point's projection falls,
        # where 0 is a and 1 is b.
        def pts_to_seg(pts, a, b):
            ab = b - a
            t = np.clip(((pts - a) @ ab) / (ab @ ab), 0, 1)

            # Returns a set of vector norms (one for each point to the ab)
            return np.linalg.norm(pts - (a + t[:, None] * ab), axis=1)

        # This is the mirror version: one point, many segments: A[i]->B[i].
        # Because every segment now has its own direction, @ no longer works, so einsum("ij, ij->i") computes a dot
        # product row by row

        # This is needed because when a new cat is being placed, we want to prevent that cat from being too close to
        # any existing lines.

        # p is one point. In the code it is the candidate cat c.
        # A is the start of every segment, and B is the end of every segment.
        # Row i of A and row i of together are segment i.
        def pt_to_segs(p, A, B):
            AB = B - A
            # This is Einstein summation
            # We consider two vectors, p - A[i], and B[i] - A[i]
            t = np.clip(np.einsum("ij,ij->i", p - A, AB) / np.einsum("ij,ij->i", AB, AB), 0, 1)
            return np.linalg.norm(p - (A + t[:, None] * AB), axis=1)

        def spot_ok(c, pp, parent_id, strict):
            if c[0] > -min_dist / 2 or c[0] < -half_x:
                return False
            n = cnt[0]
            pts = Q[:n]
            if (np.linalg.norm(pts - c, axis=1) < min_dist).any():
                # cats never overlap (hard rule)
                return False
            # line clearance is only a preference
            if strict:
                keep = Qid[:n] != parent_id
                if (pts_to_seg(pts[keep], pp, c) < line_clear).any():
                    return False
                if n > 1 and (pt_to_segs(c, QA[1:n], Q[1:n]) < line_clear).any():
                    return False
            return True

        def add_node(j, pos, pos_parent, direction):
            P[j] = pos
            D[j] = direction
            Q[cnt[0]] = pos
            QA[cnt[0]] = pos_parent
            Qid[cnt[0]] = j
            cnt[0] += 1

        skipped = [0]

        def place_gen(g):
            n = 2 ** g
            spread = np.radians(first_spread) * spread_decay ** (g - 1)
            # left half; random order is fairer
            for i in rng.permutation(n // 2):
                pg = gidx(g - 1, i // 2)
                pp, pdir = P[pg], D[pg]
                # parent was never placed, so neither is this cat
                if np.isnan(pp[0]):
                    continue
                sign = -1.0 if i % 2 == 0 else 1.0
                # how far below the root the parent is
                pp_q = -pp[1]
                r = edge_min
                c = None
                while c is None:
                    # no candidate can be above y_limit once even the flattest direction is below it
                    if r > r_cap or pp_q + 0.0998 * r > y_limit:
                        break
                    for _ in range(20):
                        if r > edge_min + 3 * edge_step:
                            # crowded: any downward direction
                            a = rng.uniform(-PI + 0.1, -0.1)
                        else:
                            a = pdir + sign * spread * (1 + spread_jitter * rng.uniform(-1, 1))
                            a = float(np.clip(a, -PI + 0.1, -0.1))
                        rr = r + rng.uniform(0, edge_step)
                        c_try = pp + rr * np.array([np.cos(a), np.sin(a)])
                        # below anything the camera shows
                        if -c_try[1] > y_limit:
                            continue
                        strict = r < edge_min + 8 * edge_step
                        if spot_ok(c_try, pp, pg, strict):
                            c, a_ok = c_try, a
                            break
                    if c is None:
                        r += edge_step if r < edge_min + 8 * edge_step else 0.15 * r
                # no room: end this branch here
                if c is None:
                    skipped[0] += 1
                    continue
                j, jm = gidx(g, i), gidx(g, n - 1 - i)
                add_node(j, c, pp, a_ok)
                pm = P[gidx(g - 1, (n - 1 - i) // 2)]
                add_node(jm, np.array([-c[0], c[1]]), pm, -PI - a_ok)
            built[0] = g

        def ensure(g):
            g = min(g, G_cap)
            while built[0] < g:
                place_gen(built[0] + 1)

        # Timeline
        d_exit = 0.0
        while c_of(d_exit) < zoom_end * H / 2 + cat_height / 2:
            d_exit += 0.01
        end_depth = d_exit + tail_seconds / seconds_per_level

        # Which nodes are ever on screen (so we only build those)
        ds = np.linspace(-1, end_depth, 300)
        cs = np.array([c_of(d) for d in ds])
        zf = zoom_start + (zoom_end - zoom_start) * (ds + 1) / (end_depth + 1)
        half_w = zf * W / 2 + 1.0
        half_h = zf * H / 2 + 1.0
        # lowest point the camera ever shows
        y_limit = cs.max() + half_h.max()

        vis = []
        g = 0
        while True:
            ensure(g)
            ids = np.arange(gidx(g, 0), gidx(g, 2 ** g))
            x, q = P[ids, 0], -P[ids, 1]
            ok = ds > g - 2                       # born(g, d) > 0
            seen = (
                (np.abs(x)[:, None] <= half_w[None, :])
                & (np.abs(q[:, None] - cs[None, :]) <= half_h[None, :])
                & ok[None, :]
            ).any(axis=1)
            vis.append(seen)
            # nothing placed in this generation: we're done
            if np.isnan(q).all() or g >= G_cap:
                break
            g += 1

            if skipped[0]:
                print(f"PopulationTree: {skipped[0]} cats had no room and were skipped")

        # Re-parenting: each cat links to the nearest cat above it
        cat_clear = 0.05    # padding around a cat's box when testing for lines through it
        min_rise = 0.1      # parent must be at least this much higher on screen
        max_tries = 12      # how many nearest candidates a cat may try

        def seg_hits_boxes(a, b, centers, hw, hh):
            """Vectorised Liang-Barsky: does segment a-b touch each axis-aligned box?"""
            d = b - a
            half = np.array([hw, hh])
            lo = centers - half - a
            hi = centers + half - a
            t0 = np.zeros(len(centers))
            t1 = np.ones(len(centers))
            for k in range(2):
                if abs(d[k]) < 1e-12:
                    outside = (lo[:, k] > 0) | (hi[:, k] < 0)
                    t1 = np.where(outside, -1.0, t1)
                else:
                    ta, tb = lo[:, k] / d[k], hi[:, k] / d[k]
                    t0 = np.maximum(t0, np.minimum(ta, tb))
                    t1 = np.minimum(t1, np.maximum(ta, tb))
            return t0 <= t1

        def orient(p, q, r):
            return (q[..., 0] - p[..., 0]) * (r[..., 1] - p[..., 1]) \
                 - (q[..., 1] - p[..., 1]) * (r[..., 0] - p[..., 0])

        def seg_crosses(a, b, C, D):
            o1, o2 = orient(a, b, C), orient(a, b, D)
            o3, o4 = orient(C, D, a), orient(C, D, b)
            return (o1 * o2 < 0) & (o3 * o4 < 0)

        def trimmed(p, c):
            """Line from cat p to cat c, shortened to the cats' bounding boxes (None if too short)."""
            dist = np.linalg.norm(c - p)
            u = (c - p) / dist
            trim = min(cat_w / 2 / (abs(u[0]) + 1e-9),
                       cat_height / 2 / (abs(u[1]) + 1e-9)) + 0.04
            if dist <= 2 * trim + 0.05:
                return None
            return p + u * trim, c - u * trim

        # every placed cat (drawn or not), with its generation
        node_ids, node_gen = [], []
        for g in range(len(vis)):
            for i in range(2 ** g):
                j = gidx(g, i)
                if np.isfinite(P[j, 0]):
                    node_ids.append(j)
                    node_gen.append(g)
        node_ids, node_gen = np.array(node_ids), np.array(node_gen)
        pos = P[node_ids]
        n_nodes = len(node_ids)
        hw, hh = cat_w / 2 + cat_clear, cat_height / 2 + cat_clear

        def is_seen(j, g):
            return bool(vis[g][j - (2 ** g - 1)])

        # Work on the left half only (root included) and mirror each chosen line,
        # so the tree stays symmetric and the two halves never interact.
        left = np.where(pos[:, 0] < 0)[0]
        id2idx = {int(j): t for t, j in enumerate(node_ids)}

        accA = np.zeros((len(left) + 1, 2))
        accB = np.zeros((len(left) + 1, 2))
        n_acc = [0]
        lines_by_gen = {}

        def add_line(k, pk, a, b):
            accA[n_acc[0]], accB[n_acc[0]] = a, b
            n_acc[0] += 1
            gk, gp = int(node_gen[k]), int(node_gen[pk])
            if is_seen(int(node_ids[k]), gk) or is_seen(int(node_ids[pk]), gp):
                # fades in once both cats exist
                bucket = lines_by_gen.setdefault(max(gk, gp), [])
                bucket.append(Line([*a, 0], [*b, 0], stroke_width=1.5))
                bucket.append(Line([-a[0], a[1], 0], [-b[0], b[1], 0], stroke_width=1.5))

        def candidates(k, tries, rise, earlier):
            ok = (pos[:, 1] > pos[k, 1] + rise) & (pos[:, 0] <= 0)
            if earlier:
                ok &= node_gen < node_gen[k]
            idx = np.where(ok)[0]
            if not len(idx):
                return []
            dist = np.linalg.norm(pos[idx] - pos[k], axis=1)
            o = np.argsort(dist)[:tries]
            return [(dist[t], idx[t]) for t in o]

        # Passes get looser; a cat only reaches a later pass if the earlier ones failed.
        passes = [
            dict(tries=12,   rise=0.1, earlier=True,  clear=cat_clear, cross=True),
            dict(tries=None, rise=0.1, earlier=True,  clear=cat_clear, cross=True),
            # any cat above, any generation
            dict(tries=None, rise=0.0, earlier=False, clear=0.0,       cross=True),
            # crossings allowed
            dict(tries=None, rise=0.0, earlier=False, clear=0.0,       cross=False),
        ]
        todo = list(left)
        for n_pass, cfg in enumerate(passes, 1):
            hw, hh = cat_w / 2 + cfg["clear"], cat_height / 2 + cfg["clear"]
            cands = {k: candidates(k, cfg["tries"], cfg["rise"], cfg["earlier"]) for k in todo}
            order = sorted((k for k in todo if cands[k]), key=lambda k: cands[k][0][0])
            failed = [k for k in todo if not cands[k]]
            for k in order:
                chosen = None
                for _, pk in cands[k]:
                    seg = trimmed(pos[pk], pos[k])
                    if seg is None:
                        continue
                    a, b = seg
                    others = np.ones(n_nodes, dtype=bool)
                    others[[k, pk]] = False
                    if seg_hits_boxes(a, b, pos[others], hw, hh).any():
                        # would go through a cat
                        continue
                    if cfg["cross"] and n_acc[0] and seg_crosses(a, b, accA[:n_acc[0]], accB[:n_acc[0]]).any():
                        # would cross a line already chosen
                        continue
                    chosen = (a, b, pk)
                    break
                if chosen is None:
                    failed.append(k)
                else:
                    add_line(k, chosen[2], chosen[0], chosen[1])
            print(f"PopulationTree: pass {n_pass}: {len(failed)} cats still without a parent")
            todo = failed

        # Last resort: connect to the layout's own parent, no checks
        orphans = 0
        for k in todo:
            g = int(node_gen[k])
            i = int(node_ids[k]) - (2 ** g - 1)
            pk = id2idx[gidx(g - 1, i // 2)]
            seg = trimmed(pos[pk], pos[k])
            if seg is None:
                # the two cats are practically touching
                orphans += 1
                continue
            add_line(k, pk, *seg)
        print(f"PopulationTree: {orphans} cats left without a line")

        # Mobjects (one group + one updater per generation)
        line_groups, cat_groups = [], []
        for g, seen in enumerate(vis):
            cats = VGroup()
            for i in range(2 ** g):
                if seen[i]:
                    j = gidx(g, i)
                    cats.add(template.copy().move_to([P[j, 0], P[j, 1], 0]))
            lines = VGroup(*lines_by_gen.get(g, []))

            def update_cats(m, g=g):
                m.set_opacity(born(g, depth.get_value()))

            def update_lines(m, g=g):
                m.set_stroke(opacity=born(g, depth.get_value()))

            if len(cats):
                cats.add_updater(update_cats)
            if len(lines):
                lines.add_updater(update_lines)
            cat_groups.append(cats)
            line_groups.append(lines)

        self.add(*line_groups, *cat_groups)

        # Camera: scrolls down, root rises off the top
        def update_camera(_):
            self.camera.frame.move_to([0, -c_of(depth.get_value()), 0])

        camera_driver = Mobject()
        camera_driver.add_updater(update_camera)
        self.add(camera_driver)

        self.camera.frame.set_width(W * zoom_start)
        self.camera.frame.move_to([0, 0, 0])

        self.play(
            depth.animate.set_value(end_depth),
            self.camera.frame.animate.set_width(W * zoom_end),
            run_time=seconds_per_level * (end_depth + 1),
            rate_func=linear,
        )
        self.wait(0.5)