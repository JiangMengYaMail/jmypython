
def add(*vectors):
	by_coors = zip(*vectors)
	coors_sum = [sum(coors) for coors in by_coors]
	return tuple(coors_sum)

