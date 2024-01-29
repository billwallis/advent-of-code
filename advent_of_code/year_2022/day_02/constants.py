"""
Constants to use in the solutions.
"""

ENCODING_OPPONENT = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}
ENCODING_PLAYER_1 = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
ENCODING_PLAYER_2 = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}
SCORES = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
    "lose": 0,
    "draw": 3,
    "win": 6,
}
DEFEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}
