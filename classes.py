from random import shuffle

# graphical representation of card values
val_dictionary = {
    1: "A",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K"
}

# graphical representation of card suits
suit_dictionary = {
    0: "♣",
    1: "◆",
    2: "♥",
    3: "♠"
}


class NotEnoughCardsError(Exception):
    """raised when there aren't enough cards to draw"""
    pass


class WrongCardError(Exception):
    """raised when the card can't be played"""
    pass


class Card():
    """Represents a single card in a deck"""
    def __init__(self, val: int, suit: int) -> None:
        """Constructor of Card"""
        if type(val) != int or type(suit) != int:
            raise TypeError("Value and suit must be intigers.")
        if val not in range(1, 14) or suit not in range(0, 4):
            raise ValueError("Value and suit must be within range.")
        self._val = val
        self._suit = suit

    def info(self) -> str:
        """returns card as string"""
        return f"{val_dictionary[self._val]}{suit_dictionary[self._suit]}"

    def __str__(self) -> str:
        """string of card"""
        return self.info()

    def get_val(self):
        """returns the value of card"""
        return self._val

    def get_suit(self):
        """returns the value of card"""
        return self._suit


class Played():
    """The stack of played card"""
    def __init__(self, first_card: Card) -> None:
        """Constructor of played, takes the first card in the stack"""
        if type(first_card) is not Card:
            raise TypeError("first_card argument must be Card type.")
        else:
            self._cards = []
            self._cards.append(first_card)

    def play(self, card: Card) -> None:
        """puts the card on stack"""
        if type(card) is not Card:
            raise TypeError("card argument must be Card type.")
        else:
            self._cards.append(card)

    def covered(self) -> list[Card]:
        """
        deletes and returns the cards, so they can be put back into the deck
        """
        return_cards = []
        for i in range(0, len(self._cards) - 1):
            return_cards.append(self._cards.pop(0))
        return return_cards

    def get_last(self) -> Card:
        """the most recent card, which is visible to all players"""
        return self._cards[len(self._cards) - 1]


class Deck():
    """The deck of cards from which all the players pull their cards"""
    def __init__(self) -> None:
        """constructor of deck, creates 52 cards and shuffles them"""
        self._cards = []
        for i in range(1, 14):
            for j in range(0, 4):
                self._cards.append(Card(i, j))
        self.shuffle()

    def shuffle(self) -> None:
        """shuffles the cards"""
        shuffle(self._cards)

    def draw(self, amount: int, force=False) -> list[Card]:
        """deletes and returns the chosen amount of cards from the deck"""
        if amount > len(self._cards) and not force:
            raise NotEnoughCardsError("More cards needed in deck to draw.")
        elif amount > len(self._cards) and force:
            amount = len(self._cards)
        return_cards = []
        for i in range(0, amount):
            return_cards.append(self._cards.pop(0))
        return return_cards

    def return_cards(self, cards: list[Card]) -> None:
        """takes a list of cards as argument and puts them back to the deck"""
        self._cards.extend(cards)


class Player():
    """Repesents a single player in the game"""
    def __init__(self, name: str, is_bot=False) -> None:
        """
        corntructor of player, takes name as argument
        and info on whether the player is a bot
        """
        self._cards = []
        self._name = name
        self._points = 0
        self._is_bot = is_bot
        self._stop = 0
        self._makao = False

    def new_game(self, cards: list[Card]) -> None:
        """should be called before new game, gives new card
        to the player and restets the stop and makao variables"""
        self._cards = cards
        self._stop = 0
        self._makao = False

    def info(self) -> str:
        """displays the name and number of cards of player"""
        hidden_cards = []
        for card in self._cards:
            hidden_cards.append('X')
        return f'{self._name}\'s cards: {hidden_cards}\n'

    def __str__(self) -> str:
        """string of player"""
        return self.info()

    def get_name(self) -> str:
        """returns the name of player"""
        return self._name

    def get_cards(self) -> list[Card]:
        """returns the cards of player"""
        return self._cards

    def get_is_bot(self) -> bool:
        """returns true if the player is a bot"""
        return self._is_bot

    def get_points(self) -> int:
        """returns the points of player"""
        return self._points

    def add_points(self, points):
        """adds point to player"""
        self._points += points

    def get_makao(self) -> bool:
        """returns true if the player has called makao"""
        return self._makao

    def set_makao(self, new_makao: bool):
        """sets if player has called makao"""
        self._makao = new_makao

    def get_stop(self) -> bool:
        """returns stop, for how many turns the player is stopped"""
        return self._stop

    def set_stop(self, new_stop: bool):
        """sets fo how long the player must stop"""
        self._stop = new_stop

    def my_cards(self) -> str:
        """returns the string with cards of player"""
        str_cards = ""
        for i in range(0, len(self._cards)):
            str_cards += f'{i}: {str(self._cards[i])}\n'
        return f'Your cards: \n{str_cards}'

    def play_card(self, index: int) -> Card:
        """deletes and returns card of the chosen index"""
        if index not in range(0, len(self._cards)):
            raise ValueError("Wrong card index.")
        else:
            return self._cards.pop(index)

    def draw_cards(self, cards: list[Card]) -> None:
        """adds the list of cards given as parameter to the player's cards"""
        self._cards.extend(cards)

    def most_common_suit(self):
        """returns the suit which occurs most commonly in players cards"""
        suit_occurences = [0, 0, 0, 0]
        for card in self._cards:
            suit_occurences[card.get_suit()] += 1
        return suit_occurences.index(max(suit_occurences))

    def most_common_val(self):
        """returns the value which occurs most commonly in players cards"""
        val_occurences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for card in self._cards:
            val_occurences[card.get_val()] += 1
        vals_to_demand = val_occurences[5:10:]
        return vals_to_demand.index(max(vals_to_demand)) + 5
