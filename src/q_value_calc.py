from collections import namedtuple
QVal = namedtuple('QVal', ['qval', 'hit', 'score'])


def calculate_q_value(hits,decoys=False):
    hits.sort(key=lambda x: x.score, reverse=True)
    fdr_vals = []
    for i in range(len(hits)):
        #calculate the proportion of false hits so far
        if decoys:
            fdr = sum([int(h.hit == 'decoy') for h in hits[:i+1]])/(i+1)
        else:
            fdr = sum([int(not h.hit) for h in hits[:i+1]])/(i+1)
        fdr_vals.append(fdr)
    q_vals = [0 for f in fdr_vals]
    q_vals[-1] = fdr_vals[-1]
    # ensure non-decreasing q_value
    for i in range(len(q_vals)-2,0,-1):
        q_vals[i] = min(fdr_vals[i],q_vals[i+1])
    q_list = []
    for i,h in enumerate(hits):
        # Simon says:
        #if h.hit:
            q_list.append((q_vals[i],h.hit,h.score))
    return q_list