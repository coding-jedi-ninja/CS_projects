"""
CS 5001 - HW 9
Hangman with AI Assistance

Team Members:
- Arja Sadhukhan (NUID: 003163346)
- Ryu Hemingway
- Saloni Surana

This program is a two-player Hangman game.
Player 1 enters a secret word using masked input.
Player 2 guesses one letter at a time.
The game checks input, tracks wrong guesses,
and draws the hangman using matplotlib.
"""

import matplotlib.pyplot as plt
import pwinput


# Maximum number of wrong guesses allowed before the game ends
MAX_WRONG_GUESSES = 6


def get_secret_word():
    """
    Ask Player 1 to enter the secret word.
    The letters are masked with * so Player 2 cannot see the word.

    Returns:
        str: a valid lowercase secret word
    """
    while True:
        secret_word = pwinput.pwinput(
            prompt="Player 1, enter the secret word: ",
            mask="*"
        ).lower()

        if not secret_word.isalpha():
            print("Invalid word. Please enter letters only.")
        else:
            return secret_word


def display_word(secret_word, guessed_letters):
    """
    Show the letters that have been guessed correctly.
    Show underscores for letters that have not been guessed yet.

    Args:
        secret_word (str): the hidden word
        guessed_letters (set): letters guessed so far

    Returns:
        str: word display with spaces
    """
    displayed = []

    for letter in secret_word:
        if letter in guessed_letters:
            displayed.append(letter)
        else:
            displayed.append("_")

    return " ".join(displayed)


def get_guess(guessed_letters):
    """
    Ask Player 2 for one guess.
    Keep asking until the guess is valid.

    A valid guess must:
    - be one character long
    - be a letter
    - not have been guessed already

    Args:
        guessed_letters (set): letters already guessed

    Returns:
        str: one valid guessed letter
    """
    while True:
        guess = input("Enter your guess: ").lower().strip()

        if len(guess) != 1:
            print("Please enter exactly one letter.")
        elif not guess.isalpha():
            print("Please enter a valid alphabetic letter.")
        elif guess in guessed_letters:
            print("You already guessed that letter. Try again.")
        else:
            return guess


def draw_hangman(wrong_guesses):
    """
    Draw the gallows and hangman figure based on the number
    of wrong guesses.

    Args:
        wrong_guesses (int): number of incorrect guesses
    """
    plt.clf()

    # Draw the gallows
    plt.plot([0, 2], [0, 0], linewidth=2)      # base
    plt.plot([1, 1], [0, 5], linewidth=2)      # pole
    plt.plot([1, 3], [5, 5], linewidth=2)      # top beam
    plt.plot([3, 3], [5, 4.2], linewidth=2)    # rope

    # Draw the head
    if wrong_guesses >= 1:
        head = plt.Circle((3, 3.7), 0.3, fill=False, linewidth=2)
        plt.gca().add_patch(head)

    # Draw the body
    if wrong_guesses >= 2:
        plt.plot([3, 3], [3.4, 2.2], linewidth=2)

    # Draw the left arm
    if wrong_guesses >= 3:
        plt.plot([3, 2.5], [3.0, 2.6], linewidth=2)

    # Draw the right arm
    if wrong_guesses >= 4:
        plt.plot([3, 3.5], [3.0, 2.6], linewidth=2)

    # Draw the left leg
    if wrong_guesses >= 5:
        plt.plot([3, 2.5], [2.2, 1.4], linewidth=2)

    # Draw the right leg
    if wrong_guesses >= 6:
        plt.plot([3, 3.5], [2.2, 1.4], linewidth=2)

    plt.xlim(-0.5, 4.5)
    plt.ylim(-0.5, 5.5)
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.title(f"Wrong guesses: {wrong_guesses}/{MAX_WRONG_GUESSES}")
    plt.show(block=False)
    plt.pause(0.5)


def is_word_guessed(secret_word, guessed_letters):
    """
    Check whether every letter in the secret word
    has been guessed.

    Args:
        secret_word (str): the hidden word
        guessed_letters (set): letters guessed so far

    Returns:
        bool: True if all letters are guessed, otherwise False
    """
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True


def play_hangman():
    """
    Run the full Hangman game.
    """
    print("Welcome to Hangman!")

    secret_word = get_secret_word()
    guessed_letters = set()
    wrong_guesses = 0

    # Show the empty gallows at the start
    draw_hangman(wrong_guesses)

    while wrong_guesses < MAX_WRONG_GUESSES and not is_word_guessed(secret_word, guessed_letters):
        print("\nWord:", display_word(secret_word, guessed_letters))
        print("Guessed letters:", " ".join(sorted(guessed_letters)) if guessed_letters else "None")
        print("Wrong guesses left:", MAX_WRONG_GUESSES - wrong_guesses)

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
        else:
            wrong_guesses += 1
            print("Wrong guess!")
            draw_hangman(wrong_guesses)

    print("\nFinal word:", display_word(secret_word, guessed_letters))

    if is_word_guessed(secret_word, guessed_letters):
        print("Congratulations! Player 2 guessed the word!")
    else:
        # Make sure the full hangman is visible before showing the losing message
        draw_hangman(wrong_guesses)
        print(f"Game over! The word was: {secret_word}")


# Start the game
play_hangman()