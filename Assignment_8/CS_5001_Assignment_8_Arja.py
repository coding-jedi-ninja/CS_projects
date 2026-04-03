# hangman.py
# Team Members: Arja Sadhukhan, Saloni Surana, Ryu Hemingway
# NU ID(s): <003163346>, <ID 2>, <003163519>
# Course: CS 5001 / 5003 — Spring 2026

"""
Hangman Game with Matplotlib

For our HW8 assignment, we are tasked to change our program from playing the Hangman game in terminal to a matplotlib style.

"""

import matplotlib.pyplot as plt
import sys

# For Windows
try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False
    import tty
    import termios


plt.ion()


def masked_input(prompt=""):
    """
    Read input from the keyboard and display * for each typed character.
    Works in terminal/command-line environments.
    """
    print(prompt, end="", flush=True)
    chars = []

    if WINDOWS:
        while True:
            ch = msvcrt.getch()

            # Enter key
            if ch in {b'\r', b'\n'}:
                print()
                break

            # Backspace key
            elif ch == b'\x08':
                if chars:
                    chars.pop()
                    print("\b \b", end="", flush=True)

            # Regular character
            else:
                try:
                    decoded = ch.decode("utf-8")
                except UnicodeDecodeError:
                    continue

                if decoded.isprintable():
                    chars.append(decoded)
                    print("*", end="", flush=True)

    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)

                # Enter key
                if ch in ("\r", "\n"):
                    print()
                    break

                # Backspace/Delete key
                elif ch in ("\x7f", "\b"):
                    if chars:
                        chars.pop()
                        print("\b \b", end="", flush=True)

                # Regular character
                elif ch.isprintable():
                    chars.append(ch)
                    print("*", end="", flush=True)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return "".join(chars)


def draw_hangman(wrong_count):
    """
    Draw the gallows and the hangman figure based on the number
    of wrong guesses (0 to 6).
    """
    plt.clf()
    fig = plt.gcf()
    ax = fig.gca()

    ax.set_title(f"Wrong guesses: {wrong_count}")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    # Gallows
    ax.plot([2, 8], [1, 1], linewidth=3)   # base
    ax.plot([3, 3], [1, 8], linewidth=3)   # pole
    ax.plot([3, 6], [8, 8], linewidth=3)   # top beam
    ax.plot([6, 6], [8, 7], linewidth=3)   # rope

    # Head
    if wrong_count >= 1:
        head = plt.Circle((6, 6.2), 0.7, fill=False, linewidth=3)
        ax.add_patch(head)

    # Body
    if wrong_count >= 2:
        ax.plot([6, 6], [5.5, 3.6], linewidth=3)

    # Left arm
    if wrong_count >= 3:
        ax.plot([6, 5], [5.0, 4.3], linewidth=3)

    # Right arm
    if wrong_count >= 4:
        ax.plot([6, 7], [5.0, 4.3], linewidth=3)

    # Left leg
    if wrong_count >= 5:
        ax.plot([6, 5], [3.6, 2.0], linewidth=3)

    # Right leg
    if wrong_count >= 6:
        ax.plot([6, 7], [3.6, 2.0], linewidth=3)


def get_display_word(secret_word, guessed_letters):
    """
    Return the word display with guessed letters shown
    and underscores for letters not guessed yet.
    """
    display = []

    for letter in secret_word:
        if letter in guessed_letters:
            display.append(letter)
        else:
            display.append("_")

    return " ".join(display)


def is_word_guessed(secret_word, guessed_letters):
    """
    Return True if all letters in the secret word
    have been guessed.
    """
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True


def play_hangman():
    """
    Main game function.
    """
    print("Welcome to Hangman!")

    # Masked input for Player 1
    secret_word = masked_input("Player 1, enter the secret word: ").lower().strip()

    while not secret_word.isalpha():
        print("Invalid word. Please enter letters only.")
        secret_word = masked_input("Player 1, enter the secret word: ").lower().strip()

    # Clear screen effect
    print("\n" * 50)

    guessed_letters = []
    wrong_letters = []
    wrong_count = 0
    max_wrong = 6

    while wrong_count < max_wrong and not is_word_guessed(secret_word, guessed_letters):
        draw_hangman(wrong_count)
        plt.pause(0.1)

        print("\nWord:", get_display_word(secret_word, guessed_letters))
        print("Wrong guesses remaining:", max_wrong - wrong_count)
        print("Wrong letters guessed so far:", wrong_letters)

        guess = input("Player 2, enter a letter: ").lower().strip()

        while len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter exactly one letter.")
            guess = input("Player 2, enter a letter: ").lower().strip()

        if guess in guessed_letters or guess in wrong_letters:
            print("You already guessed that letter. Try again.")
            continue

        if guess in secret_word:
            guessed_letters.append(guess)
            print("Good guess!")
        else:
            wrong_letters.append(guess)
            wrong_count += 1
            print("Wrong guess!")

    # Final state
    draw_hangman(wrong_count)
    plt.pause(0.1)

    if is_word_guessed(secret_word, guessed_letters):
        print("\nWord:", get_display_word(secret_word, guessed_letters))
        print("Congratulations! You guessed the word!")
    else:
        print("\nYou lost!")
        print("The secret word was:", secret_word)

    plt.show()


def main():
    play_hangman()


if __name__ == "__main__":
    main()