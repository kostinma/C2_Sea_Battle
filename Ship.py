
class Ship:
    #
    #   'x' indicates the ship compartment that defines the ship coordinates
    #   (lowest h and v coordinates)
    #   +----> h
    #   |
    # v v
    #      x+++++
    #      ++++++
    #

    m_hor_0 = None   # horizontal coordinate of the ship (the point 'x')
    m_ver_0 = None   # vertical coordinate of the ship (the point 'x')
    m_d_hor = None   # length along the horizontal axis
    m_d_ver = None   # length along the vertical axis
    m_hull  = None   # status/health of the hull compartment by compartment


    # Constructor
    # (h0, v0) - coordinates of the ship
    # dh, dv - ship dimensions
    # hp - initial health of each compartment
    def __init__(self, h0, v0, dh, dv, hp=1.0):
        self.m_hor_0 = h0
        self.m_ver_0 = v0
        self.m_d_hor = dh
        self.m_d_ver = dv
        self.m_hull = [[float(hp) for i in range(dh)] for j in range(dv)]


    # Method used for tests
    def print_ship_stats(self) -> None:
        print("Coordinate H: ", self.m_hor_0)
        print("Coordinate V: ", self.m_ver_0)
        print("Size H: ", self.m_d_hor)
        print("Size V: ", self.m_d_ver)
        print("Hull:")
        for i in range(self.m_d_ver):
            for j in range(self.m_d_hor):
                print(i, j, self.m_hull[i][j])
        print("Floats? ", self.is_OK())


    # True if at least one compartment is OK
    def is_OK(self) -> bool:
        for i in range(self.m_d_ver):
            if any(self.m_hull[i]):
                return True
        return False


    # Describe how the ship reacts to an explosion at (X,Y)
    #
    # *
    #   x-
    #   --
    #   --
    # Return True if there is an impact.
    def boom(self, h:int, v:int) -> bool:
        # (h, v) - coordinates
        if self.m_hor_0 <= h < self.m_hor_0+self.m_d_hor:
            if self.m_ver_0 <= v < self.m_ver_0+self.m_d_ver:
                self.m_hull[v-self.m_ver_0][h-self.m_hor_0] = 0.0
                return True
        return False


    # True if the point (h, v) is in the "wake" of the ship.
    # To keep it simple for this task, the wake is an area including the ship
    # itself and one square area around the ship.
    def in_wake(self, h:int, v:int) -> bool:
        # (h, v) - coordinates
        if      (self.m_hor_0 - 1 <= h < self.m_hor_0 + self.m_d_hor + 1) and \
                (self.m_ver_0 - 1 <= v < self.m_ver_0 + self.m_d_ver + 1):
            return True
        else:
            return False


    # True if the two ships are too close to each other.
    # One ship cannot be in the wake of the other, that is
    # min separation is one square.
    # The method is static to make it look symmetric.
    @staticmethod
    def ships_collide(ship_one, ship_two) -> bool:
        for     v in range(ship_one.m_ver_0, ship_one.m_ver_0+ship_one.m_d_ver):
            for h in range(ship_one.m_hor_0, ship_one.m_hor_0+ship_one.m_d_hor):
                if ship_two.in_wake(h, v):
                    return True
        return False


    # Method used for tests only.
    # Test ships_collide(...).
    @ staticmethod
    def test_ships_collide():
        # one = Ship(h0=4, v0=5, dh=2, dv=3)
        # for v in range(3, 10):
        #     for h in range(2, 8):
        #         two = Ship(h0=h, v0=v, dh=1, dv=1)
        #         print(h, v, Ship.ships_collide(one, two))

        one = Ship(h0=4, v0=5, dh=1, dv=3)
        for v in range(2, 10):
            for h in range(2, 7):
                two = Ship(h0=h, v0=v, dh=1, dv=2)
                print(h, v, Ship.ships_collide(one, two))


    # Method used for tests only.
    # Test how the hull changes.
    # Test function for a ship 3x2
    def test_2_3(self):
        self.print_ship_stats()

        self.m_hull[0][0] = 0.0
        self.m_hull[0][1] = 0.0
        self.print_ship_stats()

        self.m_hull[1][0] = 0.0
        self.m_hull[1][1] = 0.0
        self.print_ship_stats()

        self.m_hull[2][0] = 0.0
        self.print_ship_stats()

        self.m_hull[2][1] = 0.0
        self.print_ship_stats()


    # Method used for tests only.
    # Test the boom method, scan area around and in the ship.
    def test_boom_2_3(self):
        print("boom: ++++++")
        for v in range(4, 9):
            for h in range(3, 7):
                print(v, h, self.boom(h, v))
        print("boom: ------")


    # Method used for tests only.
    # Test the in_wake method, scan area around and in the ship.
    def test_in_wake_2_3(self):
        print("wake: ++++++")
        for v in range(3, 10):
            for h in range(2, 8):
                print(v, h, self.in_wake(h, v))
        print("wake: ------")


if __name__ == "__main__":
    a_ship = Ship(h0=4, v0=5, dh=2, dv=3)
    # a_ship.test_2_3()
    # a_ship.test_boom_2_3()
    # a_ship.test_in_wake_2_3()

    # Ship.test_ships_collide()

# End of file
