import sys

import subprocess

import matplotlib.pyplot as plt

from zipfile import ZipFile

from libs.boolean_logic_funcs.main import BoolVector
from libs.pylogisim.main import Logisim, Wire
import libs.pylogisim.comp as cpns


def first_circ(lab1, wire):

    labels = [cpns.Text(50, 50, text='СДНФ', parent=lab1.circuit)]


    pins = [
            cpns.Pin(100, 100, facing='down', label='x4', labelloc='up', parent=lab1.circuit),
            cpns.Pin(130, 100, facing='down', label='x3', labelloc='up', parent=lab1.circuit),
            cpns.Pin(160, 100, facing='down', label='x2', labelloc='up', parent=lab1.circuit),
            cpns.Pin(190, 100, facing='down', label='x1', labelloc='up', parent=lab1.circuit),
            cpns.Pin(220, 100, facing='down', label='x0', labelloc='up', parent=lab1.circuit)

            ] 

    and_gates=[]
    for i, substr in enumerate(bv.sdnf.split(' and ')):

        negates =[True if 'not' in item else False for item in substr.split(' or ')]

        and_gates.append(
                cpns.AndGate(
                    350,
                    150 + i * 70,
                    facing='right',
                    negates=negates, 
                    parent=lab1.circuit)
                )

    for and_gate in and_gates:
        for pin in reversed(pins):
            wire.connect(pin, and_gate)

    or_gate = cpns.OrGate(450 + len(and_gates) * 10, 350 + int(len(and_gates)/2) * 40 - 20, inputs=len(and_gates) + 1 if len(and_gates) % 2 == 0 else len(and_gates), facing='right', parent=lab1.circuit) 

    for i, and_gate in enumerate(and_gates):
            if and_gate.y > or_gate.y:
                wire.connect(and_gate, or_gate, points=[(and_gate.x + i * 10, and_gate.y)])
            else:
                wire.connect(and_gate, or_gate, points=[(or_gate.x - 60 - i * 10, and_gate.y)])

    probe = cpns.Probe(or_gate.x + 100, or_gate.y, facing='left', label='',parent=lab1.circuit)
    
    wire.connect(or_gate, probe)


def sec_circ(lab1, wire):

    padding = 700
    labels = [cpns.Text(50 + padding, 50, text='СКНФ', parent=lab1.circuit)]


    pins = [
            cpns.Pin(100 + padding, 100, facing='down', label='x4', labelloc='up', parent=lab1.circuit),
            cpns.Pin(130 + padding, 100, facing='down', label='x3', labelloc='up', parent=lab1.circuit),
            cpns.Pin(160 + padding, 100, facing='down', label='x2', labelloc='up', parent=lab1.circuit),
            cpns.Pin(190 + padding, 100, facing='down', label='x1', labelloc='up', parent=lab1.circuit),
            cpns.Pin(220 + padding, 100, facing='down', label='x0', labelloc='up', parent=lab1.circuit)

            ]

    or_gates=[]
    for i, substr in enumerate(bv.sknf.split(' or ')):

        negates =[True if 'not' in item else False for item in substr.split(' and ')]

        or_gates.append(
                cpns.OrGate(
                    350 + padding,
                    150 + i * 70,
                    facing='right',
                    negates=negates, 
                    parent=lab1.circuit)
                )

    for or_gate in or_gates:
        for pin in reversed(pins):
            wire.connect(pin, or_gate)

    and_gate = cpns.AndGate(450 + len(or_gates) * 10 + padding, 350 + int(len(or_gates)/2) * 40 - 20, inputs=len(or_gates) + 1 if len(or_gates) % 2 == 0 else len(or_gates), facing='right', parent=lab1.circuit) 

    for i, or_gate in enumerate(or_gates):

        if or_gate.y <= and_gate.y:
            wire.connect(or_gate, and_gate, points=[(and_gate.x - 60 - i * 10, or_gate.y)])
        else:
            wire.connect(or_gate, and_gate, points=[(or_gate.x + i * 10, or_gate.y)])

    probe = cpns.Probe(and_gate.x + 100, and_gate.y, facing='left', label='',parent=lab1.circuit)
    
    wire.connect(and_gate, probe)

def create_latex_svg(tex:str):
    pass


if __name__ == '__main__':
    bv = BoolVector(str(sys.argv[1]))

#    project = Logisim(name=bv.hex)
#    wire = Wire()

#    first_circ(project, wire)
#    sec_circ(project, wire)

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.set_axis_off()

    t = ax.text(0.5, 0.5, bv.latex_sdnf(), 
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='black')
    ax.figure.canvas.draw()
    bbox = t.get_window_extent()
    fig.set_size_inches(bbox.width/80, bbox.height/80)
    plt.savefig(bv.hex + '.png')

#    path_logisim = project.export_circuit()
    path_table_png = bv.export_table_png()
    path_table_excel = bv.export_table_excel()
    path_to_sknf = bv.export_sknf()
    path_to_sdnf = bv.export_sdnf()

    zipObj = ZipFile(bv.hex + '.zip', 'w')
    zipObj = ZipFile(path_to_sdnf)
#    zipObj.write(path_logisim)
    zipObj.write(path_table_png)
#    zipObj.write(path_table_excel)
    zipObj.write('manual.txt')

#    subprocess.run(['rm', path_logisim, path_table_png, path_table_excel])
