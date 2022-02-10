
def print_dist(dist):
    keys = dist.keys()
    for i in dist:
        dd = dict(dist[i].items())
        arrayToPrint = []
        for k in keys:
            if k in dd: 
                arrayToPrint.append(dd[k])
        print(i.ljust(3), arrayToPrint)