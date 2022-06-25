MAX_COORDS: tuple = (480, 640)


class GameLogic:

    def calculate_position_of_racket(self, coords: tuple, aspect_ratio: float) -> tuple:
        """
        Calculates the position of the racket based on the coordinates of the hand.
        :param coords:
        :param aspect_ratio:
        :return:
        """

        # max x and y coordinates of the hand 763 576
        def calculate_coords(coord: int, max_value: int) -> float:
            # if coord < 0: return 0
            # if coord > max_value: return max_value/10
            # if 0 < coord < max_value:
            return coord / max_value * 10

        x = calculate_coords(coords[0], MAX_COORDS[0]) - 5
        y = 15 - calculate_coords(coords[1], MAX_COORDS[1])

        print(x, y)

        return x, y, -20
