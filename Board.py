
from Fleet import Fleet
import random

class Board:
    m_public_view  = None   # 2D map
    m_private_view = None   # 2D map
    m_fleet = None

    def __init__(self, fleet):
        self.m_fleet = fleet
        self.init_public_view()
        self.init_private_view()

    # Shoot until hit an empty cell
    def shoot_randomly(self):
        while True:
            h = random.randint(1, self.m_fleet.H_max)
            v = random.randint(1, self.m_fleet.V_max)
            if self.shoot(h, v):
                return
            else:
                continue


    # True if (h, v) are valid, that is not yet used coordinates
    def shoot(self, h:int, v:int) -> bool:
        # (h, v) epicenter coordinates

        if self.m_private_view[v][h] == 'T' or self.m_private_view[v][h] == 'X':
            return False

        if self.m_fleet.boom(h, v):
            self.m_private_view[v][h] = 'X'
            self.m_public_view[v][h] = 'X'
        else:
            self.m_private_view[v][h] = 'T'
            self.m_public_view[v][h] = 'T'

        return True


    # Create a 2D map of what other players would see
    def init_public_view(self):
        if self.m_fleet == None:
            raise Exception("Board: init_public_view: fleet is not defined")

        self.m_public_view = []
        H_max = self.m_fleet.H_max
        V_max = self.m_fleet.V_max

        # line 1
        a_line = []
        a_line.append('0')
        # a_line.append('|')
        for i in range(H_max):
            j = i + 1
            k = j % 10
            a_line.append(str(k))
        self.m_public_view.append(a_line)

        # line 2
        # a_line = []
        # a_line.append('-')
        # a_line.append('+')
        # for i in range(H_max):
        #     a_line.append('-')
        # self.m_public_view.append(a_line)

        # other lines
        for j in range(V_max):
            a_line = []
            k = (j+1) % 10
            a_line.append(str(k))
            # a_line.append('|')
            for i in range(H_max):
                a_line.append('O')
            self.m_public_view.append(a_line)


    # Create a 2D map of what owner would see
    def init_private_view(self):
        if self.m_fleet == None:
            raise Exception("Board: init_private_view: fleet is not defined")

        self.m_private_view = []
        H_max = self.m_fleet.H_max
        V_max = self.m_fleet.V_max

        # line 1
        a_line = []
        a_line.append('0')
        # a_line.append('|')
        for i in range(H_max):
            j = i + 1
            k = j % 10
            a_line.append(str(k))
        self.m_private_view.append(a_line)

        # line 2
        # a_line = []
        # a_line.append('-')
        # a_line.append('+')
        # for i in range(H_max):
        #     a_line.append('-')
        # self.m_private_view.append(a_line)

        # Other lines
        for j in range(V_max):
            a_line = []
            k = (j+1) % 10
            a_line.append(str(k))
            # a_line.append('|')
            for i in range(H_max):
                a_line.append('O')
            self.m_private_view.append(a_line)

        # Add ships to the view
        for h in range(1, H_max+1):
            for v in range(1, V_max+1):
                if self.m_fleet.in_any_ship(h, v):
                    self.m_private_view[v][h] = '■'


    def print_public_view(self):
        for line in self.m_public_view:
            print('|'.join(line))


    def print_private_view(self):
        for line in self.m_private_view:
            print('|'.join(line))


if __name__ == "__main__":
    pass

# End of file
