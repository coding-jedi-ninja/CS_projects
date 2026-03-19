# hangman.py
# Team Members: <Name 1>, <Name 2>, <Name 3>
# NU ID(s): <ID 1>, <ID 2>, <ID 3>
# Course: CS 5001 / 5003 — Spring 2026

"""
Hangman Game for CS 5001 / 5003

This program implements a terminal-based Hangman game.
It follows the assignment requirements:
1. Includes helper functions with docstrings
2. Includes example calls in comments
3. Uses a main game loop
4. Uses an entry point with replay support

Extra features added:
- Colours
- Simple sound cues
- Changing themes
"""

# -----------------------------
# Imports
# -----------------------------
import os
import sys
import time


# -----------------------------
# Global Settings
# -----------------------------
MAX_WRONG = 6
USE_COLOURS = True
USE_SOUND = True


# -----------------------------
# Theme Data
# -----------------------------
# These themes use ANSI escape codes for terminal colours.
# If a terminal does not support colours, turn USE_COLOURS to False.
THEMES = [
    {
        "name": "Forest",
        "title": "\033[92m",      # bright green
        "text": "\033[32m",       # green
        "good": "\033[96m",       # cyan
        "bad": "\033[91m",        # red
        "warn": "\033[93m",       # yellow
        "reset": "\033[0m"
    },
    {
        "name": "Ocean",
        "title": "\033[94m",      # blue
        "text": "\033[36m",       # cyan-ish
        "good": "\033[92m",       # green
        "bad": "\033[95m",        # magenta
        "warn": "\033[93m",       # yellow
        "reset": "\033[0m"
    },
    {
        "name": "Sunset",
        "title": "\033[95m",      # magenta
        "text": "\033[33m",       # orange/yellow
        "good": "\033[92m",       # green
        "bad": "\033[91m",        # red
        "warn": "\033[96m",       # cyan
        "reset": "\033[0m"
    }
]


