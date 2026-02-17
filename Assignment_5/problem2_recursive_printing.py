# I confirm that AI code completion tools were disabled while writing this program.
# Name: Arja Sadhukhan
# NU ID: 003163346

"""
Problem 2: Recursive Printing

Design a recursive function that accepts an integer argument, n, and prints every 
second number from n down to a minimum of 0. Assume that n is always a 
positive integer.
"""


def recursive_print(n):
    """
    Recursively prints every second number from n down to 0
    
    Args:
        n (int): A positive integer
    """
    #Base case: stop when n < 0
    if n < 0:
        return
    
    #Print the current number
    print(n)

    #Call the function again with a smaller value
    recursive_print(n - 2)


def main():
    """
    Main function to test the recursive print function
    """
    
    # Get user input
    print("\n--- User Input Test ---")
    try:
        num = int(input("Enter a positive integer: "))
        if num >= 0:
            print(f"\nPrinting every second number from {num} down to 0:")
            recursive_print(num)
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter an integer.")


if __name__ == "__main__":
    main()
