# PROBLEM 4: Data Filtering and Visualization
# Course: Intensive Foundation of Computer Science using Python
# Utilize: Loops + Conditionals + List of dictionaries + Scatter plot

"""
PROBLEM 4: Filter and visualize data based on multiple conditions

SCENARIO:
You have sales data for a store. Filter the data based on conditions,
organize it in data structures, and create meaningful visualizations.

REQUIREMENTS:
1. Given lists of products, prices, and quantities sold
2. Create a list of dictionaries, where each dictionary represents a product
   with keys: 'name', 'price', 'quantity', 'revenue'
3. Use loops and conditionals to:
   - Calculate total revenue for each product (price × quantity)
   - Filter products into categories based on revenue:
     * High performers: revenue > $5000
     * Medium performers: $2000 <= revenue <= $5000
     * Low performers: revenue < $2000
4. Create a scatter plot where:
   - X-axis: Price
   - Y-axis: Quantity sold
   - Color: Different color for each performance category
   - Size: Proportional to revenue (revenue/10 works well)
5. Add product name labels next to each point
6. Add a legend explaining the color coding
7. Calculate and print summary statistics:
   - Total revenue across all products
   - Average revenue
   - Top performing product
   - Lowest performing product

HINTS:
- Create dictionary: {'name': products[i], 'price': prices[i], ...}
- Use .append() to add dictionaries to list
- Scatter for each category separately (different colors)
- Use plt.annotate() to add product labels
- Use max() with key parameter: max(list, key=lambda x: x['revenue'])

YOUR CODE BELOW:
"""

import matplotlib.pyplot as plt
import numpy as np

def problem4():
    """
    Filter and visualize sales data based on conditions
    """
    
    # Given data
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam',
                'Headphones', 'Speaker', 'Microphone', 'Tablet', 'Phone']
    prices = [1200, 25, 75, 300, 80, 150, 200, 100, 500, 800]
    quantities = [5, 100, 50, 15, 40, 30, 20, 25, 12, 18]
    
    # Step 1: Create list of dictionaries
    
    products_data = []

    for i in range(len(products)):
        revenue = prices[i] * quantities[i]

        product_dict = {
            'name': products[i],
            'price': prices[i],
            'quantity': quantities[i],
            'revenue': revenue
        }

        products_data.append(product_dict)
    
    # Step 2: Categorize products based on revenue
    # Create three empty lists: high_performers, medium_performers, low_performers
    # Loop through products_data and use conditionals to categorize

    high_performers = []
    medium_performers = []
    low_performers = []

    for item in products_data:
        rev = item['revenue']

        if rev > 5000:
            high_performers.append(item)
        elif 2000 <= rev <= 5000:
            medium_performers.append(item)
        else:
            low_performers.append(item)
    
    # Step 3: Create scatter plot
    plt.figure(figsize=(10, 6))
    
    # Step 4: Plot each category with different colors

    # Loop through each category and plot
    
    def plot_category(data, color, label):
        for item in data:
            plt.scatter(
                item['price'],
                item['quantity'],
                color=color,
                s=item['revenue'] / 10,   # size proportional to revenue
                alpha=0.7,
                label=label
            )
            # To avoid repeating legend labels multiple times:
            label = None

    plot_category(high_performers, "green", "High performers (> $5000)")
    plot_category(medium_performers, "orange", "Medium performers ($2000-$5000)")
    plot_category(low_performers, "red", "Low performers (< $2000)")
    
    # Step 5: Add product name labels
    
    for item in products_data:
        plt.annotate(
            item['name'],
            (item['price'], item['quantity']),
            textcoords="offset points",
            xytext=(5, 5),
            ha='left'
        )

    
    # Step 6: Add formatting (labels, title, legend, grid)
    plt.title("Sales Performance: Price vs Quantity")
    plt.xlabel("Price ($)")
    plt.ylabel("Quantity Sold")
    plt.grid(True)

    # Legend (avoid duplicates)
    plt.legend()
    
    # Step 7: Calculate and print summary statistics
    total_revenue = sum(item['revenue'] for item in products_data)
    average_revenue = total_revenue / len(products_data)

    top_product = max(products_data, key=lambda x: x['revenue'])
    lowest_product = min(products_data, key=lambda x: x['revenue'])

    print("----- Summary Statistics -----")
    print(f"Total revenue: ${total_revenue:.2f}")
    print(f"Average revenue: ${average_revenue:.2f}")
    print(f"Top performing product: {top_product['name']} (${top_product['revenue']:.2f})")
    print(f"Lowest performing product: {lowest_product['name']} (${lowest_product['revenue']:.2f})")

   
    # Step 8: Show the plot
    plt.show()

# Test your function
if __name__ == "__main__":
    problem4()
    print("Problem 4 complete!")