# -----------------------------
# Utility Functions
# -----------------------------
def clear_screen():
    """
    Clears the terminal screen for a cleaner game experience.
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_theme(game_number):
    """
    Returns a theme dictionary based on the game number so that
    the theme changes across repeated games.

    Parameters:
        game_number (int): The number of the current game session.

    Returns:
        dict: A dictionary representing the selected theme.
    """
    return THEMES[(game_number - 1) % len(THEMES)]


def colour_text(text, colour_code, theme):
    """
    Wraps text in ANSI colour codes if colours are enabled.

    Parameters:
        text (str): The text to colour.
        colour_code (str): The ANSI colour code.
        theme (dict): Current theme dictionary.

    Returns:
        str: Coloured text if colours are enabled, else plain text.
    """
    if USE_COLOURS:
        return f"{colour_code}{text}{theme['reset']}"
    return text


def play_sound(sound_type):
    """
    Plays a simple sound cue for user feedback.

    The function tries to use winsound on Windows.
    On other systems, it falls back to the terminal bell.

    Parameters:
        sound_type (str): Type of sound to play.
                          Expected values: 'good', 'bad', 'win', 'lose'
    """
    if not USE_SOUND:
        return

    try:
        if os.name == "nt":
            import winsound

            if sound_type == "good":
                winsound.Beep(900, 150)
            elif sound_type == "bad":
                winsound.Beep(400, 200)
            elif sound_type == "win":
                winsound.Beep(900, 150)
                winsound.Beep(1100, 150)
                winsound.Beep(1300, 200)
            elif sound_type == "lose":
                winsound.Beep(500, 200)
                winsound.Beep(350, 250)
        else:
            # Terminal bell fallback
            print("\a", end="")
    except Exception:
        # Safe fallback in case sound is unsupported
        pass


def display_hangman(wrong_count, theme):
    """
    Displays a visual hangman figure based on wrong guesses.

    Parameters:
        wrong_count (int): Number of wrong guesses made.
        theme (dict): Current theme dictionary.
    """
    stages = [
        """
         +---+
         |   |
             |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
        /    |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
        / \\  |
             |
        =========
        """
    ]

    art = stages[wrong_count]
    print(colour_text(art, theme["warn"], theme))


# -----------------------------
# Helper Functions
# -----------------------------
def get_display_word(secret_word, guessed_letters):
    """
    Returns a display version of the secret word where guessed letters
    appear in their correct positions and unguessed letters appear as
    underscores. Letters are separated by spaces.

    Parameters:
        secret_word (str): The secret word to guess.
        guessed_letters (list): List of letters guessed so far.

    Returns:
        str: Display string with letters and underscores separated by spaces.
    """
    display_letters = []

    for letter in secret_word:
        if letter in guessed_letters:
            display_letters.append(letter)
        else:
            display_letters.append("_")

    return " ".join(display_letters)


# Example calls:
# print(get_display_word('elephant', ['e', 'l', 'a']))   # e l e _ _ a _ _
# print(get_display_word('cat', []))                     # _ _ _


def is_won(secret_word, guessed_letters):
    """
    Returns True if every letter in the secret word has been guessed.
    Returns False otherwise.

    Parameters:
        secret_word (str): The secret word to guess.
        guessed_letters (list): List of letters guessed so far.

    Returns:
        bool: True if all letters in the secret word have been guessed.
    """
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True


# Example calls:
# print(is_won('cat', ['c', 'a', 't']))   # True
# print(is_won('cat', ['c', 'a']))        # False


def is_lost(wrong_count, max_wrong):
    """
    Returns True if the number of wrong guesses has reached or exceeded
    the maximum allowed wrong guesses. Returns False otherwise.

    Parameters:
        wrong_count (int): Number of wrong guesses made.
        max_wrong (int): Maximum number of wrong guesses allowed.

    Returns:
        bool: True if the player has lost, False otherwise.
    """
    return wrong_count >= max_wrong


# Example calls:
# print(is_lost(6, 6))   # True
# print(is_lost(4, 6))   # False


def get_wrong_guesses(guessed_letters, secret_word):
    """
    Returns a list of guessed letters that are not in the secret word.

    Parameters:
        guessed_letters (list): List of letters guessed so far.
        secret_word (str): The secret word to guess.

    Returns:
        list: List of wrong guessed letters.
    """
    wrong_letters = []

    for letter in guessed_letters:
        if letter not in secret_word:
            wrong_letters.append(letter)

    return wrong_letters


# Example calls:
# print(get_wrong_guesses(['e', 'z', 'l', 'q'], 'elephant'))   # ['z', 'q']
# print(get_wrong_guesses(['a', 'b'], 'apple'))                # ['b']


# -----------------------------
# Main Game Loop
# -----------------------------
def play_hangman(secret_word, game_number=1):
    """
    Runs one complete game of Hangman for the given secret word.

    Requirements handled:
    - Maximum wrong guesses is 6
    - Shows current word state
    - Shows wrong guesses remaining
    - Shows wrong letters already guessed
    - Validates user input
    - Uses case-insensitive comparison
    - Ends on win or loss and prints result

    Parameters:
        secret_word (str): The secret word to guess.
        game_number (int): Current game number, used for changing themes.
    """
    theme = get_theme(game_number)

    # Convert the secret word to lowercase to make checking case-insensitive.
    secret_word = secret_word.lower()

    # Store all guessed letters.
    guessed_letters = []

    # Continue the game until the player wins or loses.
    while True:
        wrong_letters = get_wrong_guesses(guessed_letters, secret_word)
        wrong_count = len(wrong_letters)

        clear_screen()

        # Display the current theme name.
        print(colour_text("=" * 50, theme["title"], theme))
        print(colour_text(f"Hangman Theme: {theme['name']}", theme["title"], theme))
        print(colour_text("=" * 50, theme["title"], theme))

        # Display hangman art.
        display_hangman(wrong_count, theme)

        # Display the current progress of the word.
        display_word = get_display_word(secret_word, guessed_letters)
        print(colour_text(f"Word: {display_word}", theme["text"], theme))
        print(colour_text(f"Wrong guesses remaining: {MAX_WRONG - wrong_count}", theme["text"], theme))

        # Display wrong guessed letters so the player can see them.
        if len(wrong_letters) > 0:
            print(colour_text(f"Wrong guesses: {', '.join(wrong_letters)}", theme["bad"], theme))
        else:
            print(colour_text("Wrong guesses: none", theme["text"], theme))

        # Check if the player has already won.
        if is_won(secret_word, guessed_letters):
            print()
            print(colour_text(f"Congratulations! You guessed the word: {secret_word}", theme["good"], theme))
            play_sound("win")
            break

        # Check if the player has already lost.
        if is_lost(wrong_count, MAX_WRONG):
            print()
            print(colour_text(f"Game over. You ran out of guesses. The word was: {secret_word}", theme["bad"], theme))
            play_sound("lose")
            break

        print()

        # Input validation loop.
        while True:
            guess = input("Enter a letter: ").lower().strip()

            # Reject if input is not exactly one character.
            if len(guess) != 1:
                print(colour_text("Please enter exactly one character.", theme["warn"], theme))
                continue

            # Reject if input is not alphabetic.
            if not guess.isalpha():
                print(colour_text("Please enter a letter from A-Z.", theme["warn"], theme))
                continue

            # Reject if letter was already guessed.
            if guess in guessed_letters:
                print(colour_text("You already guessed that letter. Try a new one.", theme["warn"], theme))
                continue

            # If valid, stop the validation loop.
            break

        # Record the valid guess.
        guessed_letters.append(guess)

        # Tell the player whether the guess was correct.
        if guess in secret_word:
            print(colour_text(f"Good guess! '{guess}' is in the word.", theme["good"], theme))
            play_sound("good")
        else:
            print(colour_text(f"Sorry, '{guess}' is not in the word.", theme["bad"], theme))
            play_sound("bad")

        # Pause briefly so the player can read feedback.
        time.sleep(1.2)


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == '__main__':
    game_number = 1

    while True:
        clear_screen()

        # Welcome message
        print("Welcome to Hangman!")
        print("One player enters a secret word.")
        print("The other player guesses one letter at a time.")
        print(f"You can make at most {MAX_WRONG} wrong guesses.")
        print()

        # Ask for secret word
        secret_word = input("Enter a secret word for your opponent to guess: ").strip().lower()

        # Validate the secret word before starting
        while len(secret_word) == 0 or not secret_word.isalpha():
            print("The secret word must contain letters only and cannot be empty.")
            secret_word = input("Enter a secret word for your opponent to guess: ").strip().lower()

        # Clear the screen so the guessing player does not see the word.
        clear_screen()

        # Start the game
        play_hangman(secret_word, game_number)

        # Ask if the user wants to play again
        print()
        play_again = input("Would you like to play again? (yes/no): ").strip().lower()

        while play_again not in ["yes", "y", "no", "n"]:
            play_again = input("Please enter yes or no: ").strip().lower()

        if play_again in ["no", "n"]:
            print("Thanks for playing Hangman. Goodbye!")
            break

        game_number += 1