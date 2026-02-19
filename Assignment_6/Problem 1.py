# PROBLEM 1: Student Grade Distribution with Conditionals
# Course: Intensive Foundation of Computer Science using Python
# Utilize: For loops + If/elif/else + Dictionaries + Bar chart

"""
PROBLEM 1: Analyze and visualize student grades using conditionals

SCENARIO:
You have a list of student scores. Categorize them into letter grades
and create a bar chart showing the distribution.

REQUIREMENTS:
1. Given a list of 30 student scores (ranging from 0-100)
2. Use a loop to iterate through scores
3. Use conditionals to assign letter grades:
   - A: 90-100
   - B: 80-89
   - C: 70-79
   - D: 60-69
   - F: 0-59
4. Store the count of each grade in a dictionary
5. Create a bar chart showing the distribution of letter grades
6. Add proper labels, title, and colors
7. Display the total number of students in each category on the bars

HINTS:
- Start with an empty dictionary: grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
- Use a for loop: for score in scores:
- Use if/elif/else to check score ranges
- Use plt.bar() to create the bar chart
- Use different colors for each grade (green for A, red for F, etc.)
- Display numbers on bars using plt.text()

YOUR CODE BELOW:
"""

import matplotlib.pyplot as plt
import numpy as np

def problem1():
    """
    Categorize student scores and visualize grade distribution
    """
    
    # Given data: 30 student scores
    scores = [85, 92, 78, 90, 88, 76, 95, 84, 72, 89,
              91, 65, 74, 88, 93, 70, 82, 77, 86, 94,
              68, 79, 87, 91, 73, 81, 96, 75, 83, 69]
    
    # Step 1: Create a dictionary to store grade counts
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    # Step 2: Loop through scores and categorize them
    for score in scores:
        if score>= 90:
            grade_counts['A'] += 1
        elif score >= 80:
            grade_counts['B'] += 1
        elif score >= 70:
            grade_counts['C'] += 1
        elif score >= 60:
            grade_counts['D'] += 1
        else:
            grade_counts['F'] += 1
    
    # Step 3: Create bar chart
    grades = list(grade_counts.keys())
    counts = list(grade_counts.values())

    colors = ['green', 'blue', 'orange', 'purple', 'red']

    plt.bar(grades, counts, color=colors)
    
    # Step 4: Add labels and formatting
    plt.title("Grade Distribution (30 Students)")
    plt.xlabel("Letter Grade")
    plt.ylabel("Number of Students")
    
    # Step 5: Display values on top of bars
    for i in range(len(grades)):
        plt.text(i, counts[i] + 0.1, str(counts[i]), ha='center')
    
    # Step 6: Show the plot
    plt.show()

# Test your function
if __name__ == "__main__":
    problem1()
    print("Problem 1 complete!")
