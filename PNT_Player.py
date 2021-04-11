import sys
from PNT import play_PNT


def main():
    # get argument list using sys module
    sys.argv

    tokens = list(range(1, int(sys.argv[1]) + 1))
    taken_tokens_integer = int(sys.argv[2])
    taken_tokens = []
    depth = None if int(sys.argv[3 + taken_tokens_integer]) == 0 else int(sys.argv[3 + taken_tokens_integer])

    if taken_tokens_integer != 0:
        for i in range(0, taken_tokens_integer - 1):
            x = int(sys.argv[taken_tokens_integer + i])
            taken_tokens.append(x)
            tokens.remove(x)

    done = False
    #bag_of_tokens, taken_tokens = [1, 2, 3, 4, 5, 6, 7], []
    #player = False
    #evaluation = 0
    #depth = None
    while not done:
        player = len(taken_tokens) % 2 == 0
        evaluation, move = play_PNT(tokens, taken_tokens, depth, float('-inf'), float('inf'), player)
        if depth is not None:
            depth = depth - 1
        if move is None:
            break
        tokens.remove(move)
        taken_tokens.append(move)
    print(taken_tokens, "MIN win" if player else "MAX win", evaluation)


main()
