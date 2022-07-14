
def add(*vectors):
	by_coors = zip(*vectors)
	coors_sum = [sum(coors) for coors in by_coors]
	return tuple(coors_sum)

def subtract(v1, v2):
	return tuple(item1-item2 for (item1,item2) in zip(v1,v2))
