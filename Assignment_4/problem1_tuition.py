"""
Problem 1: Tuition Increase
Name: Arja Sadhukhan
NU ID: 003163346

# I confirm that AI code completion tools were disabled while writing this program.

At one college, the tuition for a full-time student is $8,000 per semester. 
It has been announced that the tuition will increase by 3 percent each year 
for the next 5 years. Write a program with a loop that displays the projected 
semester tuition amount for the next 5 years.
"""

def calculate_tuition_for_year(current_tuition, increase_rate):
    """
    Calculate the tuition for the next year based on the increase rate.
    
    Parameters:
        current_tuition (float): The current year's tuition amount
        increase_rate (float): The annual increase rate (e.g., 0.03 for 3%)
    
    Returns:
        float: The tuition amount for the next year
    
    TODO: Implement this function
    """
    pass

    next_tuition = current_tuition * (1 + increase_rate)
    return next_tuition


def display_tuition_projection(starting_tuition, increase_rate, num_years):
    """
    Display the tuition projection for the specified number of years.
    
    Parameters:
        starting_tuition (float): The initial tuition amount
        increase_rate (float): The annual increase rate (e.g., 0.03 for 3%)
        num_years (int): Number of years to project
    
    TODO: Implement this function
    Steps:
    1. Print a header for the output
    2. Use a loop to calculate and display tuition for each year
    3. Use the calculate_tuition_for_year() function inside your loop
    4. Format the output nicely (e.g., "Year 1: $8,240.00")
    """
    pass

    print(f"Projected Semester Tuition for {num_years} years")
    print("**************************************")
    print(f"Starting Tuition: ${starting_tuition}")

    tuition = starting_tuition

    for year in range(1, num_years + 1):
        tuition = calculate_tuition_for_year(tuition, increase_rate)
        print(f"Year {year}: ${tuition:.2f}")


def main():
    """
    Main function to run the tuition projection program.
    """
    # TODO: Define the constants
    STARTING_TUITION = 8000
    INCREASE_RATE = 0.03
    NUM_YEARS = 5
    
    # TODO: Call the display_tuition_projection function with the constants
    display_tuition_projection(STARTING_TUITION, INCREASE_RATE, NUM_YEARS)
    
    pass


# Run the program
main()
