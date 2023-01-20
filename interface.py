from classes import (
    Card,
    Player,
    Played,
    val_dictionary,
    suit_dictionary
)


def get_input(text):
    """gets input from user"""
    ask = input(text)
    return ask


def display(text):
    """displays text"""
    print(text)


def display_game_start():
    """signifies the start of a game"""
    print("Start game!")


def display_new_turn():
    """signifies new turn"""
    print("New turn!")


def display_finish(player: Player):
    """signifies a player has no cards left and has ended the game"""
    print(f"{player.get_name()}: Makao over!")


def display_game_over():
    """signifies the game is over"""
    print("Game over!")


def display_card_played(player: Player, card: Card):
    print(f"{player.get_name()} played {card}.")


def input_get_val() -> int:
    """gets a value to demand from player"""
    to_display = list(range(5, 11))
    print(to_display)
    while True:
        try:
            val = input("Please select a value: ")
            if int(val) not in range(5, 11):
                raise ValueError
        except ValueError:
            print("Please choose a correct value.")
        else:
            return int(val)


def input_get_suit() -> int:
    """gets a suit to demand from player"""
    print(suit_dictionary)
    while True:
        try:
            suit = input("Choose suit by typing the corresponding number: ")
            if int(suit) not in range(0, 4):
                raise ValueError
        except ValueError:
            print("Please choose a correct suit.")
        else:
            return int(suit)


def display_state(
    players: list[Player], current_player: int, played: Played
) -> str:
    """gets a value to demand from player"""
    print_string = ""
    for i in range(0, len(players)):
        if i != current_player:
            print_string += players[i].info()
    print_string += players[current_player].my_cards()
    print_string += f"Newest card: {str(played.get_last())}"
    print(print_string)


def display_skip_turn(player: Player):
    """signifies the player skips his turn"""
    print(f"{player.get_name()} skips turn.")


def display_force_draw(to_draw: int):
    """signifies the player must draw a card"""
    string = (
        f"""You must play a card which will force
the next player to draw or draw {to_draw} cards."""
    )
    string = string.replace("\n", " ")
    print(string)


def display_stop(stop_turns: int):
    """signifies the player must wait"""
    string = (
        f"""Another player has played a stop card against you.
Play a stop card or type 'wait' to wait for {stop_turns} turns."""
    )
    string = string.replace("\n", " ")
    print(string)


def display_suit_demand(current_suit: int):
    """signifies the player must fullfill a suit demand"""
    string = (
        f"""A demand has been made. You must play
{suit_dictionary[current_suit]}
or a suit demand card to change the demand."""
    )
    string = string.replace("\n", " ")
    print(string)


def display_val_demand(current_val: int):
    """signifies the player must fullfill a value demand"""
    string = (
        f"""A demand has been made. You must play
{val_dictionary[current_val]}
or a value demand card to change the demand."""
    )
    string = string.replace("\n", " ")
    print(string)


def display_regular():
    """signifies start of regular turn"""
    print("Your turn, pick a card to play or type 'draw' to draw a card.")


def display_draw_cards_multiple(player: Player, to_draw: int):
    """signifies a player draws multiple cards"""
    print(f"{player.get_name()} draws {to_draw} cards.")


def display_draw_card_single(player: Player):
    """signifies a player draws a single card"""
    print(f"{player.get_name()} draws a card.")


def display_not_enough_cards():
    """displayed when there aren't enough cards for the player to draw"""
    print("There weren't enough cards, so you didn't get the full amount.")


def display_stop_makao(player: Player):
    """signifies a player has called stop makao"""
    print(f"{player.get_name()}: Stop Makao!")


def makao_draw(player: Player):
    """signifies a player must draw 5 cards, because he didn't say makao"""
    string = (
        f"""{player.get_name()} didn't signal makao,
they have to draw 5 cards now."""
    )
    string = string.replace("\n", " ")
    print(string)


def display_call_makao(player: Player):
    """signifies a player calls makao"""
    print(f"{player.get_name()}: Makao!")


def display_points(players: list[Player]):
    """displays the points of each player"""
    players.sort(key=lambda h: h.get_points())
    for player in players:
        print(f"{player.get_name()}: {player.get_points()} points.")


def display_winner(players: list[Player]):
    """displays the winner of the game"""
    players.sort(key=lambda h: h.get_points())
    print(f"The winner is: {players[len(players)-1].get_name()}")


def input_play_again():
    """asks user if they wish to play again"""
    string = ("""Do you want to play again? Type 'y'
to play again, type anything else to stop:
    """)
    string = string.replace("\n", " ")
    ask = input(string)
    return ask


def input_name():
    """asks user for name"""
    while True:
        ask = input("Enter your name: ")
        if ask.strip():
            return ask
        print("Try again.")


def input_opponent_number():
    """asks user for number of opponents"""
    while True:
        ask = input("How many opponents do you want? Pick from 1 to 3: ")
        if ask.isnumeric() and int(ask) in range(1, 4):
            return int(ask)
        print("Try again.")
