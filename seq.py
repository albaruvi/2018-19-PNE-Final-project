class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        print('New sequence created!')

        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def complement(self):
        sequence = ''
        for i in self.strbases:
            if i == 'A':
                sequence += 'T'
            elif i == 'T':
                sequence += 'A'
            elif i == 'G':
                sequence += 'C'
            elif i == 'C':
                sequence += 'G'
        return sequence

    def reverse(self):
        reverse_sequence = ''
        for i in self.strbases:
            reverse_sequence = i + reverse_sequence
        return reverse_sequence

    def count_base(self):
        counter_a = 0
        counter_t = 0
        counter_g = 0
        counter_c = 0
        for b in self.strbases:
            if b == 'A':
                counter_a += 1
            if b == 'T':
                counter_t += 1
            if b == 'G':
                counter_g += 1
            if b == 'C':
                counter_c += 1
        nb = {'As':counter_a, 'Ts':counter_t, 'Gs':counter_g, 'Cs':counter_c}
        return nb

    def perc_bases(self):
        from bases import count_bases
        na = count_bases(self.strbases)['As']
        nt = count_bases(self.strbases)['Ts']
        ng = count_bases(self.strbases)['Gs']
        nc = count_bases(self.strbases)['Cs']

        tl = len(self.strbases)
        if tl > 0:
            perc_a = round(100.0 * na / tl, 1)
            perc_t = round(100.0 * nt / tl, 1)
            perc_g = round(100.0 * ng / tl, 1)
            perc_c = round(100.0 * nc / tl, 1)
        else:
            perc_a = 0
            perc_t = 0
            perc_g = 0
            perc_c = 0

        pb = {'As':perc_a, 'Ts':perc_t, 'Gs':perc_g, 'Cs':perc_c}
        return pb
