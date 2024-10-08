N = range(10)
depot = 0
demand = [0, 3, 1, 2, 1, 2, 2, 2, 3, 2]

# dist[i][j] gives the travel time (mins) between i and j
dist = [
	[0, 30, 50, 120, 140, 180, 120, 210, 160, 100],
	[30, 0, 50, 100, 110, 160, 120, 190, 140, 70],
	[50, 50, 0, 70, 100, 130, 70, 160, 110, 60],
	[120, 100, 70, 0, 60, 60, 60, 90, 40, 30],
	[140, 110, 100, 60, 0, 120, 120, 150, 100, 40],
	[180, 160, 130, 60, 120, 0, 100, 30, 50, 90],
	[120, 120, 70, 60, 120, 100, 0, 130, 50, 90],
	[210, 190, 160, 90, 150, 30, 130, 0, 80, 120],
	[160, 140, 110, 40, 100, 50, 50, 80, 0, 70],
	[100, 70, 60, 30, 40, 90, 90, 120, 70, 0]
]

# DETERMINISTIC

# States:
# - Current customer
# - Visited customers
# - Minutes remaining

# Action:
# - Customer to visit next

# Value function:
# max number of cylinder delivered
# V(j, S, m)
# where:
# 	- at customer j
# 	- with m minutes remaining
# 	- having visited customers S


def v(j, S, m):
	# BASE CASE -> default - go back to depot
	# & see if there's better opts down the line

	# infeasible
	if dist[j][depot] <= m:
		best = (0, depot, 0)
	else: #stuck
		best = (-float("inf"), -float("inf"), -float("inf"))

	for k in N[1:]:
		# not visited & reachable
		if not k in S and dist[j][k] <= m:
			best = max(best, (demand[k] + v(k, S+[k], m-dist[j][k])[0], k, m-dist[j][k]))

	return best

if __name__ == '__main__':
	j = depot
	S = []
	m = 6*60

	p, _, _ = v(j, S, m)

	for i in N:
		_, j, m = v(j, S, m)
		S += [j]
		print(f"Go to: {j}\ntime remaining: {m}\n")

	print(f"# cylinders delivered: {p}")





