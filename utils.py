import numpy as np

def get_neighboors(board, x, y):
    """Return coordinate of all neighoors
    that are not "0"

    Args:
        board (np 2D array): the state of the game
        x (int): x coordinate to check
        y (int): y coordinate to check
    """
    out = []

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:

            if j == 0 and i == 0:
                continue

            n_x, n_y = x + i, y + j

            if n_x < 0 or n_x > board.shape[1] - 1:
                continue

            if n_y < 0 or n_y > board.shape[0] - 1:
                continue

            if board[y + j, x + i] != 0:
                out.append(board[y + j, x + i])

    return out


def color_from_code(code):
    """Generate a color based on a simple code

    Args:
        code (int): an integer going from 1 to 999

    Returns:
        [tuple]: the rgb color code 
    """

    if code == 0:
        return (255, 255, 255)

    assert code < 1000

    color = [0, 0, 0]

    for i, div in enumerate([100, 10, 1]):

        digit = (code // div) % 10
        color[i] = (255 // 9) * digit

    return color


def get_mean_color_code(list_code):

    # colors = [color_from_code(code) for code in list_code]

    # mean_color = np.mean(colors, dtype=int, axis=0)
    n_codes = len(list_code)

    code = 0
    

    for div in [100, 10, 1]:

        _sum = 0

        for c in list_code:
            
            digit = (c // div) % 10
            _sum += digit

        code += div * round(_sum / n_codes)

    # return 1
    return code


