import subprocess

from zipfile import ZipFile

from libs.boolean_logic_funcs.main import BoolVector
from libs.pylogisim.main import Logisim, Wire
import libs.pylogisim.comp as cpns


def first_circ(lab1, wire):

    labels = [cpns.Text(50, 50, text='СДНФ', parent=lab1.circuit)]


    pins = [
            cpns.Pin(100, 100, facing='down', label='x0', labelloc='up', parent=lab1.circuit),
            cpns.Pin(130, 100, facing='down', label='x1', labelloc='up', parent=lab1.circuit),
            cpns.Pin(160, 100, facing='down', label='x2', labelloc='up', parent=lab1.circuit),
            cpns.Pin(190, 100, facing='down', label='x3', labelloc='up', parent=lab1.circuit),
            cpns.Pin(220, 100, facing='down', label='x4', labelloc='up', parent=lab1.circuit)

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
        for pin in pins:
            wire.connect(pin, and_gate)

    or_gate = cpns.OrGate(450 + len(and_gates) * 10, 350 + int(len(and_gates)/2) * 50, inputs=len(and_gates) + 1 if len(and_gates) % 2 == 0 else len(and_gates), facing='right', parent=lab1.circuit) 

    for i, and_gate in enumerate(and_gates):

        if i <= int(len(and_gates)/2):
            wire.connect(and_gate, or_gate, points=[(or_gate.x - 60 - i * 10, and_gate.y)])
        else:
            wire.connect(and_gate, or_gate, points=[(and_gate.x + i * 10, and_gate.y)])

    probe = cpns.Probe(or_gate.x + 100, or_gate.y, facing='left', label='',parent=lab1.circuit)
    
    wire.connect(or_gate, probe)


def sec_circ(lab1, wire):

    padding = 700
    labels = [cpns.Text(50 + padding, 50, text='СКНФ', parent=lab1.circuit)]


    pins = [
            cpns.Pin(100 + padding, 100, facing='down', label='x0', labelloc='up', parent=lab1.circuit),
            cpns.Pin(130 + padding, 100, facing='down', label='x1', labelloc='up', parent=lab1.circuit),
            cpns.Pin(160 + padding, 100, facing='down', label='x2', labelloc='up', parent=lab1.circuit),
            cpns.Pin(190 + padding, 100, facing='down', label='x3', labelloc='up', parent=lab1.circuit),
            cpns.Pin(220 + padding, 100, facing='down', label='x4', labelloc='up', parent=lab1.circuit)

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
        for pin in pins:
            wire.connect(pin, or_gate)

    and_gate = cpns.AndGate(450 + len(or_gates) * 10 + padding, 350 + int(len(or_gates)/2) * 50, inputs=len(or_gates) + 1 if len(or_gates) % 2 == 0 else len(or_gates), facing='right', parent=lab1.circuit) 

    for i, or_gate in enumerate(or_gates):

        if i <= int(len(or_gates)/2):
            wire.connect(or_gate, and_gate, points=[(and_gate.x - 60 - i * 10, or_gate.y)])
        else:
            wire.connect(or_gate, and_gate, points=[(or_gate.x + i * 10, or_gate.y)])

    probe = cpns.Probe(and_gate.x + 100, and_gate.y, facing='left', label='',parent=lab1.circuit)
    
    wire.connect(and_gate, probe)


if __name__ == '__main__':
    bv = BoolVector('3488bcce')

    project = Logisim(name=bv.hex)
    wire = Wire()

    first_circ(project, wire)
    sec_circ(project, wire)

    path_logisim = project.export_circuit()
    path_table_png = bv.export_table_png()
    path_table_excel = bv.export_table_excel()
    path_to_sknf = bv.export_sknf()
    path_to_sdnf = bv.export_sdnf()

    zipObj = ZipFile(bv.hex + '.zip', 'w')
    zipObj.write(path_logisim)
    zipObj.write(path_table_png)
    zipObj.write(path_table_excel)
    zipObj.write(path_to_sknf)
    zipObj.write(path_to_sdnf)


    subprocess.run(['logisim', path_logisim])
    subprocess.run(['rm', path_table_png, path_table_excel, path_to_sdnf, path_to_sknf])
