# PROBLEM 2: Temperature Pattern Analysis with Nested Loops
# Course: Intensive Foundation of Computer Science using Python
# Utilize: Nested loops + Conditionals + Dictionaries + Line plot

"""
PROBLEM 2: Generate and plot temperature patterns for multiple cities

SCENARIO:
Create a line plot showing temperature patterns for 3 cities over 12 months.
Use nested loops to generate realistic temperature data and conditionals
to handle seasonal variations.

REQUIREMENTS:
1. Create a dictionary with 3 cities as keys
2. For each city, generate 12 monthly temperature values
3. Use nested loops: outer loop for cities, inner loop for months
4. Use conditionals to create realistic patterns:
   - Winter months (Dec, Jan, Feb): colder temperatures
   - Summer months (Jun, Jul, Aug): warmer temperatures
   - Spring/Fall months: moderate temperatures
5. Plot all three cities on the same graph with different colors
6. Add legend, labels, title, and grid
7. Mark the coldest and warmest month for each city

HINTS:
- Month indices: 0=Jan, 1=Feb, ..., 11=Dec
- Winter months: indices 0, 1, 11 (Dec, Jan, Feb)
- Summer months: indices 5, 6, 7 (Jun, Jul, Aug)
- Use different colors for each city
- Use plt.plot() with marker='o' for points
- Use min() and max() to find coldest/warmest temperatures
- Mark special points with '^' (triangle up) and 'v' (triangle down)

YOUR CODE BELOW:
"""

import matplotlib.pyplot as plt
import numpy as np

def problem2():
    """
    Generate and plot temperature patterns for multiple cities
    """
    
    # Step 1: Create dictionary for cities and their temperatures
    cities = {
        "New York": [],
        "Los Angeles": [],
        "Chicago": []
    }

    # Step 2: Define month names
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    
    # Step 3: Generate temperatures using nested loops
    # Outer loop: for each city
    # Inner loop: for each month (0-11)
    #   Use conditionals:
    #     if month_index in [0, 1, 11]:  # Winter
    #     elif month_index in [5, 6, 7]:  # Summer
    #     elif month_index in [2, 3, 4]:  # Spring
    #     else:  # Fall

    for city in cities:
        for month_index in range(12):

            if month_index in [0, 1, 11]: #Winter
                temp = np.random.randint(-5, 5)
            elif month_index in [5, 6, 7]: #Summer
                temp = np.random.randint(25, 35)
            elif month_index in [2, 3, 4]: #Spring
                temp = np.random.randint(10, 20)
            else: #Fall
                temp = np.random.randint(10, 20)

            cities[city].append(temp)
    
    
    # Step 4: Create line plot for all cities
    for city in cities:
        plt.plot(months, cities[city], marker='o', label=city)
    
    # Step 5: Mark min and max temperatures for each city
    temps = cities[city]

    min_temp = min(temps)
    max_temp = max(temps)

    min_index = temps.index(min_temp)
    max_index = temps.index(max_temp)

    plt.plot(months[min_index], min_temp, 'v', markersize=10)
    plt.plot(months[max_index], max_temp, '^', markersize=10)
    
    # Step 6: Add formatting (labels, title, legend, grid)
    plt.title("Monthly Temperature Patterns")
    plt.xlabel("Month")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    
    # Step 7: Show the plot
    plt.show()

# Test your function
if __name__ == "__main__":
    problem2()
    print("Problem 2 complete!")
