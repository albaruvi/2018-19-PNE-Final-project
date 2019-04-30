def count_bases(seq):

    counter_as = 0
    counter_ts = 0
    counter_gs = 0
    counter_cs = 0
    for b in seq:
        if b == 'A':
            counter_as += 1
        if b == 'T':
            counter_ts += 1
        if b == 'G':
            counter_gs += 1
        if b == 'C':
            counter_cs += 1
    dic = {'As': counter_as, 'Ts': counter_ts, 'Gs': counter_gs, 'Cs': counter_cs}
    # Return the dictionary
    return dic
