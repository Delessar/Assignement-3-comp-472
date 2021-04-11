from math import sqrt
from itertools import count, islice


def best_move(player_one, bag_of_tokens, taken_tokens):
    possible_moves = possible_pick(bag_of_tokens, taken_tokens)
    print("nodes evaluated", len(possible_moves), possible_moves)
    best_pick = None
    best_pick_eval = None
    for x in possible_moves:
        temp_bot = bag_of_tokens.copy()
        temp_tt = taken_tokens.copy()
        temp_bot.remove(x)
        temp_tt.append(x)
        position_evaluation = evaluate_board(not player_one, temp_bot, temp_tt)
        if best_pick_eval is None:
            best_pick_eval = position_evaluation
            best_pick = x
        elif player_one and (position_evaluation > best_pick_eval):
            best_pick_eval = position_evaluation
            best_pick = x
        elif not player_one and (position_evaluation < best_pick_eval):
            best_pick_eval = position_evaluation
            best_pick = x
    return best_pick


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

visited_node = 0
evaluated_node = 0

def play_PNT(bag_of_tokens, taken_tokens, depth, alpha, beta, player_one):
    global evaluated_node, visited_node
    print("evaluated_node ", evaluated_node)
    print("visited_node ", visited_node)
    move = None
    if depth == 0 or len(possible_pick(bag_of_tokens, taken_tokens)) == 0:
        eval_pos = evaluate_board(not player_one, bag_of_tokens, taken_tokens)
        evaluated_node = evaluated_node + 1
        # print("finish ", taken_tokens, " Win for player: ", "MAX" if not player_one else "MIN", eval_pos)
        return eval_pos, move

    if player_one:
        max_eval = float('-inf')
        possible_moves = possible_pick(bag_of_tokens, taken_tokens)
        for x in possible_moves:
            visited_node = visited_node + 1
            temp_bot = bag_of_tokens.copy()
            temp_tt = taken_tokens.copy()
            temp_bot.remove(x)
            temp_bot.sort(reverse=True)
            temp_tt.append(x)
            new_depth = None if depth is None else depth - 1
            evaluation, move2 = play_PNT(temp_bot, temp_tt, new_depth, alpha, beta, False)
            if evaluation > max_eval:
                max_eval, move = evaluation, x
                alpha = max(alpha, evaluation)
            #max_eval = max(max_eval, evaluation)
            #alpha = max(alpha, evaluation)
            if beta <= max_eval:
                move = x
                break
        return max_eval, move

    else:
        min_eval = float('inf')
        possible_moves = possible_pick(bag_of_tokens, taken_tokens)
        for x in possible_moves:
            visited_node = visited_node + 1
            temp_bot = bag_of_tokens.copy()
            temp_tt = taken_tokens.copy()
            temp_bot.remove(x)
            temp_bot.sort(reverse=True)
            temp_tt.append(x)
            new_depth = None if depth is None else depth - 1
            evaluation, move2 = play_PNT(temp_bot, temp_tt, new_depth, alpha, beta, True)
            if evaluation < min_eval:
                min_eval, move = evaluation, x
                beta = min(beta, evaluation)
            #min_eval = min(min_eval, evaluation)
            #beta = min(beta, evaluation)
            if min_eval <= alpha:
                break
        return min_eval, move