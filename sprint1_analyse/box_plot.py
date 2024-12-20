# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = 'bigboss_book.csv'  # Specify the full path to your file if needed
data = pd.read_csv(file_path)

# Replace commas with dots in the 'average_rating' column and convert to float
data['average_rating'] = data['average_rating'].str.replace(',', '.').astype(float)

# Create groups for 'number_of_pages'
# Here, we divide into groups (0-100, 100-300, etc.)
bins = [0, 100, 300, 500, 1000, float('inf')]
labels = ['<100 pages', '100-300 pages', '300-500 pages', '500-1000 pages', '>1000 pages']
data['pages_group'] = pd.cut(data['number_of_pages'], bins=bins, labels=labels)

# Sort the data by 'average_rating'
data_sorted = data.sort_values(by='average_rating', ascending=False)

# Create a boxplot to visualize 'average_rating' based on 'pages_group'
plt.figure(figsize=(10, 6))
sns.boxplot(x='pages_group', y='average_rating', data=data_sorted, color='#7C9792') 

# Add titles and labels
plt.title('Distribution of Average Ratings by Number of Pages (Sorted by Rating)', fontsize=15)
plt.xlabel('Number of Pages', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)

# Display the graph
plt.show()
