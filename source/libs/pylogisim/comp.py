import xml.etree.ElementTree as ET

class Comp():
    directions_decode = {'right': 'east', 'left': 'west', 'up': 'north', 'down': 'south'}
    def __init__(self, x_pos, y_pos, parent, facing='up'):
        self.x = x_pos
        self.y = y_pos
        self.facing = self.directions_decode[facing]
        self.parent = parent
    def move(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def _add_param(self, parent, name, value):
        if name is None or value is None:
            return None
        else:
            a = ET.SubElement(parent, 'a')
            a.set('name', name)
            a.set('val', value)
            return a
    
    def get_out(self):
        return self.x, self.y

    def get_in(self):
        return self.x, self.y

class Probe(Comp):
    def __init__(
            self,
            x_pos,
            y_pos,
            parent,
            facing = 'up',
            label = 'text',
            labelloc = 'up'
            ):
        self.label = label
        self.labelloc = self.directions_decode[labelloc]

        super().__init__(x_pos, y_pos, parent, facing)
        self._to_xml()

    def _to_xml(self):
        chip = ET.SubElement(self.parent, 'comp')

        chip.set('lib', '0')
        chip.set('name', 'Probe')
        chip.set('loc', f'({self.x},{self.y})')

        self._add_param(chip, 'facing',self.facing)
        self._add_param(chip, 'label', self.label)
        self._add_param(chip, 'labelloc',self.labelloc)
        return chip


class Pin(Comp):
    def __init__(
            self,
            x_pos,
            y_pos,
            parent,
            facing = 'up',
            label = 'text',
            labelloc = 'up',
            tristate = False
            ):
        self.label = label
        self.labelloc = self.directions_decode[labelloc] 
        self.tristate = 'true' if tristate else 'false'

        super().__init__(x_pos, y_pos, parent, facing)
        self._to_xml()

    def _to_xml(self):
        chip = ET.SubElement(self.parent, 'comp')

        chip.set('lib', '0')
        chip.set('name', 'Pin')
        chip.set('loc', f'({self.x},{self.y})')

        self._add_param(chip, 'facing',self.facing)
        self._add_param(chip, 'label', self.label)
        self._add_param(chip, 'labelloc',self.labelloc)
        self._add_param(chip, 'tristate', self.tristate)
        return chip


class OrGate(Comp):
    def __init__(
            self,
            x_pos,
            y_pos,
            parent,
            facing = 'up',
            label = '',
            inputs = 5, 
            negates = []
            ):
        self.label = label
        self.inputs = str(inputs)
        self.negates = [False for i in range(inputs)] if negates == [] else negates
        self.busy_in = [False for i in range(inputs)]

        super().__init__(x_pos, y_pos, parent, facing) 
        self._to_xml()

    def get_in(self):
        for i, item in enumerate(self.busy_in):
            if item is False:

                self.busy_in[i] = True
                if self.negates[i] == True:
                    nor_padding = -10
                else:
                    nor_padding = 0

                if self.facing == 'south':
                    return self.x - int(int(self.inputs)/2) * 10 + i * 10, self.y - 50 + nor_padding

                elif self.facing  == 'north':
                    return self.x + int(int(self.inputs)/2) * 10 - i * 10, self.y + 50 - nor_padding

                elif self.facing == 'west':
                    return self.x + 50 - nor_padding , self.y + int(int(self.inputs)/2) * 10 - i * 10
                
                elif self.facing == 'east':
                    return self.x - 50 + nor_padding, self.y - int(int(self.inputs)/2) * 10 + i * 10

    def _to_xml(self):
        chip = ET.SubElement(self.parent, 'comp')

        chip.set('lib', '1')
        chip.set('name', 'OR Gate')
        chip.set('loc', f'({self.x},{self.y})')

        self._add_param(chip, 'facing',self.facing)
        self._add_param(chip, 'label', self.label)
        self._add_param(chip, 'inputs', self.inputs)
        for i, item in enumerate(self.negates):
            if item is True:
                self._add_param(chip, f'negate{i}', 'true')
        return chip


class AndGate(Comp):
    def __init__(
            self,
            x_pos,
            y_pos,
            parent,
            facing = 'up',
            label = '',
            inputs = 5, 
            negates = []
            ):
        self.label = label
        self.inputs = str(inputs)
        self.negates = [False for i in range(inputs)] if negates == [] else negates
        self.busy_in = [False for i in range(inputs)]
        
        super().__init__(x_pos, y_pos, parent, facing)
        self._to_xml()

    def _to_xml(self):
        chip = ET.SubElement(self.parent, 'comp')

        chip.set('lib', '1')
        chip.set('name', 'AND Gate')
        chip.set('loc', f'({self.x},{self.y})')

        self._add_param(chip, 'facing',self.facing)
        self._add_param(chip, 'label', self.label)
        self._add_param(chip, 'inputs', self.inputs)
        for i, item in enumerate(self.negates):
            if item is True:
                self._add_param(chip, f'negate{i}', 'true')
        return chip

    def get_in(self):
        for i, item in enumerate(self.busy_in):
            if item is False:

                self.busy_in[i] = True
                if self.negates[i] == True:
                    nor_padding = -10
                else:
                    nor_padding = 0

                if self.facing == 'south':
                    return self.x - int(int(self.inputs)/2) * 10 + i * 10, self.y - 50 + nor_padding

                elif self.facing  == 'north':
                    return self.x + int(int(self.inputs)/2) * 10 - i * 10, self.y + 50 - nor_padding

                elif self.facing == 'west':
                    return self.x + 50 - nor_padding , self.y + int(int(self.inputs)/2) * 10 - i * 10
                
                elif self.facing == 'east':
                    return self.x - 50 + nor_padding, self.y - int(int(self.inputs)/2) * 10 + i * 10
            

class Text(Comp):
    def __init__(
            self,
            x_pos,
            y_pos,
            parent,
            text = 'text'
            ):
        self.text = text

        super().__init__(x_pos, y_pos, parent)
        self._to_xml()

    def _to_xml(self):
        chip = ET.SubElement(self.parent, 'comp')

        chip.set('lib', '6')
        chip.set('name', 'Text')
        chip.set('loc', f'({self.x},{self.y})')

        self._add_param(chip, 'text', self.text)
        return chip


