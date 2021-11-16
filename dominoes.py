import random


def create_pieces(pieces):
    for i in range(7):
        for j in range(i, 7):
            pieces.append([i, j])
    random.shuffle(pieces)


def find_first_piece(computer, player):
    for i in reversed(range(7)):
        if [i, i] in computer:
            return computer.pop(computer.index([i, i]))
        if [i, i] in player:
            return player.pop(player.index([i, i]))
    return None


def distribute_pieces(deck, player, start_pieces):
    player.extend(deck[:start_pieces])
    for item in player:
        deck.remove(item)


def initialize_game(deck, computer, player, snake):
    while True:
        create_pieces(deck)
        distribute_pieces(deck, computer, start_pieces=7)
        distribute_pieces(deck, player, start_pieces=7)
        first_piece = find_first_piece(computer, player)
        if len(computer) == len(player):
            deck.clear()
            player.clear()
            computer.clear()
            snake.clear()
            continue
        snake.append(first_piece)
        break


def print_hand(hand):
    for i, piece in enumerate(hand):
        print(f'{i + 1}: {piece}')


def print_snake(domino_snake):
    if len(domino_snake) > 6:
        right_part = str(domino_snake[0:3])[1:- 1]
        left_part = str(domino_snake[-3:])[1: - 1]
        snake = f'{right_part}...{left_part}'
    else:
        snake = str(domino_snake)[1: - 1]
    print(snake)


def print_status(player_pieces, computer_pieces, turn_indicator, players, is_over):
    if is_over:
        if len(player_pieces) == 0 or len(player_pieces) < len(computer_pieces):
            status = 'The game is over. You won!'
        elif len(computer_pieces) == 0 or len(computer_pieces) < len(player_pieces):
            status = 'The game is over. The computer won!'
        else:
            status = "The game is over. It's a draw!"
    elif players[turn_indicator] == 'computer':
        status = 'Computer is about to make a move. Press Enter to continue...'
    else:
        status = "It's your turn to make a move. Enter your command."
    print(f'Status: {status}')


def print_interface(deck, computer, player, snake, turn, players, is_over):
    print('=' * 70)
    print(f'Stock size: {len(deck)}')
    print(f'Computer pieces: {len(computer)}')
    print()
    print_snake(snake)
    print()
    print('Your pieces:')
    print_hand(player)
    print_status(player, computer, turn, players, is_over)


def check_input(pieces):
    input_string = input()
    if not input_string.lstrip("-").isdigit():
        print('Invalid input. Please try again.')
        return check_input(pieces)
    move = int(input_string)
    if abs(move) > pieces:
        print('Invalid input. Please try again.')
        return check_input(pieces)
    return move


def check_snake(snake):
    for i in range(7):
        if str(snake).count(str(i)) == 9:
            return True
    return False


def check_deck(snake, computer, player, deck):
    is_possible_move = True
    if not deck:
        for piece in computer:
            if check_left_side(snake, piece) or check_right_side(snake, piece):
                is_possible_move = False
        for piece in player:
            if check_left_side(snake, piece) or check_right_side(snake, piece):
                is_possible_move = False
    else:
        is_possible_move = False
    return is_possible_move


def check_left_side(domino_snake, players_piece):
    end = domino_snake[0][0]
    return end in players_piece


def check_right_side(domino_snake, players_piece):
    end = domino_snake[-1][1]
    return end in players_piece


def turn_piece(domino_snake, piece, side):
    if side > 0:
        if domino_snake[-1][1] != piece[0]:
            piece.reverse()
    else:
        if domino_snake[0][0] != piece[1]:
            piece.reverse()


def player_move(player_pieces, stock_pieces, domino_snake):
    while True:
        move = check_input(len(player_pieces))
        player_piece = player_pieces[abs(move) - 1]
        if move == 0:
            if len(stock_pieces) != 0:
                player_pieces.append(stock_pieces.pop(random.randint(0, len(stock_pieces) - 1)))
            break
        elif move < 0 and check_left_side(domino_snake, player_piece):
            player_pieces.remove(player_piece)
            turn_piece(domino_snake, player_piece, move)
            domino_snake.insert(0, player_piece)
            break
        elif check_right_side(domino_snake, player_piece):
            player_pieces.remove(player_piece)
            turn_piece(domino_snake, player_piece, move)
            domino_snake.append(player_piece)
            break
        else:
            print('Illegal move. Please try again.')
            continue


