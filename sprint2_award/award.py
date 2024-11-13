import pandas as pd

# Load the original CSV file
df = pd.read_csv("C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/books_corrected.csv")

# Select "id" and "awards" columns
df_awards = df[['id', 'awards']].copy()

# Delete the lines without any awards
df_awards.dropna(subset=['awards'], inplace=True)

# Create a list to store awards data
awards_data = []

# We loop on the books and awards
for _, row in df_awards.iterrows():
    book_id = row['id']
    awards = row['awards'].split(',') # Split the different award with a comma
    
    for award in awards: 
        # Extract the year of the award (If there's one)
        award_year = pd.Series(award).str.extract(r'\((\d{4})\)')[0].values[0]
        
        # Clean the text to delete the year between parenthesis and get the award all alone
        award_name = pd.Series(award).str.replace(r'\s*\(\d{4}\)', '', regex=True).values[0]
        
        # Add the information to the liste in a dictionary
        awards_data.append({
            'award_name': award_name.strip(),
            'book_id': book_id,
            'award_year': award_year
        })

# Convert the list to DataFrame
awards_df = pd.DataFrame(awards_data)

# Add an unique identifier for every award
awards_df['award_id'] = awards_df.groupby('award_name').ngroup() + 1

# Reorganize the rows in the objective of getting a clearer display
awards_df = awards_df[['award_id', 'award_name', 'book_id', 'award_year']]

# Save the result in a new CSV File
awards_df.to_csv("awards_books.csv")

# Shows a preview of the generated file
print(awards_df.head())
