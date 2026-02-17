

#x-coordinate, y-coordinate
# plt.scatter([1,2], [3,4])
# plt.show()

#Example: Student study time vs exam scores

# study_time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# exam_scores = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

# plt.scatter(study_time, exam_scores, color = 'red', s=100, alpha=0.5)
# plt.title('Study Time vs Exam Score')
# plt.xlabel('Hours Studied')
# plt.ylabel('Exam Score')
# plt.show()

#Simple data
# x = [1, 2, 3, 4, 5]
# y = [2, 4, 6, 8, 10]

# #Create the plot
# plt.plot(x, y)

# #Show the plot
# plt.show()

# #Show study hours per day
# days = [1, 2, 3, 4, 5, 6, 7]
# study_hours = [2, 3, 2.5, 4, 5, 3, 6]

# plt.plot(days, study_hours, color='blue', marker='o', linestyle='-', linewidth=2)
# plt.title('Study Hours per Day')
# plt.xlabel('Day of Week')
# plt.ylabel('Hours Studied')
# plt.grid(True)
# plt.show()

#Drawing function sin (x) with different number of plots
#Try changing the N value to see what changes
# N = 100

# x = np.linspace(0,2*np.pi, N)
# y = np.sin(x)
# plt.plot(x, y)
# plt.show()

#Example: Programming languages popularity
# languages = ['Python', 'Java', 'C++', 'JavaScript', 'Go']
# students = [45, 30, 15, 35, 10]

# plt.bar(languages, students, color= ['blue', 'orange', 'green', 'red', 'purple'])
# plt.title('Programming Languages Learned by Students')
# plt.xlabel('Language')
# plt.ylabel('Number of Students')
# plt.xticks(rotation=45) #Rotate labels if needed
# plt.tight_layout() #Prevents label cutoff
# plt.show()

# #Example: Programming languages popularity
# languages = ['Python', 'Java', 'C++', 'JavaScript', 'Go']
# students = [45, 30, 15, 35, 10]

# plt.barh(languages, students, color=['blue', 'orange', 'green', 'red', 'purple'])
# plt.title('Programming Languages (Horizontal)')
# plt.xlabel('Number of Students')
# plt.ylabel('Language')
# plt.show()

#Create a bar chart comparing the population of 4 cities

# cities = ['San Jose', 'Fremont', 'Santa Clara', 'Sunnyvale']
# population = [4500, 3000, 5000, 6000]

# plt.bar(cities, population, color= ['blue', 'orange', 'green', 'red'])
# plt.title('Population of Cities Comparison Chart')
# plt.xlabel('Cities')
# plt.ylabel('Population')
# plt.xticks(rotation=45) #Rotate labels if needed
# plt.tight_layout() #Prevents label cutoff
# plt.show()

#Example: Student exam scores distribution

#Generate random exam scores

# np.random.seed(42) #For reproducability
# exam_scores = np.random.normal(75, 10, 100) #Mean, StdDev=10, 100 students

# plt.hist(exam_scores, bins=10, color='skyblue', edgecolor='black')
# plt.title('Distribution of Exam Scores')
# plt.xlabel('Score')
# plt.ylabel('Number of Students')
# plt.axvline(exam_scores.mean(), color = 'red', linestyle= '--', label='Mean')
# plt.legend()
# plt.show()

#Create scores
# np.random.seed(42)
# scores = np.random.normal(75, 10, 100)

# #Draw a passing line
# plt.hist(scores, bins=15)
# plt.axvline(scores.min(), color= 'red', label ='Lowest Score')
# plt.axvline(scores.max(), color='green', label='Highest Score')
# plt.axvline(scores.mean(), color='black', linestyle='--', label='Average')
# plt.legend()
# plt.show()

# #Create 2x2 grid of plots
# fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# #Plot 1: Line Plot
# axes[0, 0]. plot([1, 2, 3, 4], [1, 4, 9, 16])
# axes[0, 0].set_title('Line Plot')

# #Plot 2: Scatter plot
# axes[0, 1].scatter([1, 2, 3, 4], [1, 4, 9, 16], color='red')
# axes[0, 1].set_title('Scatter Plot')

# #Plot 3: Bar chart
# axes[1, 0].bar(['A', 'B', 'C'], [3, 7, 5])
# axes[1, 0].set_title('Bar Chart')
        
# #Plot 4: Histogram
# axes[1, 1].hist(np.random.randn(100), bins=20)
# axes[1, 1].set_title('Histogram')

# plt.tight_layout()
# plt.show()

# N = 100
# x = np.linspace(0,2*np.pi, N)
# y = np.sin(x)

# plt.plot(x,y)

# #Change the font size and spacing of axes

# plt.xticks(fontsize = 20)
# plt.yticks(np.linspace(-1, 1, 5), fontsize = 20)

# plt.show()
                                    
#Control figure size and quality <= try changing configuration
# plt.figure(figsize=(20, 10), dpi=20)
# plt.plot([1, 2, 3], [1, 4, 9])
# plt.show()

# plt.plot([1, 2, 3, 4], [1, 4, 9, 16], label = 'Quadratic Growth', marker = 'o')
# plt.plot([1, 2, 3, 4], [1, 2, 3, 4], label = 'Linear Growth', marker = 's')

# plt.legend(loc='upper left')
# plt.title('Growth Comparison')
# plt.xlabel('Time')
# plt.ylabel('Value')

# #Add annotation
# plt.annotate('Inflection point', xy=(3, 9), xytext=(2, 12), arrowprops=dict(arrowstyle='->', color='red'))

# plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

#Set seaborn style
# sns.set_style("whitegrid")

# #Sample data
# tips = sns.load_dataset('tips') #Built-in dataset

# sns.violinplot(data=tips, x='day', y='total_bill')
# plt.title('Distribution of Bills by Day')
# plt.show()

#Set seaborn style
# sns.set_style("whitegrid")

#Sample data
# tips = sns.load_dataset('tips') #Built-in dataset

# #Create correlation matrix
# correlation = tips.corr(numeric_only=True)

# #Plot heatmap
# sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
# plt.title('Correlation Matrix')
# plt.show()


#Set seaborn style
sns.set_style("whitegrid")

#Sample data
tips = sns.load_dataset('tips') #Built-in dataset

sns.pairplot(tips, hue='time')
plt.show()
