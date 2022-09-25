import xml.etree.ElementTree as ET

class Logisim():

    def __init__(self, name):
        self.name = name
        self.project = ET.parse('/home/gl_epka/Code/Architecture_labs/source/libs/pylogisim/base.circ')
        self.root = self.project.getroot()
        
        self.circuit = ET.SubElement(self.root, 'circuit')
        self.circuit.set('name', 'main')
        
        a = ET.SubElement(self.circuit, 'a')
        a.set('name', 'circuit')
        a.set('val', 'main')

        a = ET.SubElement(self.circuit, 'a')
        a.set('name', 'clabel')
        a.set('val', '')

        a = ET.SubElement(self.circuit, 'a')
        a.set('name', 'clabelup')
        a.set('val', 'east')
        
        a = ET.SubElement(self.circuit, 'a')
        a.set('name', 'clabelfont')
        a.set('val', 'SansSerif plain 12')
    
    def export_circuit(self):
        tree = ET.ElementTree(self.root)
        path = self.name.replace(' ', '_') + '.circ'
        tree.write(path)

        return path
        


class Wire():

    def set_wire(self, x1, y1, x2, y2, parent):
        if x1 == x2 or y1 == y2:
            wire1 = ET.SubElement(parent, 'wire')
            wire1.set('from', f'({x1},{y1})')
            wire1.set('to', f'({x2},{y2})')

        else:
            wire1 = ET.SubElement(parent, 'wire')
            wire1.set('from', f'({x1},{y1})')
            wire1.set('to', f'({x1},{y2})')
            
            wire2 = ET.SubElement(parent, 'wire')
            wire2.set('from', f'({x1},{y2})')
            wire2.set('to', f'({x2},{y2})')
                


    def connect(self, frm, to, points = None):
        frmx, frmy = frm.get_out()
        tox, toy = to.get_in()
        
        if points is None:
            self.set_wire(frmx, frmy, tox, toy, frm.parent)
        else:
            prevx, prevy = frmx, frmy
            for pointx, pointy in points:
                self.set_wire(prevx, prevy, pointx, pointy, frm.parent)
                prevx, prevy = pointx, pointy
            
            self.set_wire(prevx, prevy, tox, toy, frm.parent)

