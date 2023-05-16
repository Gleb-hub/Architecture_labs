import sys;

from libs.boolean_logic_funcs.main import BoolVector


def sdnf2vivada(bv):
    sdnf: str = bv.sdnf
    sdnf = sdnf.replace('and', '||')
    sdnf = sdnf.replace('or', '&&')
    sdnf = sdnf.replace('not{', '~')
    sdnf = sdnf.replace('}', '')
    sdnf = sdnf.replace('x_', 'in[')
    sdnf = sdnf.replace('0', '0]')
    sdnf = sdnf.replace('1', '1]')
    sdnf = sdnf.replace('2', '2]')
    sdnf = sdnf.replace('3', '3]')
    sdnf = sdnf.replace('4', '4]')

    return sdnf

if __name__ == '__main__':
    bv = BoolVector('133AABBF')
    print(sdnf2vivada(bv))


