import math

from pylatex import Math

import pandas as pd
import dataframe_image as dfi

pd.options.display.latex.repr = True


class BooleanVector:

    def __init__(self, hex_vec: str):
        self.hex = hex_vec
        self.ranks = 0
    
    @property
    def bin(self):
        res = str('{0:08b}'.format(int(self.hex, 16)))
        if len(res) % 4 != 0:
            res = '0' * (4 - (len(res) % 4)) + res
        return res

    @property
    def bin_table(self):
        table_dict = {}
        self.ranks = int(math.log2(len(self.bin)))

        for rank in range(self.ranks - 1, -1, -1):
            table_dict['x' + str(rank)] = self._gen_bin_col(len(self.bin), 2 ** rank)
        
        table_dict['y'] = [bit for bit in self.bin]
        return pd.DataFrame(table_dict)

    def export_table_png(self):
        dfi.export(self.bin_table, self.hex + '_table.png', table_conversion='matplotlib')

    def export_table_excel(self):
        self.bin_table.to_excel(self.hex + '_table.xlsx')

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

    @property
    def sknf(self):
        res = ''
        array = self.bin_table.loc[self.bin_table['y'] == '1'].index.values
        
        for i in array:
            res += '('
            for rank in range(self.ranks):
                var = 'x'+str(rank)
                bit = self.bin_table.loc[i].at[var]
                if int(bit) == 1:
                    res += 'x_' + str(rank)
                else:
                    res += 'not x_' + str(rank)
                res += ' or '

            res = res[:-4]
            res += ') and '
        return res[:-5] 

    @property
    def sdnf(self):
        res = ''
        array = self.bin_table.loc[self.bin_table['y'] == '0'].index.values
        
        for i in array:
            res += '('
            for rank in range(self.ranks):
                var = 'x'+str(rank)
                bit = self.bin_table.loc[i].at[var]
                if int(bit) == 0:
                    res += 'x_' + str(rank)
                else:
                    res += 'not x_' + str(rank)
                res += ' and '

            res = res[:-5]
            res += ') or '
        return res[:-4] 

    def export_sdnf(self):
        res = self.sdnf.replace('or', '\\vee').replace('and', '\\wedge').replace('not', '\\overline')
        file = open(self.hex + '_sdnf.txt', 'w')
        file.write(res)
        file.close()
        return res
    
    def export_sknf(self):
        res = self.sknf.replace('or', '\\vee').replace('and', '\\wedge').replace('not', '\\overline')
        file = open(self.hex + '_sknf.txt', 'w')
        file.write(res)
        file.close()
        return res


if __name__ == '__main__':
    bool_vec = BooleanVector("1112666b")
    bool_vec.export_table_excel()
