# CS 5001, Assignment #3 Rock, Paper, Scissors Game
# DO NOT use AI tools while working on this assignment.

#Name: Arja Sadhukhan
#NUID: 003163346

# I confirm that AI code completion tools were disabled while writing this program.

import random

rock = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper = """
_______
---'   ____)____
            ______)
            _______)
            _______)
---.__________)
"""

scissors = """
    _______
---'   ____)____
            ______)
         __________)
      (____)
---.__(___)
"""
art = [rock, paper, scissors]

# TO DO: Print the title of the game and/or welcome message

choices = ["rock", "paper", "scissors"]

print("Welcome to the Rock-Paper-Scissors game!")
print("What is your choice? Please type 0 for rock, 1 for paper, and 2 for scissors.")

# TO DO: Prompt the user for input (0, 1, 2)
user_input = input()

#Validate input
if user_input not in ["0", "1", "2"]:
    print("Invalid input. Please run the program again and enter 0, 1, or 2.")
else:
    user_choice = int(user_input)
    computer_choice = random.randint(0, 2)

# TO DO: Print ASCII art for user's choice

print(f"You chose {choices[user_choice]}.")
print(art[user_choice])

# TO DO: Generate computer choice

print(f"Computer chose {choices[computer_choice]}.")

# TO DO: Print ASCII art for computer's choice

print(art[computer_choice])

# TO DO: Decide winner using conditionals

if user_choice == computer_choice:
    print("It's a tie.")
elif (
    (user_choice == 0 and computer_choice == 2) or
    (user_choice == 1 and computer_choice == 0) or
    (user_choice == 2 and computer_choice == 1)
    ):

# TO DO: Print result

    print("You win.")
else:
    print("You lose.")
