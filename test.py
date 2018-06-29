from tqdm import tqdm


def partiesliste(seq):
	# retuns all subsets possibles from seq

    p = []
    i, imax = 0, 2**len(seq)-1
    with tqdm(total=2**len(seq)) as progress:    
        while i <= imax:
            s = []
            j, jmax = 0, len(seq)-1
            while j <= jmax:
                if (i>>j)&1 == 1:
                    s.append(seq[j])
                    progress.update(1)
                j += 1
            p.append(s)
            progress.update(1)
            i += 1 
    del p[0]
    return p

L = []

for i in range(30):
    L.append(i)

print(len(partiesliste(L)))

