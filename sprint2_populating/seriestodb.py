import pandas as pd
import numpy as np
from IPython.display import display

data = pd.read_csv('new_data/books_corrected.csv')

#get the "series" column of the dataframe

series = data['series']

#delete all the NaN values of series
series = series.dropna()

# Delete the parenthesis from the string

s_no_parens = series.str.strip('()')

# Split the string at ' #' and take the first part
s_cleaned = s_no_parens.str.split(' #').str[0]

#Select distinct values from s_cleaned
distinct_values = s_cleaned.unique()

#convert numpy array to dataframe
distinct_values_df = pd.DataFrame(distinct_values)

# rename the column to "series_name"
distinct_values_df.columns = ['name_series']

display(distinct_values_df)

#save the dataframe to a csv file
distinct_values_df.to_csv('new_data/SeriesList.csv', index=False)

