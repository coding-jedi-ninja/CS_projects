# PROBLEM 3: Population Growth Simulation with While Loop
# Course: Intensive Foundation of Computer Science using Python
# Utilize: While loop + Conditionals + Lists + Subplots

"""
PROBLEM 3: Simulate population growth with conditions and plot the results

SCENARIO:
Simulate population growth for a city over time. Use a while loop to continue
until certain conditions are met. Store data in lists and visualize growth.

REQUIREMENTS:
1. Start with initial population of 1000
2. Use a while loop that continues until:
   - Population exceeds 10,000 OR
   - 50 years have passed
3. Each year:
   - If population < 5000: growth rate is 8%
   - If population >= 5000: growth rate is 5%
   - If year is divisible by 10: there's a special event (add 500 people)
4. Store year and population in separate lists
5. Create TWO subplots side by side:
   a. Left subplot: Line plot of population over time
   b. Right subplot: Bar chart showing growth for each decade
6. Add annotations for special events on the line plot
7. Print final population and years elapsed

HINTS:
- While loop: while population < 10000 and year < max_years:
- Check divisibility: if year % 10 == 0:
- Create subplots: fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
- Plot on specific subplot: ax1.plot(...) or ax2.bar(...)
- Annotations: ax1.annotate(text, xy=(x, y), ...)
- Keep track of special event years in a separate list

YOUR CODE BELOW:
"""

import matplotlib.pyplot as plt
import numpy as np

def problem3():
    """
    Simulate population growth with conditions
    """
    
    # Step 1: Initialize variables
    population = 1000
    year = 0
    max_years = 50

    years = [year]
    populations = [population]

    event_years = []
    event_pops = []
    
    # Step 2: While loop for simulation
    # while population < 10000 and year < max_years:

    while population <= 10000 and year < max_years:
      year += 1   #Increment year
      
      if population < 5000:   # Determine growth rate based on population
            growth_rate = 0.08
      else:
         growth_rate = 0.05
      
      population = population * (1 + growth_rate)  #Apply growth

      if year % 10 == 0:   #Check for special events (year % 10 == 0)
          population += 500
          event_years.append(year)
          event_pops.append(population)

      years.append(year)   #Store values in lists
      populations.append(population)

    year_to_pop = dict(zip(years, populations))

    decade_labels = []
    decade_growth = []

    # Decades: 0-10, 10-20, ...
    for start in range(0, year, 10):
        end = min(start + 10, year)
        growth = year_to_pop[end] - year_to_pop[start]

        decade_labels.append(f"{start}-{end}")
        decade_growth.append(growth)
   
    
    # Step 3: Create two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    
    # Step 4: Left subplot - Population growth line plot
    ax1.plot(years, populations, marker='o')
    ax1.set_title("Population Growth Over Time")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Population")
    ax1.grid(True)
    
    # Step 5: Right subplot - Growth by decade bar chart
    ax2.bar(decade_labels, decade_growth)
    ax2.set_title("Population Growth by Decade")
    ax2.set_xlabel("Decade")
    ax2.set_ylabel("Population Increase")
    ax2.grid(True, axis='y')
    
    # Step 6: Add annotations for special events
    for ev_year, ev_pop in zip(event_years, event_pops):
        ax1.annotate(
            "+500 event",
            xy=(ev_year, ev_pop),
            xytext=(ev_year, ev_pop + 300),
            arrowprops=dict(arrowstyle="->")
        )

    for label in ax2.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')

    # Step 7: Print summary and show plot
    print(f"Years elapsed: {year}")
    print(f"Final population: {population:.2f}")

    plt.tight_layout()
    plt.show()

# Test your function
if __name__ == "__main__":
    problem3()
    print("Problem 3 complete!")
