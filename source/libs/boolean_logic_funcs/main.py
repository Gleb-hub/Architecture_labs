import math

import pandas as pd
import dataframe_image as dfi

pd.options.display.latex.repr = True


class BooleanVector:

    def __init__(self, hex_vec: str):
        self.hex = hex_vec

    @property
    def bin(self):
        res = str('{0:08b}'.format(int(self.hex, 16)))
        if len(res) % 4 != 0:
            res = '0' * (4 - (len(res) % 4)) + res
        return res

    @property
    def bin_table(self):
        table_dict = {}
        ranks = int(math.log2(len(self.bin)))

        for rank in range(ranks - 1, -1, -1):
            table_dict['x' + str(rank)] = self._gen_bin_col(len(self.bin), 2 ** rank)
        
        table_dict['y'] = [ bit for bit in self.bin]
        return pd.DataFrame(table_dict)

    def export_table(self, filepath='table.png'):
        dfi.export(self.bin_table, filepath, table_conversion='matplotlib')

    def _gen_bin_col(self, vec_len, step):
        res = []
        curr = 0
        for bit in range(vec_len):
            if curr >= step:
                res.append('1')
                if curr == step * 2 - 1:
                    curr = 0
                else:
                    curr += 1
            else:
                res.append('0')
                curr += 1
        return res

    def FDNF(self):
        pass

    def FCNF(self):
        pass



if __name__ == '__main__':
    bool_vec = BooleanVector("1112666b")
    print(bool_vec.export_table(filepath='1112666b_table.png'))
