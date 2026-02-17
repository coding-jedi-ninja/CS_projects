"""
Problem 3: Calculating the Factorial of a Number
Name: Arja Sadhukhan
NU ID: 003163346

# I confirm that AI code completion tools were disabled while writing this program.

In mathematics, the notation n! represents the factorial of the nonnegative 
integer n. The factorial of n is the product of all the nonnegative integers 
from 1 to n. For example:
    7! = 1 x 2 x 3 x 4 x 5 x 6 x 7 = 5,040
    4! = 1 x 2 x 3 x 4 = 24

Write a program that lets the user enter a nonnegative integer then uses a 
loop to calculate the factorial of that number. Display the factorial.
"""

def get_nonnegative_integer():
    """
    Prompt the user to enter a nonnegative integer.
    
    Returns:
        int: A nonnegative integer entered by the user
    
    TODO: Implement this function
    Hint: Use input() to get user input and convert it to an integer
    """
    pass
    while True:
        try:
            n = int(input("Enter a nonnegative integer: "))
            if n < 0:
                print(" Please enter 0 or a positive integer.")
                continue
            return n
        except ValueError:
            print("Invalid input. Please enter a whole number (like 0, 3, 10).")

def calculate_factorial(n):
    """
    Calculate the factorial of a nonnegative integer using a loop.
    
    Parameters:
        n (int): A nonnegative integer
    
    Returns:
        int: The factorial of n
    
    TODO: Implement this function
    Steps:
    1. Initialize result to 1 (remember: 0! = 1)
    2. Use a loop to multiply result by each number from 1 to n
    3. Return the result
    
    Important: Remember that 0! = 1 by definition
    """
    result = 1
    for num in range(1, n + 1):
        result *= num
    return result

def display_result (n, factorial_value):

    """
    Display the factorial result.

    Parameters:
        n (int): The original number
        factorial_value (int): The factorial of n
    """
    print(f"{n}! = {factorial_value}")

# TODO: Create a function to display the result
# Think about:
# - What parameters does it need?
# - What should it print?
# - How should it format the output?


def main():
    """
    Main function to run the factorial calculator.
    """
    # TODO: Get a nonnegative integer from the user
    
    # TODO: Calculate the factorial
    
    # TODO: Display the result
    
    n = get_nonnegative_integer()
    factorial_value = calculate_factorial(n)
    display_result(n, factorial_value)


# Run the program
main()
