import pulp

def minimum_dominating_set(g):
    """
    g[i] is the list of neighbors of vertex i.
    Returns a minimum dominating set.
    """

    n = len(g)

    # Create the optimization problem
    prob = pulp.LpProblem("MinimumDominatingSet", pulp.LpMinimize)

    # Binary variable for each vertex
    x = [
        pulp.LpVariable(f"x_{i}", cat="Binary")
        for i in range(n)
    ]

    # Objective:
    # Minimize the number of selected vertices
    prob += pulp.lpSum(x)

    # Every vertex must be dominated
    for i in range(n):

        # Closed neighborhood:
        # vertex i plus all its neighbors
        closed = [i] + g[i]

        prob += pulp.lpSum(x[j] for j in closed) >= 1

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Extract solution
    S = [i for i in range(n) if pulp.value(x[i]) > 0.5]

    return S