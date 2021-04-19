import sys
from math import sqrt
from itertools import count, islice

visited_node = 0
evaluated_node = 0
max_depth = 0
search_depth = 0


def first_move(number_of_tokens):
    # odd
    if number_of_tokens % 2 == 1:
        return [num for num in list(range(int((number_of_tokens + 1) / 2))) if num % 2 == 1]
    else:
        return [num for num in list(range(int((number_of_tokens + 2) / 2))) if num % 2 == 1]


def possible_pick(bag_of_tokens, taken_tokens):
    if len(taken_tokens) == 0:
        return first_move(len(bag_of_tokens))
    else:
        # last moved played
        last_played_number = taken_tokens[-1]
        return [num for num in bag_of_tokens if
                (num % last_played_number == 0 or last_played_number % num == 0)]


def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))


def evaluate_board(player_one, bag_of_tokens, taken_tokens):

    player_one_multiplier = 1 if player_one else -1

    if len(bag_of_tokens) == 0 or len(possible_pick(bag_of_tokens, taken_tokens)) == 0:
        return 1.0 * player_one_multiplier
    else:
        """
            If token 1 is not taken yet, return a value of 0 (because the current state is a relatively neutral
            one for both players)
        """
        if 1 in bag_of_tokens:
            return 0
        else:
            # last moved played
            last_played_number = taken_tokens[-1]

            #
            # If the last move was 1, count the number of the possible successors (i.e., legal moves). If
            # the count is odd, return 0.5; otherwise, return-0.5.
            #
            if last_played_number == 1:
                if len(bag_of_tokens) % 2 == 1:
                    return 0.5 * player_one_multiplier
                else:
                    return -0.5 * player_one_multiplier
            #
            # If last move is a prime, count the multiples of that prime in all possible successors. If the
            # count is odd, return 0.7; otherwise, return-0.7
            #
            elif is_prime(last_played_number):
                number_of_multiple = len([num for num in bag_of_tokens if num % last_played_number == 0])
                if number_of_multiple % 2 == 1:
                    return 0.7 * player_one_multiplier
                else:
                    return -0.7 * player_one_multiplier
            #
            # If the last move is a composite number (i.e., not prime), find the largest prime that can
            # divide last move, count the multiples of that prime, including the prime number itself if it
            # hasn’t already been taken, in all the possible successors. If the count is odd, return 0.6;
            # otherwise, return-0.6
            #
            else:
                number_of_multiple = 0
                temp_bot = bag_of_tokens.copy()
                temp_bot.sort(reverse=True)
                for num in temp_bot:
                    if is_prime(num) and last_played_number % num == 0:
                        number_of_multiple = len([number for number in bag_of_tokens if number % num == 0])
                        break
                if number_of_multiple % 2 == 1:
                    return 0.6 * player_one_multiplier
                else:
                    return -0.6 * player_one_multiplier


def alpha_beta_search(bag_of_tokens, taken_tokens, alpha, beta, max_player, current_depth=0):
    global evaluated_node, visited_node, max_depth, search_depth
    visited_node = visited_node + 1

    # Update the search depth
    if current_depth > search_depth:
        search_depth = current_depth

    move = None

    # If we reached a leaf node
    if current_depth == max_depth or len(possible_pick(bag_of_tokens, taken_tokens)) == 0:
        eval_pos = evaluate_board(not max_player, bag_of_tokens, taken_tokens)
        evaluated_node = evaluated_node + 1
        return eval_pos, move

    # Prepare to expand the state
    possible_moves = possible_pick(bag_of_tokens, taken_tokens)
    new_depth = current_depth + 1

    # Max-value()
    if max_player:
        max_eval = float('-inf')
        for x in possible_moves:
            # Update the state
            temp_bot = bag_of_tokens.copy()
            temp_tt = taken_tokens.copy()
            temp_bot.remove(x)
            temp_bot.sort(reverse=True)
            temp_tt.append(x)

            # Recursively call the alpha_beta_search
            evaluation, move2 = alpha_beta_search(temp_bot, temp_tt, alpha, beta, False, new_depth)
            if evaluation > max_eval:
                max_eval, move = evaluation, x
                alpha = max(alpha, evaluation)
            if beta <= max_eval:
                move = x
                break

        return max_eval, move
    # Min-value()
    else:
        min_eval = float('inf')
        for x in possible_moves:
            # Update the state
            temp_bot = bag_of_tokens.copy()
            temp_tt = taken_tokens.copy()
            temp_bot.remove(x)
            temp_bot.sort(reverse=True)
            temp_tt.append(x)

            # Recursively call the alpha_beta_search
            evaluation, move2 = alpha_beta_search(temp_bot, temp_tt, alpha, beta, True, new_depth)
            if evaluation < min_eval:
                min_eval, move = evaluation, x
                beta = min(beta, evaluation)
            if min_eval <= alpha:
                move = x
                break

        return min_eval, move


def print_output(move, value):
    global evaluated_node, visited_node, max_depth, search_depth
    print("Move:", move)
    print("Value:", value)
    print('Number of node visited:', visited_node)
    print('Number of nodes evaluated:', evaluated_node)
    print('Max depth reached: ', search_depth)

    if visited_node == evaluated_node:
        print('Avg Effective Branching Factor: N/A since the game already ended.')
    else:
        print('Avg Effective Branching Factor:', round(((visited_node - 1) / (visited_node - evaluated_node)), 1))


def main():
    global max_depth

    # get argument list using sys module
    sys.argv
    tokens = list(range(1, int(sys.argv[1]) + 1))
    taken_tokens_integer = int(sys.argv[2])
    taken_tokens = []
    max_depth = None if int(sys.argv[3 + taken_tokens_integer]) == 0 else int(sys.argv[3 + taken_tokens_integer])

    if taken_tokens_integer != 0:
        for i in range(0, taken_tokens_integer):
            x = int(sys.argv[3 + i])
            taken_tokens.append(x)
            tokens.remove(x)

    player = len(taken_tokens) % 2 == 0

    evaluation, move = alpha_beta_search(tokens, taken_tokens, float(-1), float(1), player)
    print_output(move, evaluation)


main()