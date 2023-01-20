from classes import Card, Player, Deck, Played, NotEnoughCardsError
from main import Game
import pytest


def test_card_init_standard():
    card = Card(1, 0)
    assert card.get_suit() == 0
    assert card.get_val() == 1


def test_card_init_string():
    with pytest.raises(TypeError) as e:
        card = Card("bad", "value")
        card
    str(e.value) == "Value and suit must be intigers."


def test_card_init_value_out_of_range():
    with pytest.raises(ValueError) as e:
        card = Card(16, 0)
        card
    str(e.value) == "Value and suit must be within range."


def test_card_init_suit_out_of_range():
    with pytest.raises(ValueError) as e:
        card = Card(0, 20)
        card
    str(e.value) == "Value and suit must be within range."


def test_card_info():
    card = Card(1, 0)
    assert card.info() == "A♣"


def test_card_str():
    card = Card(1, 0)
    assert str(card) == "A♣"


def test_played_init_standard():
    played = Played(Card(1, 0))
    assert played.get_last().info() == "A♣"


def test_played_init_not_a_card():
    with pytest.raises(TypeError) as e:
        played = Played("A♣")
        played
    assert str(e.value) == "first_card argument must be Card type."


def test_played_play():
    played = Played(Card(1, 0))
    played.play(Card(1, 1))
    assert played.get_last().info() == "A◆"


def test_played_play_not_card():
    played = Played(Card(1, 0))
    with pytest.raises(TypeError) as e:
        played.play("a card")
    assert str(e.value) == "card argument must be Card type."


def test_played_covered():
    played = Played(Card(1, 1))
    played.play(Card(2, 1))
    played.play(Card(3, 1))
    played.play(Card(4, 1))
    cards = played.covered()
    assert cards[0].info() == "A◆"
    assert cards[1].info() == "2◆"
    assert cards[2].info() == "3◆"
    assert played.get_last().info() == "4◆"


def test_deck_init(monkeypatch):
    def fake_shuffle(f):
        pass

    monkeypatch.setattr("classes.shuffle", fake_shuffle)
    deck = Deck()
    cards = deck.draw(52)
    for i in range(1, 14):
        for j in range(0, 4):
            card = cards.pop(0)
            assert card.get_val() == i
            assert card.get_suit() == j


def test_deck_not_enough_cards():
    deck = Deck()
    with pytest.raises(NotEnoughCardsError) as e:
        cards = deck.draw(54)
        cards
    assert str(e.value) == "More cards needed in deck to draw."


def test_deck_force_draw():
    deck = Deck()
    cards = deck.draw(54, True)
    assert len(cards) == 52


def test_deck_return_cards():
    deck = Deck()
    card = deck.draw(1)
    deck.return_cards([card])
    assert len(deck.draw(52)) == 52


def test_player_init():
    player = Player("Jurek Ogórek")
    assert player.get_name() == "Jurek Ogórek"
    assert player.get_is_bot() is False


def test_player_init_bot():
    player = Player("Jurek Ogórek", True)
    assert player.get_name() == "Jurek Ogórek"
    assert player.get_is_bot() is True


def test_player_info():
    player = Player("Jurek Ogórek", True)
    assert str(player) == "Jurek Ogórek's cards: []\n"
    assert player.info() == "Jurek Ogórek's cards: []\n"


def test_player_draw_cards():
    player = Player("Jurek Ogórek")
    player.draw_cards([Card(1, 0), Card(2, 0)])
    assert player.my_cards() == "Your cards: \n0: A♣\n1: 2♣\n"
    assert player.info() == "Jurek Ogórek's cards: ['X', 'X']\n"


def test_player_play_card():
    player = Player("Jurek Ogórek")
    player.draw_cards([Card(1, 0), Card(2, 0)])
    card = player.play_card(0)
    assert card.get_val() == 1
    assert card.get_suit() == 0
    assert len(player.get_cards()) == 1


def test_player_most_common_suit():
    player = Player("Jurek Ogórek")
    player.draw_cards([Card(1, 0), Card(2, 0)])
    assert player.most_common_suit() == 0


def test_player_most_common_val_regular():
    player = Player("Jurek Ogórek")
    player.draw_cards([Card(5, 0), Card(5, 1), Card(5, 2), Card(7, 1)])
    assert player.most_common_val() == 5


def test_player_most_common_val_lot_of_function():
    player = Player("Jurek Ogórek")
    player.draw_cards(
        [Card(6, 0), Card(6, 1), Card(2, 2), Card(2, 0), Card(2, 1)]
    )
    assert player.most_common_val() == 6


def test_player_most_common_val_tie():
    player = Player("Jurek Ogórek")
    player.draw_cards([Card(6, 0), Card(6, 1), Card(7, 2), Card(7, 1)])
    assert player.most_common_val() == 6


def test_game_init():
    game = Game(
        [Player("Jurek Ogórek"), Player("Karolina Malina"), Player("Władek")]
    )
    played = game._played
    assert game._current_val == played.get_last().get_val()
    assert game._current_suit == played.get_last().get_suit()
    assert game._to_draw == 0
    assert game._stop_turns == 0
    assert game._demand_maker is None
    assert game._current_player == 0
    assert game._played_turn is False