def computer_move(player_pieces, stock_pieces, domino_snake):
    input()
    movies = []
    movies.extend(range(-len(player_pieces), 0))
    movies.extend(range(1, len(player_pieces) + 1))
    movies.append(0)
    for move in movies:
        player_piece = player_pieces[abs(move) - 1]
        if move == 0:
            if len(stock_pieces) != 0:
                player_pieces.append(stock_pieces.pop(random.randint(0, len(stock_pieces) - 1)))
            break
        elif move < 0 and check_left_side(domino_snake, player_piece):
            player_pieces.remove(player_piece)
            turn_piece(domino_snake, player_piece, move)
            domino_snake.insert(0, player_piece)
            break
        elif check_right_side(domino_snake, player_piece):
            player_pieces.remove(player_piece)
            turn_piece(domino_snake, player_piece, move)
            domino_snake.append(player_piece)
            break


def calculate_numbers(computer_pieces, domino_snake):
    _weight_numbers = dict()
    visible_piece = []
    visible_piece.extend(computer_pieces)
    visible_piece.extend(domino_snake)
    for i in range(7):
        count = 0
        for item in visible_piece:
            if item == [i, i]:
                count += 2
            elif i in item:
                count += 1
        _weight_numbers[i] = count
    return _weight_numbers


def weight_hand(weight_numbers, computer_pieces):
    weight_pieces = dict()
    for index, item in enumerate(computer_pieces):
        weight_piece = weight_numbers[item[0]] + weight_numbers[item[1]]
        weight_pieces[index] = weight_piece

    sorted_keys = sorted(weight_pieces, key=weight_pieces.get)  # [1, 3, 2]
    computer_sort = list(computer_pieces)
    for i, val in enumerate(sorted_keys):
        computer_pieces[i] = computer_sort[val]
    computer_pieces.reverse()


def computer_ai_move(computer_pieces, stock_pieces, domino_snake):
    input()
    weight_numbers = calculate_numbers(computer_pieces, domino_snake)
    weight_hand(weight_numbers, computer_pieces)
    for piece in computer_pieces:
        if check_left_side(domino_snake, piece):
            computer_pieces.remove(piece)
            turn_piece(domino_snake, piece, side=-1)
            domino_snake.insert(0, piece)
            break
        if check_right_side(domino_snake, piece):
            computer_pieces.remove(piece)
            turn_piece(domino_snake, piece, side=1)
            domino_snake.append(piece)
            break
    else:
        if len(stock_pieces) != 0:
            computer_pieces.append(stock_pieces.pop(random.randint(0, len(stock_pieces) - 1)))


def game():
    stock_pieces, computer_pieces, player_pieces, domino_snake = [], [], [], []
    players = ('player', 'computer')

    initialize_game(deck=stock_pieces, computer=computer_pieces, player=player_pieces, snake=domino_snake)
    turn_indicator = 1 if len(player_pieces) < len(computer_pieces) else 0

    while True:
        is_over = check_snake(domino_snake) \
                  or check_deck(domino_snake, computer_pieces, player_pieces, stock_pieces) \
                  or len(computer_pieces) == 0 or len(player_pieces) == 0
        print_interface(deck=stock_pieces,
                        computer=computer_pieces,
                        player=player_pieces,
                        snake=domino_snake,
                        turn=turn_indicator,
                        players=players,
                        is_over=is_over)
        if is_over:
            break
        if players[turn_indicator] == 'player':
            player_move(player_pieces=player_pieces, stock_pieces=stock_pieces, domino_snake=domino_snake)
        else:
            computer_ai_move(computer_pieces=computer_pieces, stock_pieces=stock_pieces, domino_snake=domino_snake)
        turn_indicator = (turn_indicator + 1) % len(players)


game()
