# I confirm that AI code completion tools were disabled while writing this program.
# Name: Arja Sadhukhan
# NU ID: 003163346

"""
Problem 3: Largest List Item

Design a function that accepts a list as an argument and returns the largest value 
in the list. The function should use recursion to find the largest item.
"""


def find_largest(lst):
    """
    Recursively finds and returns the largest value in a list
    
    Args:
        lst (list): A list of comparable values
        
    Returns:
        The largest value in the list
    """
    if not lst:
        raise ValueError("List cannot be empty")
    
    #Base case: only one element
    if len(lst) == 1:
        return lst[0]
    
    #Recursive case:
    #Compare first element with largest in the rest of the list
    largest_in_rest = find_largest(lst[1:])
    return lst[0] if lst[0] > largest_in_rest else largest_in_rest


def main():
    """
    Main function to test the find_largest function
    """
    # Test case 1: list of integers
    test_list1 = [3, 7, 2, 9, 4, 1, 8]
    print(f"Test List 1: {test_list1}")
    print(f"Largest value: {find_largest(test_list1)}")
    
    # Test case 2: list with negative numbers
    test_list2 = [-5, -2, -10, -1, -7]
    print(f"\nTest List 2: {test_list2}")
    print(f"Largest value: {find_largest(test_list2)}")
    
    # Test case 3: list with one element
    test_list3 = [42]
    print(f"\nTest List 3: {test_list3}")
    print(f"Largest value: {find_largest(test_list3)}")
    
    # Test case 4: list with floats
    test_list4 = [3.5, 7.2, 2.1, 9.8, 4.3]
    print(f"\nTest List 4: {test_list4}")
    print(f"Largest value: {find_largest(test_list4)}")
    
    # User input test
    print("\n--- User Input Test ---")
    try:
        user_input = input("Enter a list of numbers separated by spaces: ")
        user_list = [float(x) for x in user_input.split()]
        if user_list:
            print(f"Your list: {user_list}")
            print(f"Largest value: {find_largest(user_list)}")
        else:
            print("Empty list provided.")
    except ValueError:
        print("Invalid input. Please enter numbers separated by spaces.")


if __name__ == "__main__":
    main()
