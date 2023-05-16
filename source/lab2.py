import sys

import subprocess

from zipfile import ZipFile

from libs.boolean_logic_funcs.main import BoolVector
from libs.pylogisim.main import Logisim, Wire
import libs.pylogisim.comp as cpns


if __name__ == '__main__':
    bv = BoolVector(str(sys.argv[1]))
    
