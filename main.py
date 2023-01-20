import interface
from classes import (
    Player,
    Deck,
    Played,
    NotEnoughCardsError,
    WrongCardError
)

DECK_SIZE = 5


class Game:
    """
    Represents a game of makao, with all
    players and their possible moves, a deck
    of cards and a stack of played cards
    """

    def __init__(self, players: list[Player]) -> None:
        """
        Constructor of game, takes the players as argumnet,
        creates deck and played, sets all variables
        """
        self._players = players
        self._deck = Deck()
        first_card = self._deck.draw(1)[0]
        while first_card.get_val() not in range(5, 11):
            self._deck.return_cards([first_card])
            first_card = self._deck.draw(1)[0]
        self._played = Played(first_card)
        self._current_val = first_card.get_val()
        self._current_suit = first_card.get_suit()
        self._to_draw = 0
        self._stop_turns = 0
        self._demand_maker = None
        self._current_player = 0
        self._played_turn = False

    def draw(self, player_index: int, amount: int):
        """player under player_index draws a chosen amount of cards"""
        try:
            if amount > 1:
                interface.display_draw_cards_multiple(
                    self._players[player_index], amount
                )
            else:
                interface.display_draw_card_single(self._players[player_index])
            self._players[player_index].draw_cards(self._deck.draw(amount))
        except NotEnoughCardsError:
            self._deck.return_cards(self._played.covered())
            self._players[player_index].draw_cards(
                self._deck.draw(amount, True)
            )
            raise

    def is_playable(self, player_index: int, card_index: int) -> bool:
        """checks whether the card can be played now"""
        condition1 = (
            self._players[player_index].get_cards()[card_index].get_val()
            != self._current_val
        )
        condition2 = (
            self._players[player_index].get_cards()[card_index].get_suit()
            != self._current_suit
        )
        condition3 = self._players[player_index].get_cards()[
            card_index
        ].get_val() != 12
        condition4 = self._current_val != 12
        condition5 = (
            self._current_val == -1
            and self._players[player_index].get_cards()[
                card_index
            ].get_val() == 1
        )
        condition6 = (
            self._current_suit == -1
            and self._players[player_index].get_cards()[
                card_index
            ].get_val() == 11
        )
        condition7 = self._to_draw != 0
        condition8 = (
            self._played.get_last().get_val() in [2, 3] and self._players[
                player_index
            ].get_cards()[card_index].get_val() in [2, 3]
        )
        condition9 = (
            self._played.get_last().get_val() == 13
            and self._players[player_index].get_cards()[
                card_index
            ].get_val() == 13
        )
        condition10 = (
            self._stop_turns != 0
            and self._players[player_index].get_cards()[
                card_index
            ].get_val() != 4
        )
        return not (
            (
                condition1
                and condition2
                and condition3
                and condition4
                and not condition5
                and not condition6
            )
            or (condition7 and not condition8 and not condition9)
            or condition10
        )

    def play(self, player_index: int, card_index: int, demand=None) -> None:
        """
        plays the card from the players hand
        onto the played cards stack, raises WrongCardError if impossible
        """
        if not self.is_playable(player_index, card_index):
            raise WrongCardError("You can't play this card right now. ")
        else:
            interface.display_card_played(
                self._players[player_index],
                self._players[player_index].get_cards()[card_index],
            )
            if (
                self._played.get_last().get_val() == 13
                and self._players[
                    player_index
                ].get_cards()[card_index].get_val() == 13
            ):
                self._to_draw = 0
            self._played.play(
                self._players[player_index].play_card(card_index)
            )
            if self._demand_maker is None:
                self._current_suit = self._played.get_last().get_suit()
                self._current_val = self._played.get_last().get_val()
            if self._played.get_last().get_val() == 2:
                self._to_draw += 2
            elif self._played.get_last().get_val() == 3:
                self._to_draw += 3
            elif (
                self._played.get_last().get_val() == 13
                and self._played.get_last().get_suit() == 3
            ):
                self._to_draw += 5
            elif self._played.get_last().get_val() == 4:
                self._stop_turns += 1
            elif self._played.get_last().get_val() == 11:
                self._current_val = demand
                self._current_suit = -1
                self._demand_maker = player_index
            elif self._played.get_last().get_val() == 1:
                self._current_val = -1
                self._current_suit = demand
                self._demand_maker = player_index

    def start_draw(self):
        """draws new cards of each player"""
        for player in self._players:
            player.new_game(self._deck.draw(DECK_SIZE))

    def play_game(self) -> list[Player]:
        """
        plays the game and gives the points
        to winning players, ends when there is
        only one player left
        """
        points_to_get = len(self._players) - 1
        not_over = True
        self.start_draw()
        interface.display_game_start()
        while not_over:
            interface.display_new_turn()
            for player in self._players:
                if len(player.get_cards()) != 0:
                    if player.get_is_bot():
                        self.play_bot()
                    else:
                        self.play_human()
                        if len(
                            self._players[self._current_player].get_cards()
                        ) == 1:
                            self.makao()
                    if len(
                        self._players[self._current_player].get_cards()
                    ) == 0:
                        interface.display_finish(
                            self._players[self._current_player]
                        )
                        self._players[self._current_player].add_points(
                            points_to_get
                        )
                        points_to_get -= 1
                        if points_to_get == 0:
                            interface.display_game_over()
                            return self._players
                else:
                    self.clear_demand(True)
                self._current_player += 1
                if self._current_player >= len(self._players):
                    self._current_player = 0

    def makao(self):
        """
        allows the player to call
        makao if he has only one card left
        """
        ask = interface.get_input(
            "Type 'makao' to signify that you have one card left: "
        )
        if ask == "makao":
            self._players[self._current_player].set_makao(True)

    def stop_makao(self):
        """
        checks each player, if they have one
        card and they haven't called makao, they must draw cards
        """
        interface.display_stop_makao(self._players[self._current_player])
        for i in range(0, len(self._players)):
            if (
                self._players[i].get_makao() is False
                and len(self._players[i].get_cards()) == 1
            ):
                interface.makao_draw(self._players[i])
                self.draw(i, 5)

    def clear_demand(self, played_demand):
        """
        ends the demand, returns the game to the standard mode of play
        """
        if self._demand_maker == self._current_player and played_demand:
            self._demand_maker = None
            self._current_suit = self._played.get_last().get_suit()
            self._current_val = self._played.get_last().get_val()

    def play_human(self):
        """
        allows the human to make his turn,
        verifies if his inputs are correct
        and allows him to play a card, draw, wait or stop makao
        """
        if self._players[self._current_player].get_stop() > 0:
            self._players[self._current_player].set_stop(
                self._players[self._current_player].get_stop() - 1
            )
            interface.display_skip_turn(self._players[self._current_player])
            return
        played_demand = True
        while True:
            try:
                interface.display_state(
                    self._players, self._current_player, self._played
                )
                if self._to_draw > 0:
                    interface.display_force_draw(self._to_draw)
                elif self._stop_turns > 0:
                    interface.display_stop(self._stop_turns)
                elif self._current_val == -1:
                    interface.display_suit_demand(self._current_suit)
                elif self._current_suit == -1:
                    interface.display_val_demand(self._current_val)
                else:
                    interface.display_regular()
                ask = interface.get_input("Your move: ")
                if ask == "draw" and self._stop_turns == 0:
                    self._players[self._current_player].set_makao(False)
                    if self._to_draw > 0:
                        self.draw(self._current_player, self._to_draw)
                        self._to_draw = 0
                        self.play_human()
                        return
                    else:
                        self.draw(self._current_player, 1)
                elif ask.isnumeric():
                    if int(ask) not in range(
                        0, len(self._players[self._current_player].get_cards())
                    ):
                        raise ValueError(
                            "Please choose a correct card number."
                        )
                    elif (
                        self._players[self._current_player]
                        .get_cards()[int(ask)]
                        .get_val()
                        == 11
                    ):
                        val = interface.input_get_val()
                        self.play(self._current_player, int(ask), val)
                        played_demand = False
                    elif (
                        self._players[self._current_player]
                        .get_cards()[int(ask)]
                        .get_val()
                        == 1
                    ):
                        suit = interface.input_get_suit()
                        self.play(self._current_player, int(ask), suit)
                        played_demand = False
                    else:
                        self.play(self._current_player, int(ask))
                elif ask == "wait" and self._stop_turns > 0:
                    self._players[self._current_player].set_stop(
                        self._players[self._current_player].get_stop()
                        + self._stop_turns
                        - 1
                    )
                    self._stop_turns = 0
                    interface.display_skip_turn(
                        self._players[self._current_player]
                    )
                elif ask == "stop makao":
                    self.stop_makao()
                    self.play_human()
                    return
                else:
                    raise ValueError(
                        "Incorrect input, try typing something else."
                    )
            except NotEnoughCardsError:
                interface.display_not_enough_cards()
                self._to_draw = 0
                break
            except Exception as e:
                interface.display(e)
            else:
                self.clear_demand(played_demand)
                break

    def play_bot(self):
        """
        Makes the turn for a bot player, chooses the first
        card to play if it's possible, draws or waits otherwise.
        Will call stop Makao if at least one player
        has one card and hasn't raised Makao.
        When making a demand will choose the most
        common value or suit from the bot's cards.
        When they are of equal rarity the bot will choose the lower one.
        """
        for player in self._players:
            if player.get_makao() is False and len(player.get_cards()) == 1:
                self.stop_makao()
                break
        try:
            played_demand = True
            if self._players[self._current_player].get_stop() > 0:
                self._players[self._current_player].set_stop(
                    self._players[self._current_player].get_stop() - 1
                )
                interface.display_skip_turn(
                    self._players[self._current_player]
                )
                return
            for i in range(0, len(self._players[
                self._current_player
            ].get_cards())):
                if self.is_playable(self._current_player, i):
                    if (
                        self._players[
                            self._current_player
                        ].get_cards()[i].get_val()
                        == 1
                    ):
                        self.play(
                            self._current_player,
                            i,
                            self._players[
                                self._current_player
                            ].most_common_suit()
                        )
                        played_demand = False
                    elif (
                        self._players[
                            self._current_player
                        ].get_cards()[i].get_val() == 11
                    ):
                        self.play(
                            self._current_player,
                            i,
                            self._players[
                                self._current_player
                            ].most_common_val()
                        )
                        played_demand = False
                    else:
                        self.play(self._current_player, i)
                    self.clear_demand(played_demand)
                    if len(self._players[
                        self._current_player
                    ].get_cards()) == 1:
                        self._players[self._current_player].set_makao(True)
                        interface.display_call_makao(
                            self._players[self._current_player]
                        )
                    return
            if self._stop_turns > 0:
                self._players[self._current_player].set_stop(
                    self._players[self._current_player].get_stop()
                    + self._stop_turns
                    - 1
                )
                self._stop_turns = 0
                interface.display_skip_turn(
                    self._players[self._current_player]
                )
            elif self._to_draw > 0:
                self._players[self._current_player].set_makao(False)
                self.draw(self._current_player, self._to_draw)
                self._to_draw = 0
                self.play_bot()
            else:
                self._players[self._current_player].set_makao(False)
                self.draw(self._current_player, 1)
            self.clear_demand(played_demand)
        except NotEnoughCardsError:
            self._to_draw = 0


def generate_players(name: str, opponents: int) -> list[Player]:
    """generates players before the game"""
    players = [Player(name)]
    for i in range(1, opponents + 1):
        players.append(Player(f"opponent{i}", True))
    return players


def main():
    """
    The main function.
    Request number of players from user, starts the game,
    after the game shows the score and asks the user if he wants to play again.
    If yes, starts the game again. If no,
    """
    players = generate_players(
        interface.input_name(),
        interface.input_opponent_number()
    )
    new_game = True
    while new_game:
        game = Game(players)
        players = game.play_game()
        interface.display_points(players)
        ask = interface.input_play_again()
        if ask == "y":
            new_game = True
        else:
            new_game = False
    interface.display_winner(players)


if __name__ == "__main__":
    main()
