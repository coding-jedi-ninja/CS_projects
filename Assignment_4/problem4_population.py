"""
Problem 4: Population
Name: Arja Sadhukhan
NU ID: 003163346

# I confirm that AI code completion tools were disabled while writing this program.

Write a program that predicts the approximate size of a population of organisms. 
The application should prompt the user to enter the starting number of organisms, 
the average daily population increase (as a percentage), and the number of days 
the organisms will be left to multiply.

Example:
    Starting number of organisms: 2 
    Average daily increase: 30% 
    Number of days to multiply: 10

The program should display a table showing the population for each day.
"""

def get_population_inputs():
    """
    Prompt user for initial population parameters.
    
    Returns:
        (starting_population, daily_increase_rate, num_days)
        daily_increase_rate should be as a decimal (e.g., 0.30 for 30%)
    
    TODO: Implement this function
    Steps:
    1. Prompt for starting number of organisms
    2. Prompt for daily increase percentage
    3. Prompt for number of days
    4. Convert percentage to decimal (divide by 100)
    5. Return all three values
    """
    while True:
        try:
            starting_population = float(input("Starting number of organisms: "))
            if starting_population <= 0:
                print("Starting population must be > 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            daily_increase_percent = float(input("Average daily increase (%): "))
            if daily_increase_percent < 0:
                print("Daily increase cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid percentage.")

    while True:
        try:
            num_days = int(input("Number of days to multiply: "))
            if num_days < 1:
                print("Number of days must be at least 1.")
                continue
            break
        except ValueError:
            print("Please enter a whole number of days.")

    daily_increase_rate = daily_increase_percent / 100
    return starting_population, daily_increase_rate, num_days
    


def calculate_next_day_population(current_population, daily_increase_rate):
    """
    Calculate population for the next day.
    
    Parameters:
        current_population (float): Current day's population
        daily_increase_rate (float): Daily increase rate as decimal (e.g., 0.30 for 30%)
    
    Returns:
        float: Population for the next day
    
    TODO: Implement this function
    Hint: Next population = current population * (1 + daily_increase_rate)
    """
    return current_population * (1 + daily_increase_rate)


# TODO: Create a function to display the population table
# This function should:
# - Take starting_population, daily_increase_rate, and num_days as parameters
# - Print a header for the table
# - Use a loop to calculate and display population for each day
# - Use the calculate_next_day_population() function in your loop
# - Format output nicely (e.g., "Day 1: 2.00 organisms")


def display_population_table(starting_population, daily_increase_rate, num_days):

    """
    Display a table of population by day.
    """
    population = starting_population

    print("\nPopulation Growth Table")
    print("--------------------------")
    print(f"Day 1: {population:.2f} organisms")

    for day in range(2, num_days + 1):
        population = calculate_next_day_population(population, daily_increase_rate)
        print(f"Day {day}: {population:.2f} organisms")


def main():
    """
    Main function to run the population growth predictor.
    """
    # TODO: Get inputs from user using get_population_inputs()
    
    # TODO: Display the population table using your display function
    
    starting_population, daily_increase_rate, num_days = get_population_inputs()
    display_population_table(starting_population, daily_increase_rate, num_days)


# Run the program
main()
