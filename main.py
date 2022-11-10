# Game Sea Battle

from Fleet import Fleet
from Board import Board

# Create human player fleet
user_fleet = Fleet(H=6, V=6)    # size can be redefined later
user_fleet.place_user_ships()

# create computer player fleet
comp_fleet = Fleet(H=6, V=6)
Fleet.create_comp_fleet(comp_fleet, user_fleet)

# Boards
user_board = Board(user_fleet)
comp_board = Board(comp_fleet)

# user_board.print_private_view()
# print("")

while True:
    # Computer shoots first
    if user_board.m_fleet.still_fighting():
        print("Player's board before the computer shoots:")
        user_board.print_private_view()
        print("")
        user_board.shoot_randomly()
        print("Player's board after the computer shoots:")
        user_board.print_private_view()
        print("")
        if not user_board.m_fleet.still_fighting():
            print("Computer wins!")
            exit(0)
    else:
        print("Computer wins!")
        exit(0)

    # Player turn
    if comp_board.m_fleet.still_fighting():
        print("Computer's board before the player shoots:")
        comp_board.print_public_view()
        print("")
        while True:
            (coord_h, coord_v) = input("Player's turn. Shoot! Give pos_x and pos_y.\n").split()
            h = int(coord_h)
            v = int(coord_v)

            # True if (h, v) are valid, that is not yet used coordinates
            if comp_board.shoot(h, v):
                break
            else:
                print(f"Coordinates {h} {v} were already used.")
                continue
        print("Computer's board after the player shoots:")
        comp_board.print_public_view()
        print("")

        if not comp_board.m_fleet.still_fighting():
            print("Player wins!")
            exit(0)
    else:
        print("Player wins!")
        exit(0)


# End of file
