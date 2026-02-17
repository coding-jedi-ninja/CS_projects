"""
Problem 2: Sleep Debt
Name: Arja Sadhukhan
NU ID: 003163346

# I confirm that AI code completion tools were disabled while writing this program.

A "sleep debt" represents the difference between a person's desirable and 
actual amount of sleep. Write a program that prompts the user to enter how 
many hours he or she slept each day over a period of 7 days. Using 8 hours 
per day as the desirable amount of sleep, determine his or her sleep debt by 
calculating the total hours of sleep they got over the seven-day period and 
subtracting that from the total hours of sleep he or she should have got. 
If the user does not have a sleep debt, display a message expressing your jealousy.
"""

def get_sleep_hours(num_days):
    """
    Prompt the user to enter hours slept for each day.
    
    Parameters:
        num_days (int): Number of days to track sleep
    
    Returns:
        float: Total hours of sleep over all days
    
    TODO: Implement this function
    Steps:
    1. Initialize a variable to store total sleep hours
    2. Use a loop to prompt for sleep hours for each day
    3. Add each day's hours to the total
    4. Return the total
    """

    total_sleep = 0.0

    for day in range(1, num_days + 1):
        while True:
            try:
                hours = float(input(f"Enter sleep hours for day {day}:"))
                if hours < 0:
                    print("Hours cannot be negative. Try again.")
                    continue
                total_sleep += hours
                break
            except ValueError:
                print("Please enter a valid number (example: 7.5).")

    return total_sleep


# TODO: Create a function to calculate sleep debt
# Think about what parameters it needs and what it should return
# Hint: You'll need actual sleep hours and desirable sleep hours

def calculate_sleep_debt(actual_sleep_hours, desirable_sleep_hours):
    """
    TODO: Write the docstring
    - What does this function do?
    - What parameters does it need?
    - What does it return?
    """
    return desirable_sleep_hours - actual_sleep_hours


def display_sleep_debt_results(sleep_debt):
    """
    Display the sleep debt results with appropriate message.
    
    Parameters:
        sleep_debt (float): The calculated sleep debt (can be positive, negative, or zero)
    
    TODO: Implement this function
    Steps:
    1. If sleep_debt > 0: Display how many hours of sleep debt they have
    2. If sleep_debt <= 0: Express jealousy that they got enough/extra sleep
    """
    if sleep_debt > 0:
        print(f"You have a sleep debt of {sleep_debt:.1f} hours this week.")
    else:
        print("You've got enough sleep. Yaay, good for you! I am so jealous!")


def main():
    """
    Main function to run the sleep debt calculator.
    """
    # Constants
    DESIRABLE_HOURS_PER_DAY = 8
    NUM_DAYS = 7
    
    # TODO: Get total actual sleep hours from user
    
    # TODO: Calculate total desirable sleep hours
    
    # TODO: Calculate sleep debt using your calculate_sleep_debt function
    
    # TODO: Display results using display_sleep_debt_results function
    
    actual_sleep = get_sleep_hours(NUM_DAYS)
    desirable_sleep = DESIRABLE_HOURS_PER_DAY * NUM_DAYS
    sleep_debt = calculate_sleep_debt(actual_sleep, desirable_sleep)
    display_sleep_debt_results(sleep_debt)



# Run the program
main()
