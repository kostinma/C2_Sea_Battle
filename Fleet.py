
from Ship import Ship
import random

# Collection of ships within an operational area.
class Fleet:
    H_max     = None   # horizontal deployment range [1, H_max]
    V_max     = None   # vertical deployment range [1, V_max]
    all_ships = None   # list of ships

    # Constructor
    def __init__(self, H=6, V=6):
        self.init(H, V)

    # init can be invoked multiple times.
    # Constructor is separated for test purposes, so we can test
    # other functionality without fully defining the class.
    def init(self, H, V):
        # set limits on the field
        if H <= 1:  raise Exception(f"Range of deployment {H} is too narrow")
        if V <= 1:  raise Exception(f"Range of deployment {V} is too narrow")
        if H > 100: raise Exception(f"Range of deployment {H} is too broad")
        if V > 100: raise Exception(f"Range of deployment {V} is too broad")
        self.H_max = H
        self.V_max = V
        self.all_ships = []

    # Add a ship to the fleet.
    # True if added.
    # False if cannot be added.
    def add_ship(self, h0:int, v0:int, dh:int, dv:int) -> bool:
        # (h0, v0) - 'native' coordinates (lowest h and v)
        # dh - length along the horizontal axis
        # dv - length along the vertical axis
        if not 1 <= h0      <= self.H_max: return False
        if not 1 <= h0+dh-1 <= self.H_max: return False
        if not 1 <= v0      <= self.V_max: return False
        if not 1 <= v0+dv-1 <= self.V_max: return False
        new_ship = Ship(h0, v0, dh, dv)
        # check whether the new ship is in a good position
        for a_ship in self.all_ships:
            if Ship.ships_collide(a_ship, new_ship):
                return False
        self.all_ships.append(new_ship)
        return True

    # An alternative way to add a new ship.
    # Method similar to add_ship.
    # True if the ship is added.
    # False if cannot be added.
    def add_ship_with_direction(self, h0:int, v0:int, length:int, width:int, direction:str) -> bool:
        # (h0, v0) - ship nose coordinates, bow and port side
        # length - length of the ship
        # width - width of the ship
        # direction - can be 'N', 'S', 'W', 'E'
        # The ships 'rotates' around (h0, v0) depending on the direction

        if   direction == 'N':
            h = h0
            v = v0
            dv = length
            dh = width
        elif direction == 'S':
            h = h0 - width + 1
            v = v0 - length + 1
            dv = length
            dh = width
        elif direction == 'W':
            h = h0
            v = v0 - width + 1
            dv = width
            dh = length
        elif direction == 'E':
            h = h0 - length + 1
            v = v0
            dv = width
            dh = length
        else:
            raise Exception(f"Fatal Error: Ship.add_ship_with_direction: unexpected direction {direction}")

        return self.add_ship(h, v, dh, dv)


    # A ship with length and width is attempted to be placed at random coordinates and direction.
    # Raise an Exception if could not do it in {max_failures} attempts.
    # True if placed successfully.
    def add_ship_random(self, length:int, width:int, max_failures:int) -> bool:
        # length       - the ship length
        # width        - the ship width
        # max_failures - cap on number of attempts
        count = 0
        while True:
            h = random.randint(1, self.H_max)
            v = random.randint(1, self.V_max)
            direction = random.choice(['N', 'S', 'W', 'E'])
            count += 1
            # print(count)
            if self.add_ship_with_direction(h, v, length, width, direction):
                return True
            else:
                if count > max_failures:
                    raise Exception("Fatal: Ship.add_ship_random: too many attempts to place a ship randomly")
        return False  # this place should never be reached


    # In order to have a fair game, fleet parameters for the computer player must be identical.
    # This function will create a copy sea, a copy of fleet and place the ships randomly.
    @staticmethod
    def create_comp_fleet(comp_fleet, user_fleet):
        # comp_fleet   - resulting "computer" fleet
        # user_fleet   - original fleet by the user

        comp_fleet.H_max = user_fleet.H_max
        comp_fleet.V_max = user_fleet.V_max

        while True:
            try:
                for a_ship in user_fleet.all_ships:
                    L = a_ship.m_d_hor
                    W = a_ship.m_d_ver
                    comp_fleet.add_ship_random(length=L, width=W, max_failures=10000)
            except:
                continue

            break


    # Setup fleet either by a default way or custom way.
    def place_user_ships(self):
        print("Define your see battle size.")
        a_way = input("'D' for default configuration (6x6) or two numbers (horizontal vertical) for customized size.\n")
        if a_way.lower() == 'd':
            self.init(6, 6)
        else:
            sea_size = a_way.split()
            if len(sea_size) != 2:
                raise Exception(f"Fatal: Fleet.place_ships(): wrong input format {a_way}.")
            self.init(int(sea_size[0]), int(sea_size[1]))

        print("Would you like the default fleet ('D') or a custom fleet ('C')?")
        print("The default fleet is: 1 ship 3x1, 2 ships 2x1, 4 ships 1x1.")
        config_type = input("")
        # Check if the type is ok. Will use it later.
        if  config_type.lower() == 'd' or \
            config_type.lower() == 'c':
            pass
        else:
            raise Exception(f"Fatal: Ship.place_user_ships: unknown fleet type {config_type}.")

        placement_type = input("Would you like to place the ships randomly ('R') or by hand ('H')?.\n")
        if  placement_type.lower() == 'r' or \
            placement_type.lower() == 'h':
            pass
        else:
            raise Exception(f"Fatal: Ship.place_user_ships: unknown type {placement_type}.")

        if config_type.lower() == 'd':
            number_of_ships = 7
        elif config_type.lower() == 'c':
            number_of_ships = int(input("What is the number of ships?\n"))
        # print(number_of_ships)

        # self.print_fleet_stats()
        if config_type.lower() == 'd':
            a_list = [(3,1), (2,1), (2,1), (1,1), (1,1), (1,1), (1,1)]   # (length, width)
            if placement_type.lower() == 'r':
                for elem in a_list:
                    L = elem[0]
                    W = elem[1]
                    # print(L, W)
                    self.add_ship_random(length=L, width=W, max_failures=10000)
            elif placement_type.lower() == 'h':
                for elem in a_list:
                    L = elem[0]
                    W = elem[1]
                    # print(L, W)
                    print(f"For ship with length={L} and width={W} give pos_x pos_y direction (['N','S','W','E'])")
                    print("Example:  1 2 N")
                    (h, v, dir) = input("").split()
                    # print(h, v, dir)
                    if not self.add_ship_with_direction(h0=int(h), v0=int(v), length=L, width=W, direction=dir):
                        raise Exception("Fatal: Fleet.place_user_ships(): bad ship placement")
        elif config_type.lower() == 'c':
            # Totally customized fleet
            for i in range(1, number_of_ships+1):
                # print(i, number_of_ships)
                if placement_type.lower() == 'r':
                    (L, W) = input(f"Ship {i}. Define length and width. Give two numbers.\n").split()
                    # print(int(L), int(W))
                    self.add_ship_random(length=int(L), width=int(W), max_failures=10000)
                elif placement_type.lower() == 'h':
                    (L, W, h, v, dir) = input(f"Ship {i}. Define length width pos_x pos_y direction (['N','S','W','E'])\n").split()
                    if not self.add_ship_with_direction(h0=int(h), v0=int(v), length=int(L), width=int(W), direction=dir):
                        raise Exception("Fatal: Fleet.place_user_ships(): bad ship placement")
                else:
                    pass
                    # This place should never be reached
        else:
            pass
            # This place should never be reached
        # self.print_fleet_stats()


    # Mostly for debugging
    def print_fleet_stats(self):
        print(f"Sea size: {self.H_max} by {self.V_max}")
        for a_ship in self.all_ships:
            a_ship.print_ship_stats()


    # For tests only.
    # Test the method add_ship_random.
    def test_add_ship_random(self):
        self.init(6, 6) # reinitialize for test purpose
        print(self.add_ship_random(length=3, width=1, max_failures=10000))
        self.all_ships[0].print_ship_stats()
        print(self.add_ship_random(length=2, width=1, max_failures=10000))
        self.all_ships[1].print_ship_stats()
        print(self.add_ship_random(length=2, width=1, max_failures=10000))
        self.all_ships[2].print_ship_stats()
        print(self.add_ship_random(length=1, width=1, max_failures=10000))
        self.all_ships[3].print_ship_stats()
        print(self.add_ship_random(length=1, width=1, max_failures=10000))
        self.all_ships[4].print_ship_stats()
        print(self.add_ship_random(length=1, width=1, max_failures=10000))
        self.all_ships[5].print_ship_stats()
        print(self.add_ship_random(length=1, width=1, max_failures=10000))
        self.all_ships[6].print_ship_stats()

    # For tests only.
    # Test the add_ship method.
    def test_add_ship(self):
        self.add_ship(h0=2, v0=3, dh=3, dv=1)
        self.add_ship(h0=5, v0=5, dh=2, dv=1)
        print(self.add_ship(h0=3, v0=5, dh=2, dv=1))

    # For tests only.
    # Test the method add_ship_with_direction.
    def test_add_ship_with_direction(self):
        # print(self.add_ship_with_direction(h0=4, v0=3, length=3, width=2, direction='d'))  # Exception
        # print(self.add_ship_with_direction(h0=4, v0=3, length=3, width=2, direction='N'))
        # print(self.add_ship_with_direction(h0=4, v0=3, length=3, width=2, direction='S'))
        # print(self.add_ship_with_direction(h0=4, v0=3, length=3, width=2, direction='W'))
        print(self.add_ship_with_direction(h0=4, v0=3, length=3, width=2, direction='E'))
        self.all_ships[0].print_ship_stats()


if __name__ == "__main__":
    # a_ship = Ship(h0=4, v0=5, dh=2, dv=3)
    my_fleet = Fleet(H=6, V=6)
    # my_fleet.test_add_ship()
    # my_fleet.test_add_ship_with_direction()
    # my_fleet.test_add_ship_random()
    # my_fleet.print_fleet_stats()

    my_fleet.place_user_ships()
    comp_fleet = Fleet(H=6, V=6)
    Fleet.create_comp_fleet(comp_fleet, my_fleet)
    comp_fleet.print_fleet_stats()


# End of file
