def opt_dist(l, d):
    return min([l[:i].count(1) + l[i+d:].count(1) + l[i:i+d].count(0) for i in range(len(l) - d + 1)])