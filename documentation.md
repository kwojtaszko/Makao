# About the project
This project is a recreation of the card game 'Makao' in python in a terminal. It is played againt a chose number of bots.

# How to play
To start the game just run the main.py using the python interpreter. You will be able to enter your name and choose the numer of enemies. After that, you can play the first game. Type the card index to play it. You can also type 'wait', 'draw' and 'stop makao' for special actions

# Classes
## Card
Represents a single card in a deck.
## Played
The stack of played card
## Deck
The deck of cards from which all the players pull their cards
## Player
Repesents a single player in the game
## Game
Represents a game of makao, with all players and their possible moves, a deck of cards and a stack of played cards.

# Interface
The interface.py file facilitates the communication with the user.

# Tests
The tests are in the test_cards.py file

# Functions in Game
Most of the in-game operations happen inside the Game class.
## draw
player under player_index draws a chosen amount of cards
## playable
checks whether the card can be played now
## play
plays the card from the players hand onto the played cards stack, raises WrongCardError if impossible
## start_draw
draws new cards of each player
## play_game
plays the game and gives the points to winning players, ends when there is only one player left
## makao
allows the player to call makao if he has only one card left
## stop_makao
checks each player, if they have one card and they haven't called makao, they must draw cards
## clear_demand
ends the demand, returns the game to the standard mode of play
## play_demand
allows the human to make his turn, verifies if his inputs are correct and allows him to play a card, draw, wait or stop makao
## play_bot
Makes the turn for a bot player.

# Bot
Part of the task was implementing a bot which would play against the user.
## How it works
Each turn chooses the first card to play if it's possible, draws or waits otherwise. Will call stop Makao if at least one player has one card and hasn't raised Makao. When making a demand will choose the most common value or suit from the bot's cards. When they are of equal rarity the bot will choose the lower one.

# What's missing?
While most of the features are implemented, there are some, which are missing.
## King of hearts
The king of hearts doesn't force the previous player to draw. Instead it just blocks the king of pikes. I tried implementing it, but this card deviates from the standard structure of each player having a turn to play in a fixed order, so it is hard to implement.
## Multiple cards per turn
Only one card can be played per turn. The possibility of playing multiple cards caused many issues with player input, so I had to delete it.
## Bots
The bots aren't very smart. Strategies, such as using queens only when no other card is on hand could be implemented. However, since Makao is mostly a luck-based game there were many situations in which bots won a game against me.
## Difficulty levels
Since this was on optional addition I decided not to focus on it and to work on other features
## Testing
More tests could be made, especially for the Game class.

# Final words
This is probably the largest program I have ever worked on. I spent many hours on it and I am proud of it. Despite the missing features it is a pretty complicated program which runs well.

# PS
I didn't know in which language should I write the documentation. Since the project is in English I decided to be consistent. I hope this is ok.